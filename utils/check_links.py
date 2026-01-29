#!/usr/bin/env python3
"""
Link Checker for GitHub Pages
=============================

Validates all links in HTML files for a GitHub Pages site.

Usage:
------
# Check local files only (fast, no network)
python check_links.py

# Include external URL validation
python check_links.py --check-external

# Check specific file
python check_links.py --file index.html

# Verbose output
python check_links.py -v

# Custom base path
python check_links.py --base-path /path/to/repo

Exit Codes:
-----------
0 - All links valid
1 - One or more broken links found
2 - Script error (invalid arguments, etc.)
"""

import argparse
import html.parser
import os
import re
import sys
import urllib.parse
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

# Optional HTTP checking
try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False


# =============================================================================
# DATA CLASSES
# =============================================================================

@dataclass
class Link:
    """Represents a link found in an HTML file."""
    url: str
    source_file: str
    line_number: int
    link_type: str  # 'local', 'fragment', 'external', 'cdn', 'skip'
    element: str    # 'a', 'img', 'link', 'script'


@dataclass
class CheckResult:
    """Result of checking a single link."""
    link: Link
    valid: bool
    error: Optional[str] = None


@dataclass
class Summary:
    """Summary statistics for the check run."""
    total_links: int = 0
    valid_links: int = 0
    broken_links: int = 0
    skipped_links: int = 0
    files_checked: int = 0
    results: List[CheckResult] = field(default_factory=list)


# =============================================================================
# HTML PARSER
# =============================================================================

class LinkExtractor(html.parser.HTMLParser):
    """Extract all links from HTML content."""

    def __init__(self, source_file: str):
        super().__init__()
        self.source_file = source_file
        self.links: List[Link] = []
        self.ids: Set[str] = set()  # For fragment validation

    def handle_starttag(self, tag: str, attrs: list):
        attrs_dict = dict(attrs)
        line = self.getpos()[0]

        # Track IDs for fragment validation
        if 'id' in attrs_dict:
            self.ids.add(attrs_dict['id'])

        # Extract links based on tag type
        if tag == 'a' and 'href' in attrs_dict:
            self._add_link(attrs_dict['href'], line, 'a')
        elif tag == 'img' and 'src' in attrs_dict:
            self._add_link(attrs_dict['src'], line, 'img')
        elif tag == 'link' and 'href' in attrs_dict:
            self._add_link(attrs_dict['href'], line, 'link')
        elif tag == 'script' and 'src' in attrs_dict:
            self._add_link(attrs_dict['src'], line, 'script')

    def _add_link(self, url: str, line: int, element: str):
        link_type = self._classify_link(url)
        self.links.append(Link(
            url=url,
            source_file=self.source_file,
            line_number=line,
            link_type=link_type,
            element=element
        ))

    def _classify_link(self, url: str) -> str:
        """Classify link type based on URL pattern."""
        if url.startswith('#'):
            return 'fragment'
        elif url.startswith(('http://', 'https://')):
            if 'cdn.' in url or 'jsdelivr' in url or 'unpkg' in url or 'katex' in url:
                return 'cdn'
            return 'external'
        elif url.startswith(('mailto:', 'tel:', 'javascript:')):
            return 'skip'
        else:
            return 'local'


# =============================================================================
# CHECKERS
# =============================================================================

class LocalFileChecker:
    """Check if local file references exist."""

    def __init__(self, base_path: Path):
        self.base_path = base_path

    def check(self, link: Link) -> CheckResult:
        if link.link_type != 'local':
            return CheckResult(link=link, valid=True, error="Not a local link")

        # Resolve relative path from source file location
        source_dir = Path(link.source_file).parent
        target_path = self.base_path / source_dir / link.url

        # Normalize path (handle ../ etc)
        try:
            target_path = target_path.resolve()
        except (OSError, ValueError) as e:
            return CheckResult(link=link, valid=False, error=f"Invalid path: {e}")

        # Check existence
        if target_path.exists():
            return CheckResult(link=link, valid=True)
        else:
            # Try to show relative path for clearer error
            try:
                rel_path = target_path.relative_to(self.base_path)
            except ValueError:
                rel_path = target_path

            return CheckResult(
                link=link,
                valid=False,
                error=f"File not found: {rel_path}"
            )


