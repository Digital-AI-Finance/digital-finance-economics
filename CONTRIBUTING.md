# Contributing to Digital Finance & Economics

Thank you for your interest in contributing to this educational course! We welcome contributions from economists, educators, developers, and students who are passionate about digital finance and economics. Whether you're fixing a typo, improving content, or creating new visualizations, your contributions help make this course better for everyone.

## Types of Contributions Welcome

We appreciate contributions in many forms:

### Typo Fixes and Corrections
- Spelling and grammar corrections in slides or documentation
- Factual corrections or clarifications in course content
- Updates to outdated references or data

### Content Improvements
- Clarifications of economic concepts
- Additional examples or case studies
- Improved explanations of complex topics
- Enhanced theoretical grounding for key ideas

### New Chart Visualizations
- Additional charts to support lesson concepts
- Improved visual representations of economic models
- Interactive visualizations or animations
- Updated data visualizations

### Quiz Question Improvements
- New quiz questions for assessment
- Improved question clarity
- Better answer explanations
- Additional difficulty levels

### Documentation Enhancements
- Improvements to README, SYLLABUS, or other docs
- Better setup instructions
- Additional usage examples
- Contributions to course guides

## Development Setup

### Prerequisites
- Git
- Python 3.8+
- LaTeX distribution (for compiling slides)
- Basic familiarity with Beamer (for slide contributions)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Digital-AI-Finance/digital-finance-economics.git
   cd Digital-Finance-Economics
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install LaTeX (if needed)**

   **macOS:**
   ```bash
   brew install --cask mactex
   ```

   **Ubuntu/Debian:**
   ```bash
   sudo apt-get install texlive-full
   ```

   **Windows:**
   - Download and install [MiKTeX](https://miktex.org/download) or [TeX Live](https://www.tug.org/texlive/)

4. **Verify installation**
   ```bash
   # Test LaTeX
   pdflatex --version

   # Test Python dependencies
   python -c "import matplotlib; print('OK')"
   ```

## Pull Request Workflow

### Step 1: Create a Feature Branch
```bash
git checkout -b fix/typo-lesson-01
# or
git checkout -b feature/new-cbdc-visualization
```

Use descriptive branch names. Common prefixes:
- `fix/` - Bug fixes or typo corrections
- `feature/` - New content or visualizations
- `docs/` - Documentation improvements
- `quiz/` - Quiz question additions/improvements

### Step 2: Make Your Changes

**For LaTeX/Slides:**
- Edit `.tex` files in the appropriate lesson folder (e.g., `L01_Introduction/L01_Introduction.tex`)
- Follow the existing Beamer template structure

**For Python/Charts:**
- Place chart generation scripts in lesson subdirectories
- Follow the existing naming convention: `01_chart_name/`

**For Quiz Questions:**
- Edit or create `LXX_Topic/questions.json`
- Follow the existing JSON structure

**For Documentation:**
- Edit markdown files in the repository root

### Step 3: Test Your Changes

**For LaTeX slides:**
```bash
cd LXX_Topic/
pdflatex LXX_Topic.tex
# Verify the PDF compiles without errors
```

**For Python scripts:**
```bash
python -m pytest  # if test suite exists
# or run your script directly
python script_name.py
```

**For quiz questions:**
- Verify JSON is valid:
  ```bash
  python -m json.tool LXX_Topic/questions.json
  ```
- Check that all fields are present (question, options, correct_answer, explanation)

**For HTML/web content:**
- Test in a browser by opening `index.html`
- Verify all links work correctly

### Step 4: Commit and Push

```bash
git add .
git commit -m "Add: New AMM visualization for L06 Market Microstructure"
# or
git commit -m "Fix: Typo in L02 monetary economics definition"
```

**Commit message guidelines:**
- Use clear, descriptive messages
- Start with a verb: Add, Fix, Update, Improve, Clarify
- Reference lesson numbers (e.g., L02, L03)
- Keep first line under 50 characters when possible

```bash
git push origin fix/typo-lesson-01
```

### Step 5: Submit a Pull Request

On GitHub:
1. Go to the repository and click "New Pull Request"
2. Select your branch
3. Fill out the PR template with:
   - Clear title (same as commit message)
   - Description of changes
   - Why this change is important
   - Any relevant issue numbers
4. Submit and respond to any feedback

## Code Style Guidelines

### Python

Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/):
- Use 4-space indentation
- Maximum line length: 79 characters
- Use meaningful variable names
- Add docstrings to functions

```python
def calculate_network_effect(num_users):
    """
    Calculate Metcalfe's law network effect.

    Args:
        num_users (int): Number of network participants

    Returns:
        float: Network value proportional to n(n-1)/2
    """
    return num_users * (num_users - 1) / 2
```

### LaTeX/Beamer

- Use consistent indentation (2 or 4 spaces)
- Keep slides uncluttered with 3-5 bullet points max
- Use `\textbf{}` for emphasis, not `\emph{}`
- Include source citations for data and quotes
- Follow the existing template structure

```latex
\begin{frame}[fragile]
  \frametitle{Monetary Base vs Broad Money}
  \begin{itemize}
    \item M0: Currency in circulation
    \item M1: Cash + demand deposits
    \item M2: M1 + savings deposits
  \end{itemize}
  \footnotesize{Source: Central Bank, 2024}
\end{frame}
```

### JSON (Quiz Questions)

Use proper indentation (2 spaces):
```json
{
  "question": "What is Gresham's Law?",
  "options": [
    "Bad money drives out good",
    "Good money drives out bad",
    "Markets always clear",
    "Prices adjust instantly"
  ],
  "correct_answer": 0,
  "explanation": "Gresham's Law states that when two currencies circulate..."
}
```

### HTML/CSS

- Use semantic HTML5 elements
- Write clean, readable CSS
- Follow existing style conventions in `index.html`
- Test responsiveness on mobile devices

## File Naming Conventions

- LaTeX files: `LXX_Topic_Name/LXX_Topic_Name.tex`
- Chart folders: `LXX_Topic/NN_chart_name/` (where NN is 01, 02, etc.)
- Chart outputs: `chart.png` (preview) and `chart.pdf` (vector)
- Quiz files: `LXX_Topic/questions.json`
- Python scripts: `snake_case.py` (lowercase with underscores)

## Testing

Before submitting a pull request:

1. **Verify all changes compile/run without errors**
2. **Check for obvious typos and formatting issues**
3. **Test on different platforms if possible** (Windows, macOS, Linux)
4. **Review your own changes** before requesting review

## Getting Help

### Questions or Issues?
- Open an issue on GitHub describing your question or problem
- Provide context and examples when possible
- Be respectful and specific

### Contribution Ideas?
- Check existing issues and pull requests to avoid duplicates
- Start with small contributions to get familiar with the workflow
- Ask maintainers if you're unsure about a direction

## Code of Conduct

Contributors are expected to maintain a respectful, inclusive environment:
- Be respectful of different perspectives
- Provide constructive feedback
- Focus on improving the course quality
- Report inappropriate behavior to project maintainers

## Recognition

Contributors will be recognized in:
- The `CONTRIBUTORS.md` file (when created)
- GitHub contributor statistics
- Course materials (when appropriate)

## License

By contributing, you agree that your contributions will be licensed under the same license as the project.

---

**Thank you for contributing to Digital Finance & Economics!** Questions? Open an issue on [GitHub](https://github.com/Digital-AI-Finance/digital-finance-economics/issues).
