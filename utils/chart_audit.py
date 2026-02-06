#!/usr/bin/env python3
"""Chart Quality Audit Tool - Analyzes chart.py files against 20 criteria."""

import ast
import re
import json
import sys
from pathlib import Path
from typing import Dict, List, Any

def analyze_chart(chart_path: Path) -> Dict[str, Any]:
    """Analyze a single chart.py against all 20 criteria."""
    results = {
        'path': str(chart_path),
        'criteria': {},
        'pass_count': 0,
        'fail_count': 0
    }

    # Read source code
    try:
        source = chart_path.read_text(encoding='utf-8')
    except Exception as e:
        results['error'] = str(e)
        return results

    # Parse AST
    try:
        tree = ast.parse(source)
    except SyntaxError as e:
        results['error'] = f"Syntax error: {e}"
        return results

    # Extract docstring
    docstring = ast.get_docstring(tree) or ""

    # A1: Font size >= 12
    font_match = re.search(r"'font\.size':\s*(\d+)", source)
    font_size = int(font_match.group(1)) if font_match else 0
    results['criteria']['A1_font_size'] = {
        'pass': font_size >= 12,
        'value': font_size,
        'threshold': '>= 12'
    }

    # A2: Axis label size >= 11
    label_match = re.search(r"'axes\.labelsize':\s*(\d+)", source)
    label_size = int(label_match.group(1)) if label_match else 0
    results['criteria']['A2_axis_label_size'] = {
        'pass': label_size >= 11,
        'value': label_size,
        'threshold': '>= 11'
    }

    # A3: Figure size adequate
    # Check for figsize in plt.subplots(), plt.figure(), AND rcParams
    figsize_match = re.search(r'figsize\s*=\s*\((\d+(?:\.\d+)?),\s*(\d+(?:\.\d+)?)\)', source)
    if not figsize_match:
        # Also check rcParams pattern: 'figure.figsize': (10, 6)
        figsize_match = re.search(r"'figure\.figsize'\s*:\s*\((\d+(?:\.\d+)?),\s*(\d+(?:\.\d+)?)\)", source)
    if figsize_match:
        width, height = float(figsize_match.group(1)), float(figsize_match.group(2))
        adequate = width >= 10 or height >= 6
    else:
        width, height, adequate = 0, 0, False
    results['criteria']['A3_figure_size'] = {
        'pass': adequate,
        'value': f'{width}x{height}',
        'threshold': 'width >= 10 OR height >= 6'
    }

    # A4: DPI quality
    png_dpi_match = re.search(r"savefig.*?\.png.*?dpi\s*=\s*(\d+)", source, re.DOTALL)
    pdf_dpi_match = re.search(r"savefig.*?\.pdf.*?dpi\s*=\s*(\d+)", source, re.DOTALL)
    # Also check for dpi in any savefig
    any_dpi = re.findall(r'dpi\s*=\s*(\d+)', source)
    png_dpi = int(png_dpi_match.group(1)) if png_dpi_match else (int(any_dpi[1]) if len(any_dpi) > 1 else 150)
    pdf_dpi = int(pdf_dpi_match.group(1)) if pdf_dpi_match else (int(any_dpi[0]) if any_dpi else 300)
    results['criteria']['A4_dpi_quality'] = {
        'pass': png_dpi >= 150 and pdf_dpi >= 300,
        'value': f'PNG:{png_dpi}, PDF:{pdf_dpi}',
        'threshold': 'PNG >= 150, PDF >= 300'
    }

    # A5: Tick label size >= 10
    xtick_match = re.search(r"'xtick\.labelsize':\s*(\d+)", source)
    ytick_match = re.search(r"'ytick\.labelsize':\s*(\d+)", source)
    xtick_size = int(xtick_match.group(1)) if xtick_match else 0
    ytick_size = int(ytick_match.group(1)) if ytick_match else 0
    results['criteria']['A5_tick_label_size'] = {
        'pass': xtick_size >= 10 and ytick_size >= 10,
        'value': f'X:{xtick_size}, Y:{ytick_size}',
        'threshold': 'both >= 10'
    }

    # A6: Legend font size >= 10
    legend_match = re.search(r"'legend\.fontsize':\s*(\d+)", source)
    legend_size = int(legend_match.group(1)) if legend_match else 0
    results['criteria']['A6_legend_font_size'] = {
        'pass': legend_size >= 10,
        'value': legend_size,
        'threshold': '>= 10'
    }

    # A7: Uses standard ML color palette
    ml_colors = ['MLPURPLE', 'MLBLUE', 'MLORANGE', 'MLGREEN', 'MLRED']
    colors_defined = sum(1 for c in ml_colors if c in source)
    results['criteria']['A7_color_palette'] = {
        'pass': colors_defined >= 3,  # At least 3 of 5 colors used
        'value': f'{colors_defined}/5 ML colors',
        'threshold': '>= 3 ML colors defined'
    }

    # B1: Axis labels present
    has_xlabel = 'set_xlabel' in source
    has_ylabel = 'set_ylabel' in source
    results['criteria']['B1_axis_labels'] = {
        'pass': has_xlabel and has_ylabel,
        'value': f'X:{has_xlabel}, Y:{has_ylabel}',
        'threshold': 'both present'
    }

    # B2: Title descriptive (5+ words)
    title_match = re.search(r"set_title\s*\(\s*['\"](.+?)['\"]", source)
    title_text = title_match.group(1) if title_match else ""
    title_words = len(title_text.split()) if title_text else 0
    results['criteria']['B2_title_descriptive'] = {
        'pass': title_words >= 5,
        'value': f'{title_words} words',
        'threshold': '>= 5 words'
    }

    # B3: Legend clarity
    plot_count = len(re.findall(r'\.plot\(', source))
    has_legend = 'legend(' in source
    needs_legend = plot_count >= 2
    results['criteria']['B3_legend_clarity'] = {
        'pass': not needs_legend or has_legend,
        'value': f'{plot_count} plots, legend:{has_legend}',
        'threshold': 'legend if 2+ plots'
    }

    # B4: Grid lines
    has_grid = 'grid(True' in source or 'grid(alpha' in source
    results['criteria']['B4_grid_lines'] = {
        'pass': has_grid,
        'value': has_grid,
        'threshold': 'grid(True) present'
    }

    # B5: Has data annotations
    annotation_count = len(re.findall(r'\.annotate\(|ax\.text\(', source))
    results['criteria']['B5_data_annotations'] = {
        'pass': annotation_count >= 1,
        'value': f'{annotation_count} annotations',
        'threshold': '>= 1 annotation'
    }

    # B6: Axis labels include units
    xlabel_match = re.search(r"set_xlabel\s*\(['\"]([^'\"]+)['\"]", source)
    ylabel_match = re.search(r"set_ylabel\s*\(['\"]([^'\"]+)['\"]", source)
    xlabel = xlabel_match.group(1) if xlabel_match else ""
    ylabel = ylabel_match.group(1) if ylabel_match else ""
    unit_patterns = r'[\(%$€£¥]|\bper\b|\b/\b|years?|months?|days?|seconds?|%'
    has_units = bool(re.search(unit_patterns, xlabel, re.I)) or bool(re.search(unit_patterns, ylabel, re.I))
    results['criteria']['B6_units_specified'] = {
        'pass': has_units,
        'value': f'X:"{xlabel}", Y:"{ylabel}"',
        'threshold': 'unit indicator in axis label'
    }

    # C1: Docstring quality
    docstring_len = len(docstring)
    results['criteria']['C1_docstring_quality'] = {
        'pass': docstring_len >= 50,
        'value': f'{docstring_len} chars',
        'threshold': '>= 50 chars'
    }

    # C2: Theory reference (Author (Year) pattern - including "et al.")
    theory_pattern = re.search(r'[A-Z][a-z]+(?:\s+(?:et\s+al\.?|and\s+[A-Z][a-z]+))?\s*\(\d{4}\)', docstring)
    results['criteria']['C2_theory_reference'] = {
        'pass': bool(theory_pattern),
        'value': theory_pattern.group(0) if theory_pattern else 'None',
        'threshold': 'Author (Year) format'
    }

    # C3: Theory annotation on chart
    has_annotation = 'ax.text(' in source or 'ax.annotate(' in source or '.text(' in source
    results['criteria']['C3_theory_annotation'] = {
        'pass': has_annotation,
        'value': has_annotation,
        'threshold': 'ax.text or ax.annotate present'
    }

    # C4: Has LaTeX formula or economic model
    # Match: $...$ patterns, r'$...$' raw strings, or common LaTeX symbols
    has_latex = bool(re.search(r"r?['\"]?\$[^$]+\$|\\\\frac|\\\\sum|\\\\int|\\\\sigma|\\\\alpha|\\\\beta|\\\\cdot|cdot|\\\\Delta|\\\\omega|\\\\pi|≤|≥|→|×|÷|²|³", source))
    results['criteria']['C4_economic_model'] = {
        'pass': has_latex,
        'value': has_latex,
        'threshold': 'LaTeX formula present'
    }

    # D1: File completeness
    chart_dir = chart_path.parent
    png_exists = (chart_dir / 'chart.png').exists()
    pdf_exists = (chart_dir / 'chart.pdf').exists()
    results['criteria']['D1_file_completeness'] = {
        'pass': png_exists and pdf_exists,
        'value': f'PNG:{png_exists}, PDF:{pdf_exists}',
        'threshold': 'both files exist'
    }

    # D2: Code quality (Path(__file__) usage)
    uses_path_file = 'Path(__file__)' in source
    results['criteria']['D2_code_quality'] = {
        'pass': uses_path_file,
        'value': uses_path_file,
        'threshold': 'Path(__file__) used'
    }

    # E1: Course coverage (informational - checked at lesson level)
    # This criterion is tracked at lesson level, not individual chart
    results['criteria']['E1_coverage_info'] = {
        'pass': True,  # Always passes at chart level
        'value': 'See lesson summary',
        'threshold': 'informational only'
    }

    # Calculate totals
    for criterion, data in results['criteria'].items():
        if data['pass']:
            results['pass_count'] += 1
        else:
            results['fail_count'] += 1

    return results


