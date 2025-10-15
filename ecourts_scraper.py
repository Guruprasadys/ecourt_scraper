import os
import json
import fitz  # PyMuPDF
from datetime import datetime
import argparse

# ---------- Configuration ----------
PDF_DIR = "output/pdfs"
PARSED_FILE = "output/parsed_data.json"
os.makedirs(PDF_DIR, exist_ok=True)

# ---------- PDF Parsing Logic ----------
def parse_pdf(file_path):
    """
    Extract serial numbers and court names from a PDF file.
    """
    try:
        doc = fitz.open(file_path)
        text = ""
        for page in doc:
            text += page.get_text("text")
        doc.close()

        lines = text.splitlines()
        parsed = []

        for line in lines:
            line = line.strip()
            if not line:
                continue
            # Example pattern: "1. Case Name ..." or "Court No. 3 - CIVIL COURT"
            if line.startswith(tuple(str(i) + "." for i in range(1, 101))):
                parsed.append({"serial": line.split('.')[0], "details": line})
            elif "Court" in line and ("No" in line or "Room" in line):
                parsed.append({"court": line})

        return parsed
    except Exception as e:
        print(f"[!] Failed to parse {file_path}: {e}")
        return []

# ---------- Main Parser ----------
def parse_all_pdfs():
    """
    Parse all PDFs in the PDF_DIR folder and save JSON output.
    """
    pdf_files = [os.path.join(PDF_DIR, f) for f in os.listdir(PDF_DIR) if f.lower().endswith(".pdf")]
    if not pdf_files:
        print(f"[!] No PDFs found in {PDF_DIR}. Place the cause list PDFs here.")
        return

    all_data = []
    for pdf in pdf_files:
        print(f"[+] Parsing: {pdf}")
        parsed = parse_pdf(pdf)
        all_data.append({
            "file": pdf,
            "parsed_data": parsed
        })

    # Save output JSON
    with open(PARSED_FILE, "w", encoding="utf-8") as f:
        json.dump(all_data, f, indent=2, ensure_ascii=False)

    print(f"\n✅ Parsing complete! Saved in: {PARSED_FILE}")

# ---------- CLI ----------
def main():
    parser = argparse.ArgumentParser(description="Offline eCourts PDF Parser")
    parser.add_argument("--today", action="store_true", help="Parse PDFs for today")
    parser.add_argument("--tomorrow", action="store_true", help="Parse PDFs for tomorrow")
    parser.add_argument("--cnr", type=str, help="Lookup case by CNR (optional)")
    args = parser.parse_args()

    today = datetime.now().strftime("%Y-%m-%d")
    day = "tomorrow" if args.tomorrow else "today"
    print(f"\n=== 🏛️ eCourts Scraper for {today} ({day}) ===\n")

    parse_all_pdfs()

if __name__ == "__main__":
    main()
