#!/usr/bin/env python3
"""
Interactive Quiz Generator
==========================

Generates interactive HTML quiz players from questions.json files.

Features:
- 3-column layout with rolling question replacement
- Manual "Next" button for user-controlled pace
- KaTeX math rendering (LaTeX syntax: $...$)
- Immediate feedback with explanations
- Score tracking and results screen
- Mobile responsive (3 -> 2 -> 1 columns)
- No server required (static HTML)

Usage:
------
# Generate single quiz
python generate_quiz.py --input 01_introduction/questions.json --output quiz/quiz1.html

# Generate all quizzes from a course
python generate_quiz.py --all --course-dir . --output-dir quiz

# Custom configuration
python generate_quiz.py --input questions.json --output quiz.html --title "My Quiz" --accent "#8b5cf6"

Questions JSON Format:
----------------------
[
    {
        "id": 1,
        "question": "What is 2+2?",
        "options": {"A": "3", "B": "4", "C": "5", "D": "6"},
        "correct": "B",
        "explanation": "2+2 equals 4 by basic arithmetic."
    },
    ...
]

Math Support:
-------------
Use LaTeX syntax in questions/options/explanations:
- Inline: $\\mu$, $\\sigma^2$, $\\bar{x}$
- Display: $$E[X] = \\sum x \\cdot P(x)$$
"""

import json
import argparse
from pathlib import Path
from typing import Optional
import re


# =============================================================================
# HTML TEMPLATE
# =============================================================================