def audit_directory(base_path: Path) -> Dict[str, Any]:
    """Audit all chart.py files in the repository."""
    charts = sorted(base_path.glob('L*/*/chart.py'))

    all_results = {
        'total_charts': len(charts),
        'total_criteria': 20,
        'summary': {
            'total_pass': 0,
            'total_fail': 0,
            'by_criterion': {}
        },
        'charts': []
    }

    # Initialize criterion counters
    criteria_names = [
        'A1_font_size', 'A2_axis_label_size', 'A3_figure_size', 'A4_dpi_quality',
        'A5_tick_label_size', 'A6_legend_font_size', 'A7_color_palette',
        'B1_axis_labels', 'B2_title_descriptive', 'B3_legend_clarity', 'B4_grid_lines',
        'B5_data_annotations', 'B6_units_specified',
        'C1_docstring_quality', 'C2_theory_reference', 'C3_theory_annotation',
        'C4_economic_model',
        'D1_file_completeness', 'D2_code_quality',
        'E1_coverage_info'
    ]
    for name in criteria_names:
        all_results['summary']['by_criterion'][name] = {'pass': 0, 'fail': 0}

    # Analyze each chart
    for chart_path in charts:
        result = analyze_chart(chart_path)
        all_results['charts'].append(result)

        all_results['summary']['total_pass'] += result['pass_count']
        all_results['summary']['total_fail'] += result['fail_count']

        for criterion, data in result['criteria'].items():
            if data['pass']:
                all_results['summary']['by_criterion'][criterion]['pass'] += 1
            else:
                all_results['summary']['by_criterion'][criterion]['fail'] += 1

    return all_results


