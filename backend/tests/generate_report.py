import json
from html import escape
from pathlib import Path

results_path = Path(__file__).resolve().parent / "test-results.json"
output_path = Path(__file__).resolve().parent / "api-test-report.html"

if not results_path.exists():
    raise SystemExit("No test results found. Run pytest first.")

results = json.loads(results_path.read_text())
passed = sum(1 for item in results if item["outcome"] == "passed")
failed = sum(1 for item in results if item["outcome"] == "failed")

rows = "".join(
    f"<tr><td>{escape(item['nodeid'])}</td><td>{escape(item['outcome'])}</td><td>{item['duration']}</td></tr>"
    for item in results
)

html = f"""<!doctype html>
<html lang=\"en\">
<head>
  <meta charset=\"utf-8\" />
  <title>API Test Report</title>
  <style>
    body {{ font-family: Arial, sans-serif; margin: 2rem; }}
    .summary {{ display: flex; gap: 1rem; margin-bottom: 1rem; }}
    .card {{ border: 1px solid #ddd; padding: 1rem; border-radius: 8px; }}
    table {{ border-collapse: collapse; width: 100%; }}
    th, td {{ border: 1px solid #ddd; padding: 0.6rem; text-align: left; }}
    th {{ background: #f5f5f5; }}
    .pass {{ color: green; font-weight: bold; }}
    .fail {{ color: red; font-weight: bold; }}
  </style>
</head>
<body>
  <h1>API Test Report</h1>
  <div class=\"summary\">
    <div class=\"card\">Passed: <strong>{passed}</strong></div>
    <div class=\"card\">Failed: <strong>{failed}</strong></div>
    <div class=\"card\">Total: <strong>{len(results)}</strong></div>
  </div>
  <table>
    <thead><tr><th>Test</th><th>Status</th><th>Duration (s)</th></tr></thead>
    <tbody>{rows}</tbody>
  </table>
</body>
</html>
"""

output_path.write_text(html)
print(f"Report written to {output_path}")
