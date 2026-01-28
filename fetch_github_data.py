"""
GitHub Data Fetcher
Collects repository statistics from GitHub API for Digital-AI-Finance organization
"""

import os
import json
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import time


class GitHubDataFetcher:
    """Fetch and process GitHub repository data"""

    def __init__(self, org_name: str, token: Optional[str] = None):
        self.org_name = org_name
        self.token = token or os.getenv('GITHUB_TOKEN')
        self.base_url = "https://api.github.com"
        self.headers = {
            'Accept': 'application/vnd.github.v3+json'
        }
        if self.token:
            self.headers['Authorization'] = f'token {self.token}'

        self.session = requests.Session()
        self.session.headers.update(self.headers)

    def _make_request(self, url: str, params: Optional[Dict] = None) -> Dict:
        """Make API request with rate limit handling"""
        try:
            response = self.session.get(url, params=params)

            # Check rate limit
            remaining = int(response.headers.get('X-RateLimit-Remaining', 0))
            if remaining < 10:
                reset_time = int(response.headers.get('X-RateLimit-Reset', 0))
                wait_time = max(reset_time - time.time(), 0) + 1
                print(f"Rate limit low. Waiting {wait_time:.0f} seconds...")
                time.sleep(wait_time)

            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as e:
            print(f"API request failed: {e}")
            return {}

    def get_organization_info(self) -> Dict:
        """Fetch organization metadata"""
        url = f"{self.base_url}/orgs/{self.org_name}"
        data = self._make_request(url)

        return {
            'name': data.get('name', self.org_name),
            'description': data.get('description', ''),
            'public_repos': data.get('public_repos', 0),
            'created_at': data.get('created_at', ''),
            'updated_at': data.get('updated_at', ''),
            'url': data.get('html_url', ''),
            'avatar_url': data.get('avatar_url', '')
        }

    def get_repositories(self) -> List[Dict]:
        """Fetch all public repositories"""
        url = f"{self.base_url}/orgs/{self.org_name}/repos"
        repos = []
        page = 1

        while True:
            data = self._make_request(url, params={'page': page, 'per_page': 100})
            if not data:
                break

            repos.extend(data)

            if len(data) < 100:
                break
            page += 1

        return repos

    def get_repository_details(self, repo_name: str) -> Dict:
        """Fetch detailed repository information"""
        url = f"{self.base_url}/repos/{self.org_name}/{repo_name}"
        return self._make_request(url)

    def get_repository_languages(self, repo_name: str) -> Dict[str, int]:
        """Fetch language statistics for a repository"""
        url = f"{self.base_url}/repos/{self.org_name}/{repo_name}/languages"
        return self._make_request(url)

    def get_commits(self, repo_name: str, since_days: int = 90) -> List[Dict]:
        """Fetch recent commits"""
        since_date = (datetime.now() - timedelta(days=since_days)).isoformat()
        url = f"{self.base_url}/repos/{self.org_name}/{repo_name}/commits"

        commits = []
        page = 1

        while True:
            data = self._make_request(url, params={
                'since': since_date,
                'page': page,
                'per_page': 100
            })

            if not data:
                break

            commits.extend(data)

            if len(data) < 100:
                break
            page += 1

        return commits

    def get_contributors(self, repo_name: str) -> List[Dict]:
        """Fetch repository contributors"""
        url = f"{self.base_url}/repos/{self.org_name}/{repo_name}/contributors"
        return self._make_request(url) or []

    def get_repository_content(self, repo_name: str, path: str = "") -> List[Dict]:
        """Fetch repository file listing"""
        url = f"{self.base_url}/repos/{self.org_name}/{repo_name}/contents/{path}"
        data = self._make_request(url)
        return data if isinstance(data, list) else []

    def analyze_repository_maturity(self, repo_name: str, repo_data: Dict) -> Dict:
        """Calculate repository maturity score"""
        score = 0
        max_score = 100
        details = {}

        # Commit count (0-20 points)
        commit_count = repo_data.get('commit_count', 0)
        commit_score = min(commit_count * 2, 20)
        score += commit_score
        details['commits'] = {'score': commit_score, 'count': commit_count}

        # Documentation (0-20 points)
        has_readme = repo_data.get('has_readme', False)
        has_license = repo_data.get('has_license', False)
        doc_score = (has_readme * 10) + (has_license * 10)
        score += doc_score
        details['documentation'] = {
            'score': doc_score,
            'readme': has_readme,
            'license': has_license
        }

        # Testing (0-20 points)
        has_tests = repo_data.get('has_tests', False)
        test_score = has_tests * 20
        score += test_score
        details['testing'] = {'score': test_score, 'has_tests': has_tests}

        # License (0-15 points)
        license_score = has_license * 15
        score += license_score
        details['license'] = {'score': license_score, 'has_license': has_license}

        # CI/CD (0-15 points)
        has_ci = repo_data.get('has_ci', False)
        ci_score = has_ci * 15
        score += ci_score
        details['ci_cd'] = {'score': ci_score, 'has_ci': has_ci}

        # Community (0-10 points)
        stars = repo_data.get('stars', 0)
        forks = repo_data.get('forks', 0)
        community_score = min((stars + forks), 10)
        score += community_score
        details['community'] = {
            'score': community_score,
            'stars': stars,
            'forks': forks
        }

        return {
            'total_score': score,
            'max_score': max_score,
            'percentage': (score / max_score) * 100,
            'details': details,
            'stage': self._determine_lifecycle_stage(score)
        }

    def _determine_lifecycle_stage(self, score: int) -> str:
        """Determine repository lifecycle stage based on maturity score"""
        if score >= 80:
            return 'Production'
        elif score >= 60:
            return 'Beta'
        elif score >= 40:
            return 'Alpha'
        elif score >= 20:
            return 'Planning'
        else:
            return 'Concept'

    def fetch_all_data(self) -> Dict:
        """Fetch comprehensive organization and repository data"""
        print(f"Fetching data for {self.org_name}...")

        # Organization info
        org_info = self.get_organization_info()
        print(f"Organization: {org_info.get('name', self.org_name)}")

        # Get all repositories
        repos = self.get_repositories()
        print(f"Found {len(repos)} repositories")

        repository_data = []

        for repo in repos:
            repo_name = repo['name']
            print(f"Processing {repo_name}...")

            # Basic info
            repo_details = {
                'name': repo_name,
                'full_name': repo['full_name'],
                'description': repo.get('description', ''),
                'url': repo['html_url'],
                'created_at': repo['created_at'],
                'updated_at': repo['updated_at'],
                'pushed_at': repo.get('pushed_at', ''),
                'stars': repo['stargazers_count'],
                'forks': repo['forks_count'],
                'watchers': repo['watchers_count'],
                'open_issues': repo['open_issues_count'],
                'default_branch': repo['default_branch'],
                'has_readme': 'README' in [f['name'].upper() for f in self.get_repository_content(repo_name)],
                'has_license': repo.get('license') is not None
            }

            # Languages
            languages = self.get_repository_languages(repo_name)
            repo_details['languages'] = languages

            # Commits
            commits = self.get_commits(repo_name, since_days=90)
            repo_details['commit_count'] = len(commits)
            repo_details['recent_commits'] = commits

            # Contributors
            contributors = self.get_contributors(repo_name)
            repo_details['contributor_count'] = len(contributors)
            repo_details['contributors'] = contributors

            # Check for CI/CD
            contents = self.get_repository_content(repo_name)
            repo_details['has_ci'] = any(
                item['name'] == '.github' for item in contents
            )

            # Check for tests
            repo_details['has_tests'] = any(
                'test' in item['name'].lower() for item in contents
            )

            # Calculate maturity
            maturity = self.analyze_repository_maturity(repo_name, repo_details)
            repo_details['maturity'] = maturity

            repository_data.append(repo_details)

        # Aggregate statistics
        total_commits = sum(r['commit_count'] for r in repository_data)
        total_stars = sum(r['stars'] for r in repository_data)
        total_forks = sum(r['forks'] for r in repository_data)

        # Language aggregation
        all_languages = {}
        for repo in repository_data:
            for lang, bytes_count in repo['languages'].items():
                all_languages[lang] = all_languages.get(lang, 0) + bytes_count

        return {
            'organization': org_info,
            'repositories': repository_data,
            'summary': {
                'total_repositories': len(repository_data),
                'total_commits': total_commits,
                'total_stars': total_stars,
                'total_forks': total_forks,
                'languages': all_languages,
                'last_updated': datetime.now().isoformat()
            }
        }

    def save_data(self, data: Dict, filepath: str):
        """Save fetched data to JSON file"""
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"Data saved to {filepath}")


def main():
    """Main execution"""
    import yaml

    # Load configuration
    with open('config.yml', 'r') as f:
        config = yaml.safe_load(f)

    org_name = config['organization']
    token = os.getenv(config['github_token_env'])

    if not token:
        print(f"Warning: No GitHub token found in {config['github_token_env']} environment variable")
        print("API rate limits will be restricted to 60 requests/hour")

    # Fetch data
    fetcher = GitHubDataFetcher(org_name, token)
    data = fetcher.fetch_all_data()

    # Save data
    output_file = config['output']['data_file']
    fetcher.save_data(data, output_file)

    print(f"\nData fetch complete!")
    print(f"Repositories: {data['summary']['total_repositories']}")
    print(f"Total commits: {data['summary']['total_commits']}")
    print(f"Total stars: {data['summary']['total_stars']}")


if __name__ == '__main__':
    main()
