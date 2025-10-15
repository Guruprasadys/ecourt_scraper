eCourts Cause List Scraper: 
A Python-based scraper to extract cause list information from eCourts PDFs. It parses court serial numbers, court names, and other case details, storing them in JSON format. 

Features: 
Fetch cause lists for today or tomorrow. 
Parse PDFs to extract serial numbers and court names. 
Lookup case details using CNR number. 
Save parsed data as parsed_data.json. 
CLI options for flexible usage. 
Ready for future automation to download PDFs automatically. 

Project Structure: 
ecourt_scraper/ 
│ 
├─ ecourts_scraper.py # Main Python script 
├─ output/ 
│ ├─ pdfs/ # Folder for storing cause list PDFs 
│ └─ parsed_data.json # Parsed JSON output 
├─ requirements.txt # Required Python packages 
└─ README.md # Project documentation 

Setup Instructions: 
1.Clone or Download the Project 
git clone <your-github-repo-link> 
cd ecourt_scraper 
2.Install Python (3.10+ recommended) 
Check Python version: 
python --version 
3.Install Dependencies 
Create a virtual environment (optional but recommended): 
python -m venv venv 
venv\Scripts\activate # Windows 
source venv/bin/activate # macOS/Linux 

Install required packages: 
pip install -r requirements.txt 

requirements.txt should contain: 
PyMuPDF 
tqdm 
No Selenium or requests_html is required in the latest version. 
Prepare PDFs 
Download cause list PDFs for the date you want from eCourts

Place them inside the folder: 
output/pdfs/ 

Example: 
output/pdfs/cause_list_2025-10-15.pdf 
Running the Scraper: 
1.Parse today’s PDFs: 
python ecourts_scraper.py --today 
2.Parse tomorrow’s PDFs: 
python ecourts_scraper.py --tomorrow 
3.Lookup a case by CNR number: 
python ecourts_scraper.py --cnr <CNR_NUMBER> 

Output: 
All parsed results will be saved as: 
output/parsed_data.json 
Example JSON entry: 
{ 
"serial": "1", 
"court": "Court No. 3 - CIVIL COURT", 
"details": "1. John Doe vs. XYZ Corp ..." 
} 

Tips: 
Place all PDFs you want to parse in output/pdfs/. 
Filenames are flexible; the scraper reads all PDFs in the folder. 
Use --cnr to quickly lookup individual cases without parsing PDFs. 

