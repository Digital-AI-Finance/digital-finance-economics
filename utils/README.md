# Utility Scripts

This directory contains helper scripts for managing and generating course content.

## Scripts Overview

| Script | Purpose | Status |
|--------|---------|--------|
| `check_links.py` | Validate all links in HTML files | Main tool |
| `generate_quiz.py` | Generate interactive HTML quizzes from JSON | Main tool |
| `run_all_charts.py` | Execute all chart generation scripts | Main tool |

---

## check_links.py

Validates all links in your GitHub Pages site. Checks local file references, fragment anchors, and optionally external URLs.

### Features

- **Local file validation**: Ensures referenced files exist
- **Fragment anchor checking**: Verifies `#anchor` links point to valid `id` attributes
- **External URL checking** (optional): HTTP status validation with caching
- **CDN detection**: Automatically skips CDN links when not explicitly checking external
- **Colored output**: Easy-to-read terminal results with color support
- **Verbose mode**: Show all links (not just broken ones)

### Usage

```bash
# Fast check (local files only)
python check_links.py

# From specific directory
python check_links.py --base-path /path/to/repo

# Include external URLs (requires: pip install requests)
python check_links.py --check-external

# Verbose output (show all links)
python check_links.py -v

# Combined
python check_links.py --base-path . --check-external -v

# No colored output (for CI/CD logs)
python check_links.py --no-color
```

### Exit Codes

| Code | Meaning |
|------|---------|
| 0 | All links valid ✓ |
| 1 | One or more broken links found ✗ |
| 2 | Script error (invalid arguments, file not found, etc.) |

### Output Example

```
Link Checker - Base: /path/to/repo
External checks: disabled

Checking: index.html
  [OK] quiz/quiz1.html
  [OK] #introduction
  [BROKEN] old_file.html
    Source: index.html:45
    Error: File not found: old_file.html

Checking: quiz/quiz1.html
  [OK] ../index.html
  [OK] #results
  ...

============================================================
LINK CHECK SUMMARY
============================================================
Files checked:  2
Total links:    15
  Valid:        13
  Broken:       1
  Skipped:      1
============================================================

FAILED: 1 broken link(s) found
```

### What Gets Checked

**Local links** (relative paths):
```html
<a href="quiz/quiz1.html">Quiz 1</a>        <!-- checked -->
<img src="../images/chart.png">             <!-- checked -->
<link href="styles.css">                    <!-- checked -->
```

**Fragment links** (anchors on same page):
```html
<a href="#section">Go to section</a>        <!-- checks for id="section" -->
```

**External links** (with `--check-external`):
```html
<a href="https://example.com">Link</a>      <!-- HTTP status check -->
```

**Skipped links** (always ignored):
```html
<a href="mailto:email@example.com">Email</a>
<a href="tel:+1234567890">Call</a>
<a href="javascript:void(0)">Script</a>
```

### Implementation Details

- **LinkExtractor**: Parses HTML and extracts all links from `<a>`, `<img>`, `<link>`, `<script>` tags
- **LocalFileChecker**: Resolves relative paths and checks file existence
- **FragmentChecker**: Extracts `id` attributes and validates anchors (with caching)
- **ExternalChecker**: HTTP HEAD requests with caching and timeout handling

---

## generate_quiz.py

Generates interactive HTML quizzes from JSON question files. Creates beautiful, responsive quiz interfaces with score tracking and instant feedback.

### Features

- **3-column responsive layout**: Auto-scales to 2 columns (900px) and 1 column (600px)
- **Manual pacing**: Users control when to see next questions
- **Math support**: LaTeX rendering with KaTeX ($...$)
- **Instant feedback**: Shows correct/incorrect with explanations after each answer
- **Score tracking**: Live progress bar and score badge
- **Results screen**: Final grade with emoji and performance evaluation
- **Mobile responsive**: Works on all screen sizes
- **No server required**: Pure static HTML (runs offline)

### Usage

#### Generate Single Quiz

```bash
# Basic
python generate_quiz.py --input L01_Introduction/questions.json \
                        --output quiz/quiz1.html

# With custom title and PDF link
python generate_quiz.py --input L01_Introduction/questions.json \
                        --output quiz/quiz1.html \
                        --title "Quiz 1: Introduction to Digital Finance" \
                        --pdf "L01_Introduction/lecture_1_quiz.pdf"
```

#### Generate All Quizzes

```bash
# Generate all quizzes from current directory
python generate_quiz.py --all --course-dir . --output-dir quiz

# From specific course directory
python generate_quiz.py --all --course-dir /path/to/course --output-dir /path/to/course/quiz
```

#### Custom Styling

```bash
# Custom colors
python generate_quiz.py --input questions.json \
                        --output quiz.html \
                        --accent "#10b981" \
                        --primary "#1e40af" \
                        --secondary "#3b82f6"

# Change course name and links
python generate_quiz.py --input questions.json \
                        --output quiz.html \
                        --course "My Course Name" \
                        --dashboard "../index.html" \
                        --github "https://github.com/user/repo"
```