def main():
    """Main entry point."""
    if len(sys.argv) > 1:
        base_path = Path(sys.argv[1])
    else:
        base_path = Path(__file__).parent.parent

    if not base_path.exists():
        print(f"Error: Path does not exist: {base_path}", file=sys.stderr)
        sys.exit(1)

    results = audit_directory(base_path)

    # Print summary
    print("=" * 60)
    print("CHART QUALITY AUDIT SUMMARY")
    print("=" * 60)
    print(f"Charts analyzed: {results['total_charts']}")
    print(f"Total criteria: {results['total_criteria']}")
    print(f"Total data points: {results['total_charts'] * results['total_criteria']}")
    print(f"Pass: {results['summary']['total_pass']}")
    print(f"Fail: {results['summary']['total_fail']}")
    pass_rate = results['summary']['total_pass'] / (results['summary']['total_pass'] + results['summary']['total_fail']) * 100
    print(f"Pass rate: {pass_rate:.1f}%")
    print()

    print("By Criterion:")
    for criterion, counts in results['summary']['by_criterion'].items():
        rate = counts['pass'] / (counts['pass'] + counts['fail']) * 100 if (counts['pass'] + counts['fail']) > 0 else 0
        status = "PASS" if counts['fail'] == 0 else f"FAIL ({counts['fail']})"
        print(f"  {criterion}: {status} ({rate:.0f}%)")
    print()

    # Print failures
    print("FAILURES:")
    for chart in results['charts']:
        failures = [k for k, v in chart['criteria'].items() if not v['pass']]
        if failures:
            print(f"  {chart['path']}")
            for f in failures:
                print(f"    - {f}: {chart['criteria'][f]['value']} (need {chart['criteria'][f]['threshold']})")

    # Output JSON
    json_path = base_path / '.omc' / 'reports' / 'chart-audit-results.json'
    json_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(results, indent=2))
    print(f"\nFull results saved to: {json_path}")

    # Return exit code based on failures
    sys.exit(0 if results['summary']['total_fail'] == 0 else 1)


if __name__ == '__main__':
    main()