class FragmentChecker:
    """Check if fragment anchors exist in target documents."""

    def __init__(self, base_path: Path):
        self.base_path = base_path
        self._id_cache: Dict[str, Set[str]] = {}

    def check(self, link: Link) -> CheckResult:
        if link.link_type != 'fragment':
            return CheckResult(link=link, valid=True, error="Not a fragment")

        fragment = link.url.lstrip('#')

        # Get IDs from same file
        ids = self._get_ids(link.source_file)

        if fragment in ids:
            return CheckResult(link=link, valid=True)
        else:
            return CheckResult(
                link=link,
                valid=False,
                error=f"Fragment '#{fragment}' not found in {link.source_file}"
            )

    def _get_ids(self, file_path: str) -> Set[str]:
        """Extract all id attributes from an HTML file."""
        if file_path in self._id_cache:
            return self._id_cache[file_path]

        full_path = self.base_path / file_path
        if not full_path.exists():
            return set()

        with open(full_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Simple regex to find id attributes
        ids = set(re.findall(r'id=["\']([^"\']+)["\']', content))
        self._id_cache[file_path] = ids
        return ids


class ExternalChecker:
    """Check HTTP status of external URLs."""

    def __init__(self, timeout: int = 10):
        self.timeout = timeout
        self._cache: Dict[str, Tuple[bool, Optional[str]]] = {}

    def check(self, link: Link) -> CheckResult:
        if link.link_type not in ('external', 'cdn'):
            return CheckResult(link=link, valid=True, error="Not external")

        if not HAS_REQUESTS:
            return CheckResult(
                link=link,
                valid=True,
                error="Skipped (requests not installed)"
            )

        # Check cache first
        if link.url in self._cache:
            valid, error = self._cache[link.url]
            return CheckResult(link=link, valid=valid, error=error)

        try:
            response = requests.head(
                link.url,
                timeout=self.timeout,
                allow_redirects=True,
                headers={'User-Agent': 'Mozilla/5.0 LinkChecker'}
            )

            if response.status_code < 400:
                self._cache[link.url] = (True, None)
                return CheckResult(link=link, valid=True)
            else:
                error = f"HTTP {response.status_code}"
                self._cache[link.url] = (False, error)
                return CheckResult(link=link, valid=False, error=error)

        except requests.exceptions.Timeout:
            error = "Request timeout"
            self._cache[link.url] = (False, error)
            return CheckResult(link=link, valid=False, error=error)
        except requests.exceptions.RequestException as e:
            error = f"Request failed: {str(e)}"
            self._cache[link.url] = (False, error)
            return CheckResult(link=link, valid=False, error=error)


# =============================================================================
# REPORTER
# =============================================================================

class Reporter:
    """Generate console output for check results."""

    def __init__(self, verbose: bool = False, color: bool = True):
        self.verbose = verbose
        self.use_color = color and sys.stdout.isatty()

    def _color(self, text: str, code: str) -> str:
        """Apply ANSI color codes to text."""
        if not self.use_color:
            return text
        colors = {
            'red': '\033[91m',
            'green': '\033[92m',
            'yellow': '\033[93m',
            'blue': '\033[94m',
            'reset': '\033[0m'
        }
        return f"{colors.get(code, '')}{text}{colors['reset']}"

    def print_result(self, result: CheckResult):
        """Print a single check result."""
        if result.valid:
            if self.verbose:
                print(f"  {self._color('[OK]', 'green')} {result.link.url}")
        else:
            print(f"  {self._color('[BROKEN]', 'red')} {result.link.url}")
            print(f"    Source: {result.link.source_file}:{result.link.line_number}")
            print(f"    Error: {result.error}")

    def print_summary(self, summary: Summary):
        """Print final summary statistics."""
        print("\n" + "=" * 60)
        print("LINK CHECK SUMMARY")
        print("=" * 60)
        print(f"Files checked:  {summary.files_checked}")
        print(f"Total links:    {summary.total_links}")
        print(f"  Valid:        {self._color(str(summary.valid_links), 'green')}")
        print(f"  Broken:       {self._color(str(summary.broken_links), 'red')}")
        print(f"  Skipped:      {summary.skipped_links}")
        print("=" * 60)

        if summary.broken_links > 0:
            print(f"\n{self._color('FAILED', 'red')}: {summary.broken_links} broken link(s) found")
        else:
            print(f"\n{self._color('PASSED', 'green')}: All links valid")


# =============================================================================
# MAIN CHECKER
# =============================================================================

class LinkChecker:
    """Main link checker orchestrator."""

    def __init__(
        self,
        base_path: Path,
        check_external: bool = False,
        verbose: bool = False,
        no_color: bool = False
    ):
        self.base_path = base_path
        self.check_external = check_external
        self.verbose = verbose

        self.local_checker = LocalFileChecker(base_path)
        self.fragment_checker = FragmentChecker(base_path)
        self.external_checker = ExternalChecker() if check_external else None
        self.reporter = Reporter(verbose=verbose, color=not no_color)

    def find_html_files(self) -> List[Path]:
        """Find all HTML files to check."""
        html_files = []

        # Root index.html
        index = self.base_path / 'index.html'
        if index.exists():
            html_files.append(index)

        # Quiz files
        quiz_dir = self.base_path / 'quiz'
        if quiz_dir.exists():
            html_files.extend(sorted(quiz_dir.glob('*.html')))

        return html_files

    def check_file(self, file_path: Path) -> List[CheckResult]:
        """Check all links in a single HTML file."""
        relative_path = file_path.relative_to(self.base_path)

        print(f"\nChecking: {relative_path}")

        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Extract links
        extractor = LinkExtractor(str(relative_path))
        extractor.feed(content)

        results = []
        for link in extractor.links:
            if link.link_type == 'skip':
                continue

            if link.link_type == 'local':
                result = self.local_checker.check(link)
            elif link.link_type == 'fragment':
                result = self.fragment_checker.check(link)
            elif link.link_type in ('external', 'cdn'):
                if self.external_checker:
                    result = self.external_checker.check(link)
                else:
                    result = CheckResult(link=link, valid=True, error="Skipped")
            else:
                continue

            results.append(result)
            self.reporter.print_result(result)

        return results

    def run(self) -> Summary:
        """Run the complete link check."""
        print(f"Link Checker - Base: {self.base_path}")
        print(f"External checks: {'enabled' if self.check_external else 'disabled'}")

        html_files = self.find_html_files()

        if not html_files:
            print("No HTML files found!")
            return Summary()

        summary = Summary(files_checked=len(html_files))

        for file_path in html_files:
            results = self.check_file(file_path)

            for result in results:
                summary.total_links += 1
                summary.results.append(result)

                if result.error == "Skipped":
                    summary.skipped_links += 1
                elif result.valid:
                    summary.valid_links += 1
                else:
                    summary.broken_links += 1

        self.reporter.print_summary(summary)
        return summary


# =============================================================================
# CLI
# =============================================================================

def main():
    parser = argparse.ArgumentParser(
        description='Check all links in GitHub Pages site',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  # Check local files only (fast)
  python check_links.py

  # Include external URL checking
  python check_links.py --check-external

  # Check from specific directory
  python check_links.py --base-path /path/to/repo

  # Verbose output
  python check_links.py -v
        '''
    )

    parser.add_argument(
        '--base-path', '-b',
        type=Path,
        default=Path('.'),
        help='Base path of the repository (default: current directory)'
    )
    parser.add_argument(
        '--check-external', '-e',
        action='store_true',
        help='Also check external URLs (requires requests library)'
    )
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Show all links, not just broken ones'
    )
    parser.add_argument(
        '--no-color',
        action='store_true',
        help='Disable colored output'
    )

    args = parser.parse_args()

    # Resolve base path
    base_path = args.base_path.resolve()

    if not base_path.exists():
        print(f"Error: Path does not exist: {base_path}", file=sys.stderr)
        return 2

    if not (base_path / 'index.html').exists():
        print(f"Warning: No index.html found in {base_path}", file=sys.stderr)

    # Run checker
    checker = LinkChecker(
        base_path=base_path,
        check_external=args.check_external,
        verbose=args.verbose,
        no_color=args.no_color
    )

    summary = checker.run()

    # Exit code based on results
    return 1 if summary.broken_links > 0 else 0


if __name__ == '__main__':
    sys.exit(main())
