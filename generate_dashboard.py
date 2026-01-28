"""
Dashboard Generator
Scans lesson directories and regenerates index.html with current data.
Uses Jinja2 templating with templates/dashboard.html.j2
"""

import os
import json
import glob
from datetime import datetime
from typing import Dict, List

try:
    from jinja2 import Environment, FileSystemLoader
    HAS_JINJA2 = True
except ImportError:
    HAS_JINJA2 = False
    print("Warning: jinja2 not installed. Dashboard regeneration requires jinja2.")

import yaml


def discover_lessons(base_dir: str = ".") -> List[Dict]:
    """Scan filesystem for lesson directories and their charts"""
    lessons = []

    # Find all L##_* directories
    lesson_dirs = sorted(glob.glob(os.path.join(base_dir, "L[0-9][0-9]_*")))

    for lesson_dir in lesson_dirs:
        dirname = os.path.basename(lesson_dir)
        # Extract lesson number and name
        parts = dirname.split("_", 1)
        lesson_num = parts[0]  # e.g., "L01"
        lesson_name = parts[1].replace("_", " ") if len(parts) > 1 else ""

        # Check if .tex file exists (indicates active lesson)
        tex_files = glob.glob(os.path.join(lesson_dir, f"{dirname}.tex"))
        status = "Active" if tex_files else "Planned"

        # Find chart subdirectories
        chart_dirs = sorted(glob.glob(os.path.join(lesson_dir, "[0-9][0-9]_*")))
        charts = []
        for chart_dir in chart_dirs:
            chart_name = os.path.basename(chart_dir)
            chart_py = os.path.join(chart_dir, "chart.py")
            chart_pdf = os.path.join(chart_dir, "chart.pdf")
            charts.append({
                'name': chart_name,
                'display_name': chart_name.split("_", 1)[1].replace("_", " ").title() if "_" in chart_name else chart_name,
                'has_py': os.path.exists(chart_py),
                'has_pdf': os.path.exists(chart_pdf),
                'path': os.path.relpath(chart_dir, base_dir).replace("\\", "/")
            })

        lessons.append({
            'id': lesson_num,
            'num': lesson_num[1:],  # "01", "02", etc.
            'directory': dirname,
            'title': lesson_name.title(),
            'status': status,
            'charts': charts,
            'chart_count': len(charts)
        })

    return lessons


def assign_parts(lessons: List[Dict]) -> Dict[str, List[Dict]]:
    """Group lessons into parts"""
    parts = {
        'I': {'name': 'Foundations', 'lessons': [], 'color': '#0ea5e9'},
        'II': {'name': 'Core Economics', 'lessons': [], 'color': '#8b5cf6'},
        'III': {'name': 'Markets & Policy', 'lessons': [], 'color': '#f59e0b'}
    }

    for lesson in lessons:
        num = int(lesson['num'])
        if num <= 2:
            parts['I']['lessons'].append(lesson)
        elif num <= 5:
            parts['II']['lessons'].append(lesson)
        else:
            parts['III']['lessons'].append(lesson)

    return parts


def generate_dashboard(base_dir: str = "."):
    """Main dashboard generation"""
    # Load config
    config_path = os.path.join(base_dir, "config.yml")
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
    else:
        config = {
            'course': {
                'title': 'Digital Finance & Economics',
                'level': 'BSc',
                'duration': '45 min per session',
                'lessons': 8
            },
            'organization': 'Digital-AI-Finance',
            'repository': 'digital-finance-economics'
        }

    # Discover lessons
    lessons = discover_lessons(base_dir)
    parts = assign_parts(lessons)

    # Load repo stats if available
    stats_path = os.path.join(base_dir, "data", "repository_stats.json")
    repo_stats = {}
    if os.path.exists(stats_path):
        with open(stats_path, 'r') as f:
            repo_stats = json.load(f)

    # Compute aggregate stats
    total_charts = sum(l['chart_count'] for l in lessons)
    active_lessons = sum(1 for l in lessons if l['status'] == 'Active')

    stats = {
        'total_lessons': len(lessons),
        'active_lessons': active_lessons,
        'total_charts': total_charts,
        'last_updated': datetime.now().strftime('%Y-%m-%d')
    }

    # Generate using Jinja2 if available
    template_path = os.path.join(base_dir, "templates", "dashboard.html.j2")
    output_path = os.path.join(base_dir, "index.html")

    if HAS_JINJA2 and os.path.exists(template_path):
        env = Environment(loader=FileSystemLoader(os.path.join(base_dir, "templates")))
        template = env.get_template("dashboard.html.j2")

        html = template.render(
            config=config,
            lessons=lessons,
            parts=parts,
            stats=stats,
            repo_stats=repo_stats,
            year=datetime.now().year
        )

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)

        print(f"Dashboard generated: {output_path}")
        print(f"  Lessons: {len(lessons)} ({active_lessons} active)")
        print(f"  Charts: {total_charts}")
    else:
        print("Jinja2 template not found or jinja2 not installed.")
        print("Using existing index.html (static version).")
        if not os.path.exists(output_path):
            print("WARNING: No index.html exists!")


if __name__ == '__main__':
    generate_dashboard()
