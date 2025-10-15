from flask import Flask, jsonify, request
import subprocess
import os
import json

app = Flask(__name__)

# ---------- CONFIG ----------
OUTPUT_DIR = "output"
PARSED_FILE = os.path.join(OUTPUT_DIR, "parsed_data.json")
RESULTS_FILE = os.path.join(OUTPUT_DIR, "results.json")

# ---------- UTILITIES ----------

def run_scraper(args):
    """
    Run ecourts_scraper.py using subprocess with the given arguments.
    Returns True if successful, False otherwise.
    """
    try:
        cmd = ["python", "ecourts_scraper.py"] + args
        print(f"[INFO] Running: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
        print(result.stdout)
        if result.returncode == 0:
            return True
        else:
            print(result.stderr)
            return False
    except Exception as e:
        print(f"[ERROR] Scraper failed: {e}")
        return False


def load_json(file_path):
    """Safely load JSON file if it exists."""
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


# ---------- ROUTES ----------

@app.route("/")
def home():
    return jsonify({
        "message": "Welcome to eCourts Scraper API 🏛️",
        "routes": {
            "/causelist": "Scrape and fetch today's cause list (supports ?state=Karnataka&day=today|tomorrow)",
            "/cnr/<cnr_number>": "Fetch case details by CNR number",
            "/results": "Get last scraped cause list data",
            "/parsed": "View parsed court and serial details from PDFs"
        }
    })


@app.route("/causelist", methods=["GET"])
def cause_list():
    """Scrape eCourts cause lists by state and date."""
    state = request.args.get("state", "Karnataka")
    day = request.args.get("day", "today")

    args = [f"--{day}", "--state", state]
    success = run_scraper(args)

    if not success:
        return jsonify({"error": "Failed to fetch cause list"}), 500

    parsed_data = load_json(PARSED_FILE)
    return jsonify({
        "message": f"Cause list fetched and parsed for {state} ({day})",
        "total_records": len(parsed_data),
        "sample": parsed_data[:5]  # only first 5 entries
    })


@app.route("/cnr/<cnr_number>", methods=["GET"])
def case_by_cnr(cnr_number):
    """Fetch case details by CNR number."""
    success = run_scraper(["--cnr", cnr_number])
    if not success:
        return jsonify({"error": "Failed to fetch case details"}), 500

    # After running, read last lookup result from output/results.json if available
    data = load_json(RESULTS_FILE)
    return jsonify({
        "message": f"Case details fetched for CNR: {cnr_number}",
        "details": data if data else "No structured data found. Check console output."
    })


@app.route("/results", methods=["GET"])
def view_results():
    """Return the last scraped results.json."""
    data = load_json(RESULTS_FILE)
    if not data:
        return jsonify({"message": "No results found yet"}), 404
    return jsonify({"total": len(data), "data": data})


@app.route("/parsed", methods=["GET"])
def view_parsed():
    """Return parsed serial numbers and court names."""
    parsed = load_json(PARSED_FILE)
    if not parsed:
        return jsonify({"message": "No parsed data found"}), 404
    return jsonify({"total": len(parsed), "parsed_data": parsed})


# ---------- BONUS IDEA ----------
# Add this route for scheduling automation (future-ready)
@app.route("/auto", methods=["GET"])
def auto_schedule():
    """
    Example route to trigger automated scraping daily (can integrate with cron/schedule library).
    """
    return jsonify({
        "message": "Auto-scheduling endpoint placeholder",
        "tip": "Use 'schedule' Python library or Windows Task Scheduler to run daily scrape at 9 AM."
    })


# ---------- MAIN ----------

if __name__ == "__main__":
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    app.run(host="0.0.0.0", port=5000, debug=True)
