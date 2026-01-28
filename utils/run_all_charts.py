#!/usr/bin/env python3
"""Run all chart generation scripts and verify outputs.

Usage:
    python utils/run_all_charts.py
    python utils/run_all_charts.py --parallel  # Run in parallel
"""
import subprocess
import sys
from pathlib import Path
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed

def find_all_charts(base_dir: Path) -> list[Path]:
    """Find all chart.py files in lesson directories."""
    # Pattern: L*/*/chart.py
    charts = sorted(base_dir.glob("L*/*/chart.py"))
    return charts

def run_chart(chart_path: Path) -> dict:
    """Run a single chart.py and verify outputs."""
    chart_dir = chart_path.parent
    result = {
        "path": str(chart_path),
        "success": False,
        "pdf_exists": False,
        "png_exists": False,
        "error": None
    }

    try:
        # Run the chart script
        proc = subprocess.run(
            [sys.executable, str(chart_path)],
            cwd=str(chart_dir),
            capture_output=True,
            text=True,
            timeout=60
        )

        if proc.returncode != 0:
            result["error"] = proc.stderr[:500] if proc.stderr else "Unknown error"
            return result

        # Check outputs exist
        pdf_path = chart_dir / "chart.pdf"
        png_path = chart_dir / "chart.png"

        result["pdf_exists"] = pdf_path.exists()
        result["png_exists"] = png_path.exists()
        result["success"] = result["pdf_exists"] and result["png_exists"]

        if not result["success"]:
            missing = []
            if not result["pdf_exists"]:
                missing.append("PDF")
            if not result["png_exists"]:
                missing.append("PNG")
            result["error"] = f"Missing outputs: {', '.join(missing)}"

    except subprocess.TimeoutExpired:
        result["error"] = "Timeout (>60s)"
    except Exception as e:
        result["error"] = str(e)

    return result

def main():
    parser = argparse.ArgumentParser(description="Run all chart generation scripts")
    parser.add_argument("--parallel", "-p", action="store_true", help="Run in parallel")
    parser.add_argument("--workers", "-w", type=int, default=4, help="Number of parallel workers")
    args = parser.parse_args()

    # Find base directory (parent of utils)
    base_dir = Path(__file__).parent.parent

    print(f"Searching for charts in: {base_dir}")
    charts = find_all_charts(base_dir)
    print(f"Found {len(charts)} chart files\n")

    results = []

    if args.parallel:
        print(f"Running in parallel with {args.workers} workers...\n")
        with ThreadPoolExecutor(max_workers=args.workers) as executor:
            futures = {executor.submit(run_chart, chart): chart for chart in charts}
            for future in as_completed(futures):
                result = future.result()
                results.append(result)
                status = "OK" if result["success"] else "FAIL"
                print(f"[{status}] {result['path']}")
                if result["error"]:
                    print(f"       Error: {result['error']}")
    else:
        print("Running sequentially...\n")
        for chart in charts:
            print(f"Running: {chart}...", end=" ", flush=True)
            result = run_chart(chart)
            results.append(result)
            status = "OK" if result["success"] else "FAIL"
            print(status)
            if result["error"]:
                print(f"  Error: {result['error']}")

    # Summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)

    successes = [r for r in results if r["success"]]
    failures = [r for r in results if not r["success"]]

    print(f"Total charts: {len(results)}")
    print(f"Successful:   {len(successes)}")
    print(f"Failed:       {len(failures)}")

    if failures:
        print("\nFailed charts:")
        for r in failures:
            print(f"  - {r['path']}: {r['error']}")
        sys.exit(1)
    else:
        print("\nAll charts generated successfully!")
        sys.exit(0)

if __name__ == "__main__":
    main()