### Questions JSON Format

```json
[
    {
        "id": 1,
        "question": "What is the main purpose of a CBDC?",
        "options": {
            "A": "To replace commercial banks entirely",
            "B": "To provide a digital form of central bank money",
            "C": "To increase inflation",
            "D": "To eliminate cryptocurrency"
        },
        "correct": "B",
        "explanation": "CBDCs are designed as digital versions of fiat currency issued by central banks, providing a secure digital payment option."
    },
    {
        "id": 2,
        "question": "Calculate: $2 + 2 = ?$",
        "options": {
            "A": "$3$",
            "B": "$4$",
            "C": "$5$",
            "D": "$6$"
        },
        "correct": "B",
        "explanation": "Basic arithmetic: $2 + 2 = 4$"
    }
]
```

**Required fields:**
- `id`: Unique question number
- `question`: Question text (supports LaTeX)
- `options`: Object with keys A, B, C, D
- `correct`: Letter of correct answer (A, B, C, or D)
- `explanation`: Feedback shown after answer (supports LaTeX)

**Optional fields:**
- None (all required)

### Math Support (LaTeX)

Use standard LaTeX syntax with `$` delimiters:

```markdown
# Inline math
The expected value is $E[X] = \sum x \cdot P(x)$

# Display math (larger)
Optimization problem:
$$\max_{w} w^T \mu - \frac{\lambda}{2} w^T \Sigma w$$

# Greek letters
The volatility $\sigma$ measures risk.
Correlation coefficient: $\rho_{xy}$
The mean return: $\bar{r}$
```

### Workflow: Batch Generation

Course structure:
```
L01_Introduction/
    questions.json
    lecture_1_quiz.pdf
L02_Monetary_Economics/
    questions.json
    lecture_2_quiz.pdf
L03_CBDCs/
    questions.json
    ...
quiz/  (generated)
    quiz1.html
    quiz2.html
    quiz3.html
```

Generate all at once:
```bash
python generate_quiz.py --all
```

This automatically:
1. Finds all `LXX_*/questions.json` files
2. Matches PDF files by pattern (`*_quiz.pdf`)
3. Generates `quiz/quizXX.html` with correct numbering
4. Uses folder names to auto-generate titles

### Generated Quiz Features

**User Experience:**
- 3 questions displayed at a time
- User clicks an option to answer
- Immediate visual feedback (green/red)
- Explanation shown below answer
- "Next" button appears to continue
- When all questions answered → results screen

**Results Screen:**
- Shows score: X/N correct
- Grade: A (90%+), B (80%+), C (70%+), D (60%+), F (<60%)
- Emoji reaction (🏆, ⭐, 👍, 📝, 📖)
- Buttons to restart or return to dashboard

### Implementation Details

- **QuizGenerator class**: Main API for converting JSON → HTML
- **QUIZ_TEMPLATE**: Embedded HTML/CSS/JavaScript template
- **batch generation**: Auto-finds lesson folders with regex `L\d{2}_`
- **KaTeX rendering**: Client-side math with deferred loading
- **State management**: JavaScript tracks progress, answers, score

---

## run_all_charts.py

Finds and executes all chart generation scripts across lesson directories. Verifies that both PDF and PNG outputs are created successfully.

### Features

- **Batch execution**: Runs all `chart.py` scripts in lesson folders
- **Parallel mode**: Execute multiple charts simultaneously (default: 4 workers)
- **Output verification**: Checks that `chart.pdf` and `chart.png` are created
- **Error reporting**: Clear failure messages with timeouts and error details
- **Exit codes**: Proper CI/CD integration (0 = all success, 1 = failures)

### Usage

#### Sequential (Default)

```bash
# Run all charts one at a time
python run_all_charts.py
```

Output:
```
Searching for charts in: /path/to/course
Found 8 chart files

Running sequentially...

Running: L01_Introduction/charts/chart.py... OK
Running: L02_Monetary_Economics/charts/chart.py... OK
Running: L03_CBDCs/assets/chart.py... FAIL
  Error: Timeout (>60s)
Running: L04_Payment_Systems/charts/chart.py... OK
...

============================================================
SUMMARY
============================================================
Total charts: 8
Successful:   7
Failed:       1

Failed charts:
  - L03_CBDCs/assets/chart.py: Timeout (>60s)
```

#### Parallel Execution

```bash
# Run with 4 workers (default)
python run_all_charts.py --parallel

# Run with 8 workers
python run_all_charts.py --parallel --workers 8

# Shorthand
python run_all_charts.py -p -w 8
```

Output:
```
Searching for charts in: /path/to/course
Found 8 chart files

Running in parallel with 4 workers...

[OK] L01_Introduction/charts/chart.py
[OK] L02_Monetary_Economics/charts/chart.py
[FAIL] L03_CBDCs/assets/chart.py
       Error: Timeout (>60s)
[OK] L04_Payment_Systems/charts/chart.py
...
```