QUIZ_TEMPLATE = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} | {course_name}</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.css">
    <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.js"></script>
    <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/contrib/auto-render.min.js"></script>
    <style>
        :root {{
            --mlpurple: {color_primary};
            --mlblue: {color_secondary};
            --quiz-accent: {color_accent};
            --quiz-light: {color_accent_light};
            --correct: #22c55e;
            --correct-bg: #dcfce7;
            --incorrect: #ef4444;
            --incorrect-bg: #fee2e2;
            --bg: #f6f8fa;
            --card-bg: #ffffff;
            --text: #24292e;
            --text-secondary: #586069;
            --border: #e1e4e8;
        }}

        * {{ box-sizing: border-box; margin: 0; padding: 0; }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif;
            background: var(--bg);
            color: var(--text);
            line-height: 1.4;
            min-height: 100vh;
        }}

        .nav {{
            background: linear-gradient(135deg, var(--mlpurple), var(--mlblue));
            color: white;
            padding: 8px 16px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        .nav-title {{ font-weight: 600; font-size: 14px; }}
        .nav-links {{ display: flex; gap: 16px; }}
        .nav-links a {{ color: white; text-decoration: none; font-size: 12px; opacity: 0.9; }}
        .nav-links a:hover {{ opacity: 1; }}

        .quiz-container {{
            max-width: 1400px;
            margin: 0 auto;
            padding: 12px;
        }}

        .quiz-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 12px;
            padding: 0 4px;
        }}
        .quiz-title {{ font-size: 16px; font-weight: 600; color: var(--mlpurple); }}
        .quiz-stats {{
            display: flex;
            gap: 12px;
            font-size: 12px;
        }}
        .stat-badge {{
            padding: 4px 10px;
            border-radius: 12px;
            font-weight: 600;
        }}
        .stat-progress {{ background: var(--quiz-light); color: var(--quiz-accent); }}
        .stat-score {{ background: var(--correct-bg); color: var(--correct); }}

        .progress-bar-container {{
            height: 4px;
            background: var(--border);
            border-radius: 2px;
            margin-bottom: 12px;
        }}
        .progress-bar {{
            height: 100%;
            background: var(--quiz-accent);
            border-radius: 2px;
            transition: width 0.3s;
        }}

        /* Three-column layout */
        .questions-row {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 12px;
        }}

        .question-card {{
            background: var(--card-bg);
            border-radius: 8px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            padding: 12px;
            display: flex;
            flex-direction: column;
            transition: all 0.3s ease;
            min-height: 280px;
        }}

        .question-card.answered {{ opacity: 0.7; }}

        .question-card.correct-card {{
            border: 2px solid var(--correct);
            background: linear-gradient(to bottom, var(--correct-bg), var(--card-bg));
        }}

        .question-card.incorrect-card {{
            border: 2px solid var(--incorrect);
            background: linear-gradient(to bottom, var(--incorrect-bg), var(--card-bg));
        }}

        .q-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 8px;
        }}

        .q-number {{
            background: var(--quiz-light);
            color: var(--quiz-accent);
            padding: 2px 8px;
            border-radius: 10px;
            font-size: 10px;
            font-weight: 600;
        }}

        .q-status {{ font-size: 14px; }}

        .q-text {{
            font-size: 13px;
            font-weight: 500;
            margin-bottom: 10px;
            line-height: 1.4;
            flex-grow: 0;
        }}

        .options {{
            display: flex;
            flex-direction: column;
            gap: 6px;
            flex-grow: 1;
        }}

        .option-btn {{
            display: flex;
            align-items: center;
            gap: 8px;
            padding: 10px 12px;
            min-height: 44px;
            border: 1px solid var(--border);
            border-radius: 6px;
            background: var(--card-bg);
            cursor: pointer;
            transition: all 0.15s;
            text-align: left;
            font-size: 12px;
        }}

        .option-btn:hover:not(.disabled) {{
            border-color: var(--quiz-accent);
            background: var(--quiz-light);
        }}

        .option-btn.correct {{
            border-color: var(--correct);
            background: var(--correct-bg);
        }}

        .option-btn.incorrect {{
            border-color: var(--incorrect);
            background: var(--incorrect-bg);
        }}

        .option-btn.disabled {{ cursor: default; }}

        .option-letter {{
            width: 20px;
            height: 20px;
            border-radius: 50%;
            background: var(--border);
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 600;
            font-size: 10px;
            flex-shrink: 0;
        }}

        .option-btn.correct .option-letter {{
            background: var(--correct);
            color: white;
        }}

        .option-btn.incorrect .option-letter {{
            background: var(--incorrect);
            color: white;
        }}

        .option-text {{ flex: 1; }}

        .feedback {{
            margin-top: 8px;
            padding: 8px;
            border-radius: 6px;
            font-size: 10px;
            line-height: 1.4;
            display: none;
        }}

        .feedback.show {{ display: block; }}
        .feedback.correct {{ background: var(--correct-bg); color: #166534; }}
        .feedback.incorrect {{ background: var(--incorrect-bg); color: #991b1b; }}

        /* Results */
        .results-card {{
            background: var(--card-bg);
            border-radius: 10px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            padding: 32px;
            text-align: center;
            max-width: 500px;
            margin: 40px auto;
            display: none;
        }}
        .results-card.show {{ display: block; }}
        .results-icon {{ font-size: 48px; margin-bottom: 8px; }}
        .results-score {{ font-size: 36px; font-weight: 700; color: var(--quiz-accent); }}
        .results-label {{ font-size: 14px; color: var(--text-secondary); margin-bottom: 16px; }}
        .results-grade {{
            display: inline-block;
            padding: 6px 16px;
            border-radius: 16px;
            font-size: 13px;
            font-weight: 600;
            margin-bottom: 20px;
        }}
        .grade-a {{ background: #dcfce7; color: #166534; }}
        .grade-b {{ background: #dbeafe; color: #1e40af; }}
        .grade-c {{ background: #fef3c7; color: #92400e; }}
        .grade-d {{ background: #fed7aa; color: #9a3412; }}
        .grade-f {{ background: #fee2e2; color: #991b1b; }}

        .results-buttons {{ display: flex; gap: 12px; justify-content: center; flex-wrap: wrap; }}
        .btn {{
            padding: 8px 16px;
            border-radius: 6px;
            font-size: 12px;
            font-weight: 500;
            cursor: pointer;
            border: none;
            text-decoration: none;
        }}
        .btn-primary {{ background: var(--quiz-accent); color: white; }}
        .btn-primary:hover {{ background: #7c3aed; }}
        .btn-secondary {{ background: var(--card-bg); color: var(--text); border: 1px solid var(--border); }}

        /* Next button container */
        .next-btn-container {{
            display: flex;
            justify-content: center;
            margin-top: 16px;
        }}
        .btn-next {{
            padding: 10px 32px;
            border-radius: 8px;
            font-size: 14px;
            font-weight: 600;
            cursor: pointer;
            border: none;
            background: var(--quiz-accent);
            color: white;
            transition: all 0.2s;
            display: none;
        }}
        .btn-next:hover {{ background: #7c3aed; transform: scale(1.02); }}
        .btn-next.show {{ display: inline-block; }}
        .btn-next:disabled {{ opacity: 0.5; cursor: not-allowed; }}

        @media (max-width: 900px) {{
            .questions-row {{ grid-template-columns: repeat(2, 1fr); }}
        }}
        @media (max-width: 600px) {{
            .questions-row {{ grid-template-columns: 1fr; }}
            .question-card {{ min-height: auto; }}
        }}
    </style>
</head>
<body>
    <nav class="nav">
        <div class="nav-title">{nav_title}</div>
        <div class="nav-links">
            <a href="{dashboard_url}">Dashboard</a>
            {pdf_link}
            <a href="{github_url}" target="_blank">GitHub</a>
        </div>
    </nav>

    <main class="quiz-container">
        <div class="quiz-header">
            <div class="quiz-title">{quiz_subtitle}</div>
            <div class="quiz-stats">
                <span class="stat-badge stat-progress" id="progressBadge">0/{total_questions}</span>
                <span class="stat-badge stat-score" id="scoreBadge">Score: 0</span>
            </div>
        </div>

        <div class="progress-bar-container">
            <div class="progress-bar" id="progressBar" style="width: 0%"></div>
        </div>

        <div class="questions-row" id="questionsRow"></div>

        <div class="next-btn-container">
            <button class="btn-next" id="nextBtn" onclick="loadNextQuestions()">Next</button>
        </div>

        <div class="results-card" id="resultsCard">
            <div class="results-icon" id="resultsIcon"></div>
            <div class="results-score" id="resultsScore"></div>
            <div class="results-label">Correct Answers</div>
            <div class="results-grade" id="resultsGrade"></div>
            <div class="results-buttons">
                <button class="btn btn-primary" onclick="restartQuiz()">Try Again</button>
                <a href="{dashboard_url}" class="btn btn-secondary">Dashboard</a>
            </div>
        </div>
    </main>

    <script>
        const quizData = {{
            questions: {questions_json}
        }};

        const state = {{
            currentIndex: 0,
            answers: {{}},
            score: 0,
            displayedQuestions: [],
            pendingSlots: []
        }};

        const questionsRow = document.getElementById('questionsRow');
        const progressBar = document.getElementById('progressBar');
        const progressBadge = document.getElementById('progressBadge');
        const scoreBadge = document.getElementById('scoreBadge');
        const resultsCard = document.getElementById('resultsCard');
        const nextBtn = document.getElementById('nextBtn');

        function initQuiz() {{
            state.currentIndex = 0;
            state.answers = {{}};
            state.score = 0;
            state.displayedQuestions = [];
            state.pendingSlots = [];

            resultsCard.classList.remove('show');
            questionsRow.style.display = 'grid';
            nextBtn.classList.remove('show');

            // Show first 3 questions
            for (let i = 0; i < 3 && i < quizData.questions.length; i++) {{
                state.displayedQuestions.push(i);
            }}
            state.currentIndex = Math.min(3, quizData.questions.length);

            renderQuestions();
            updateStats();
        }}

        function renderQuestions() {{
            questionsRow.innerHTML = '';

            state.displayedQuestions.forEach((qIdx, slot) => {{
                const q = quizData.questions[qIdx];
                const answered = state.answers[q.id] !== undefined;
                const isCorrect = answered && state.answers[q.id] === q.correct;
                const isIncorrect = answered && state.answers[q.id] !== q.correct;

                const card = document.createElement('div');
                card.className = 'question-card';
                if (isCorrect) card.classList.add('correct-card', 'answered');
                if (isIncorrect) card.classList.add('incorrect-card', 'answered');

                card.innerHTML = `
                    <div class="q-header">
                        <span class="q-number">Q${{qIdx + 1}}</span>
                        ${{answered ? `<span class="q-status">${{isCorrect ? '&#10004;' : '&#10008;'}}</span>` : ''}}
                    </div>
                    <div class="q-text">${{q.question}}</div>
                    <div class="options" data-qid="${{q.id}}" data-slot="${{slot}}">
                        ${{['A','B','C','D'].map(letter => {{
                            let optClass = 'option-btn';
                            if (answered) {{
                                optClass += ' disabled';
                                if (letter === q.correct) optClass += ' correct';
                                else if (letter === state.answers[q.id]) optClass += ' incorrect';
                            }}
                            return `
                                <button class="${{optClass}}" data-letter="${{letter}}" ${{answered ? 'disabled' : ''}}>
                                    <span class="option-letter">${{letter}}</span>
                                    <span class="option-text">${{q.options[letter]}}</span>
                                </button>
                            `;
                        }}).join('')}}
                    </div>
                    <div class="feedback ${{answered ? 'show' : ''}} ${{isCorrect ? 'correct' : 'incorrect'}}">
                        ${{answered ? (isCorrect ? '&#10004; ' : `&#10008; Answer: ${{q.correct}}. `) + q.explanation : ''}}
                    </div>
                `;

                // Add click handlers
                if (!answered) {{
                    card.querySelectorAll('.option-btn').forEach(btn => {{
                        btn.addEventListener('click', () => handleAnswer(qIdx, slot, btn.dataset.letter));
                    }});
                }}

                questionsRow.appendChild(card);
            }});

            renderMath();
        }}

        function handleAnswer(qIdx, slot, letter) {{
            const q = quizData.questions[qIdx];
            state.answers[q.id] = letter;

            if (letter === q.correct) state.score++;

            // Track this slot as pending replacement
            if (!state.pendingSlots.includes(slot)) {{
                state.pendingSlots.push(slot);
            }}

            updateStats();
            renderQuestions();

            // Check if all questions answered
            const answered = Object.keys(state.answers).length;
            if (answered >= quizData.questions.length) {{
                // Short delay then show results
                setTimeout(showResults, 800);
            }} else if (state.currentIndex < quizData.questions.length && state.pendingSlots.length > 0) {{
                // Show Next button if there are more questions and pending slots
                nextBtn.classList.add('show');
            }}
        }}

        function loadNextQuestions() {{
            // Replace pending slots with new questions
            while (state.pendingSlots.length > 0 && state.currentIndex < quizData.questions.length) {{
                const slot = state.pendingSlots.shift();
                state.displayedQuestions[slot] = state.currentIndex;
                state.currentIndex++;
            }}

            // Hide Next button
            nextBtn.classList.remove('show');

            renderQuestions();

            // Check if quiz is complete (all displayed questions answered)
            const answered = Object.keys(state.answers).length;
            if (answered >= quizData.questions.length) {{
                setTimeout(showResults, 500);
            }}
        }}

        function updateStats() {{
            const answered = Object.keys(state.answers).length;
            const total = quizData.questions.length;

            progressBar.style.width = `${{(answered / total) * 100}}%`;
            progressBadge.textContent = `${{answered}}/${{total}}`;
            scoreBadge.textContent = `Score: ${{state.score}}`;
        }}

        function showResults() {{
            questionsRow.style.display = 'none';
            nextBtn.classList.remove('show');
            resultsCard.classList.add('show');

            const total = quizData.questions.length;
            const percentage = Math.round((state.score / total) * 100);

            document.getElementById('resultsScore').textContent = `${{state.score}}/${{total}}`;

            let grade, gradeClass, icon;
            if (percentage >= 90) {{ grade = 'Excellent! A'; gradeClass = 'grade-a'; icon = '&#127942;'; }}
            else if (percentage >= 80) {{ grade = 'Great! B'; gradeClass = 'grade-b'; icon = '&#11088;'; }}
            else if (percentage >= 70) {{ grade = 'Good! C'; gradeClass = 'grade-c'; icon = '&#128077;'; }}
            else if (percentage >= 60) {{ grade = 'Pass - D'; gradeClass = 'grade-d'; icon = '&#128221;'; }}
            else {{ grade = 'Keep practicing'; gradeClass = 'grade-f'; icon = '&#128218;'; }}

            document.getElementById('resultsIcon').innerHTML = icon;
            const gradeEl = document.getElementById('resultsGrade');
            gradeEl.textContent = `${{grade}} (${{percentage}}%)`;
            gradeEl.className = `results-grade ${{gradeClass}}`;
        }}

        function restartQuiz() {{
            initQuiz();
        }}

        function renderMath() {{
            if (typeof renderMathInElement !== 'undefined') {{
                renderMathInElement(document.body, {{
                    delimiters: [
                        {{left: '$$', right: '$$', display: true}},
                        {{left: '$', right: '$', display: false}}
                    ],
                    throwOnError: false
                }});
            }}
        }}

        document.addEventListener('DOMContentLoaded', () => {{
            initQuiz();
            setTimeout(renderMath, 100);
        }});
    </script>
</body>
</html>
'''


# =============================================================================
# QUIZ GENERATOR CLASS
# =============================================================================

class QuizGenerator:
    """Generate interactive HTML quizzes from questions.json files."""

    def __init__(
        self,
        course_name: str = "Digital Finance & Economics",
        color_primary: str = "#3333B2",
        color_secondary: str = "#0066CC",
        color_accent: str = "#8b5cf6",
        color_accent_light: str = "#ede9fe",
        dashboard_url: str = "../index.html",
        github_url: str = "https://github.com/Digital-AI-Finance/digital-finance-economics"
    ):
        self.course_name = course_name
        self.color_primary = color_primary
        self.color_secondary = color_secondary
        self.color_accent = color_accent
        self.color_accent_light = color_accent_light
        self.dashboard_url = dashboard_url
        self.github_url = github_url

    def load_questions(self, json_path: Path) -> list:
        """Load questions from JSON file.

        Supports two formats:
        1. Direct list: [{"id": 1, ...}, ...]
        2. Wrapped object: {"questions": [...], "title": "..."}
        """
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Handle wrapped format
        if isinstance(data, dict) and 'questions' in data:
            questions = data['questions']
        else:
            questions = data

        # Ensure each question has an id
        for i, q in enumerate(questions):
            if 'id' not in q:
                q['id'] = i + 1

        return questions

    def generate_quiz(
        self,
        questions: list,
        title: str,
        subtitle: str,
        output_path: Path,
        pdf_url: Optional[str] = None,
        nav_title: Optional[str] = None
    ) -> Path:
        """Generate an interactive quiz HTML file."""

        # Format questions as JSON string
        questions_json = json.dumps(questions, ensure_ascii=False, indent=16)

        # PDF link HTML
        pdf_link = f'<a href="{pdf_url}">PDF</a>' if pdf_url else ''

        # Generate HTML
        html = QUIZ_TEMPLATE.format(
            title=title,
            course_name=self.course_name,
            color_primary=self.color_primary,
            color_secondary=self.color_secondary,
            color_accent=self.color_accent,
            color_accent_light=self.color_accent_light,
            nav_title=nav_title or title,
            dashboard_url=self.dashboard_url,
            pdf_link=pdf_link,
            github_url=self.github_url,
            quiz_subtitle=subtitle,
            total_questions=len(questions),
            questions_json=questions_json
        )

        # Write output
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)

        return output_path

    def generate_from_json(
        self,
        json_path: Path,
        output_path: Path,
        title: Optional[str] = None,
        subtitle: Optional[str] = None,
        pdf_url: Optional[str] = None
    ) -> Path:
        """Generate quiz from a questions.json file."""

        questions = self.load_questions(json_path)

        # Auto-generate title from path if not provided
        if not title:
            # Extract from folder name: 01_introduction -> Quiz 1: Introduction
            folder_name = json_path.parent.name
            match = re.match(r'(\d+)_(.+)', folder_name)
            if match:
                num, name = match.groups()
                title = f"Quiz {int(num)}: {name.replace('_', ' ').title()}"
            else:
                title = f"Quiz: {folder_name.replace('_', ' ').title()}"

        if not subtitle:
            subtitle = title

        return self.generate_quiz(
            questions=questions,
            title=title,
            subtitle=subtitle,
            output_path=output_path,
            pdf_url=pdf_url,
            nav_title=title
        )


# =============================================================================
# BATCH GENERATION
# =============================================================================

def find_question_files(course_dir: Path) -> list:
    """Find all questions.json files in a course directory."""
    question_files = []

    # Pattern: LXX_topic_name/questions.json
    for folder in sorted(course_dir.iterdir()):
        if folder.is_dir() and re.match(r'L(\d{2})_', folder.name):
            json_path = folder / 'questions.json'
            if json_path.exists():
                question_files.append(json_path)

    return question_files


def generate_all_quizzes(
    course_dir: Path,
    output_dir: Path,
    generator: QuizGenerator
) -> list:
    """Generate all quizzes for a course."""

    question_files = find_question_files(course_dir)
    generated = []

    for json_path in question_files:
        # Determine output path: quiz/quiz1.html, quiz/quiz2.html, etc.
        folder_name = json_path.parent.name
        match = re.match(r'L(\d{2})_', folder_name)
        if match:
            num = int(match.group(1))
            output_path = output_dir / f'quiz{num}.html'
        else:
            output_path = output_dir / f'{folder_name}_quiz.html'

        # Find PDF if exists
        pdf_candidates = list(json_path.parent.glob('*_quiz.pdf'))
        pdf_url = f"../{pdf_candidates[0].relative_to(course_dir)}" if pdf_candidates else None

        generator.generate_from_json(
            json_path=json_path,
            output_path=output_path,
            pdf_url=pdf_url
        )

        generated.append(output_path)
        print(f"Generated: {output_path}")

    return generated


# =============================================================================
# CLI
# =============================================================================

def main():
    parser = argparse.ArgumentParser(
        description='Generate interactive HTML quizzes from questions.json files',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  # Generate single quiz
  python generate_quiz.py -i 01_introduction/questions.json -o quiz/quiz1.html

  # Generate all quizzes
  python generate_quiz.py --all -d . -O quiz

  # Custom styling
  python generate_quiz.py -i questions.json -o quiz.html --accent "#10b981"
        '''
    )

    # Input/Output
    parser.add_argument('-i', '--input', type=Path, help='Input questions.json file')
    parser.add_argument('-o', '--output', type=Path, help='Output HTML file')
    parser.add_argument('--all', action='store_true', help='Generate all quizzes in course')
    parser.add_argument('-d', '--course-dir', type=Path, default=Path('.'), help='Course directory (for --all)')
    parser.add_argument('-O', '--output-dir', type=Path, default=Path('quiz'), help='Output directory (for --all)')

    # Customization
    parser.add_argument('--title', type=str, help='Quiz title')
    parser.add_argument('--subtitle', type=str, help='Quiz subtitle')
    parser.add_argument('--course', type=str, default='Digital Finance & Economics', help='Course name')
    parser.add_argument('--accent', type=str, default='#8b5cf6', help='Accent color (hex)')
    parser.add_argument('--primary', type=str, default='#3333B2', help='Primary color (hex)')
    parser.add_argument('--secondary', type=str, default='#0066CC', help='Secondary color (hex)')
    parser.add_argument('--dashboard', type=str, default='../index.html', help='Dashboard URL')
    parser.add_argument('--github', type=str, default='https://github.com/Digital-AI-Finance/digital-finance-economics', help='GitHub URL')
    parser.add_argument('--pdf', type=str, help='PDF quiz URL')

    args = parser.parse_args()

    # Create generator
    generator = QuizGenerator(
        course_name=args.course,
        color_primary=args.primary,
        color_secondary=args.secondary,
        color_accent=args.accent,
        dashboard_url=args.dashboard,
        github_url=args.github
    )

    if args.all:
        # Generate all quizzes
        generated = generate_all_quizzes(
            course_dir=args.course_dir,
            output_dir=args.output_dir,
            generator=generator
        )
        print(f"\nGenerated {len(generated)} quizzes")

    elif args.input and args.output:
        # Generate single quiz
        output = generator.generate_from_json(
            json_path=args.input,
            output_path=args.output,
            title=args.title,
            subtitle=args.subtitle,
            pdf_url=args.pdf
        )
        print(f"Generated: {output}")

    else:
        parser.print_help()
        return 1

    return 0


if __name__ == '__main__':
    exit(main())