### Exit Codes

| Code | Meaning |
|------|---------|
| 0 | All charts generated successfully ✓ |
| 1 | One or more charts failed ✗ |

### What Gets Checked

Searches for chart scripts using pattern:
```
L*/*/chart.py
```

Examples:
```
L01_Introduction/charts/chart.py         ✓ matched
L02_Monetary_Economics/visualization/chart.py  ✓ matched
L03_CBDCs/assets/chart.py                ✓ matched
L01_Introduction/chart.py                ✗ not matched (wrong depth)
L01_Introduction/data.py                 ✗ not matched (wrong name)
```

### Chart Script Requirements

For a chart script to be recognized and executed:

1. **Location**: `L*/*/chart.py` (at least 2 directory levels)
2. **Outputs**: Must create `chart.pdf` and `chart.png` in same directory
3. **Runtime**: Should complete within 60 seconds
4. **Exit code**: Should return 0 on success

Example valid chart script:
```python
#!/usr/bin/env python3
import matplotlib.pyplot as plt
from pathlib import Path

# Generate chart
fig, ax = plt.subplots()
ax.plot([1,2,3], [1,4,9])
ax.set_title("Chart Title")

# Save outputs (REQUIRED)
output_dir = Path(__file__).parent
fig.savefig(output_dir / "chart.pdf")
fig.savefig(output_dir / "chart.png")
plt.close()

print("Chart generated successfully")
```

### Performance Tuning

**When to use parallel:**
- 8+ chart files
- Charts take >5 seconds each
- Machine has 4+ CPU cores

**When to use sequential:**
- <5 chart files
- Charts very fast (<1 second)
- Memory constrained
- Debugging individual charts

**Performance expectations:**
| Mode | 8 Charts @10s each | 16 Charts @5s each |
|------|--------------------|--------------------|
| Sequential | ~80s | ~80s |
| Parallel (4 workers) | ~20s | ~20s |
| Parallel (8 workers) | ~10s | ~10s |

### Implementation Details

- **find_all_charts()**: Glob-based discovery with sorting
- **run_chart()**: Subprocess execution with cwd isolation
- **Output verification**: Checks for exact file existence
- **ThreadPoolExecutor**: Thread-based parallelism (I/O bound)
- **Timeout handling**: 60-second per-chart limit
- **Error collection**: Captures stderr for debugging

---

## Common Workflows

### Before Publishing Site

```bash
# 1. Generate all quizzes
python generate_quiz.py --all

# 2. Generate all charts
python run_all_charts.py --parallel

# 3. Validate all links
python check_links.py --check-external

echo "All checks passed! Ready to publish."
```

### Quick Development Check

```bash
# Fast local validation only
python check_links.py

# No external checks needed during development
```

### CI/CD Integration

```bash
# .github/workflows/validate.yml
- name: Generate quizzes
  run: cd utils && python generate_quiz.py --all

- name: Generate charts
  run: cd utils && python run_all_charts.py

- name: Validate links
  run: cd utils && python check_links.py --check-external
```

### Troubleshooting

**Q: "No HTML files found" (check_links.py)**
A: Ensure you're running from the repo root or specify `--base-path`

**Q: Charts timeout (run_all_charts.py)**
A: Use sequential mode to debug: `python run_all_charts.py`
   Then investigate specific `L*/*/chart.py` file

**Q: KaTeX math not rendering (generate_quiz.py)**
A: Ensure `$...$` delimiters are used, not `\(...\)`
   Check browser console for KaTeX errors

**Q: "requests library not installed"**
A: Install with: `pip install requests`
   Or run without external checks: `python check_links.py`

---

## Requirements

### Python Version
- Python 3.7+

### Dependencies

| Script | Required | Optional |
|--------|----------|----------|
| check_links.py | `pathlib`, `argparse`, `html.parser` (stdlib) | `requests` (for `--check-external`) |
| generate_quiz.py | `json`, `pathlib`, `argparse`, `re` (stdlib) | None |
| run_all_charts.py | `subprocess`, `pathlib`, `argparse`, `concurrent.futures` (stdlib) | None |

### Optional Installation

```bash
# For external link checking
pip install requests
```

---

## File Formats

### Input: questions.json

```json
[
    {
        "id": 1,
        "question": "Question text here?",
        "options": {"A": "Option A", "B": "Option B", "C": "Option C", "D": "Option D"},
        "correct": "B",
        "explanation": "Why B is correct."
    }
]
```

### Output: quiz/quizN.html

Self-contained interactive quiz (no server required)

### Output: L*/*/chart.pdf, chart.png

Generated by `chart.py` scripts, verified by `run_all_charts.py`

---

## License

These utilities are part of the Digital Finance & Economics course materials.
