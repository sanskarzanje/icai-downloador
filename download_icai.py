import os
import requests
from bs4 import BeautifulSoup

SUBJECTS = [
    "https://www.icai.org/post/sm-foundation-p1-may2026",  # Accounts
    "https://www.icai.org/post/sm-foundation-p2-may2026",  # Law
    "https://www.icai.org/post/sm-foundation-p3-may2026",  # Quantitative Aptitude
    "https://www.icai.org/post/sm-foundation-p4-may2026",  # Economics
]

DOWNLOAD_DIR = "CA_Foundation_Study_Material"

os.makedirs(DOWNLOAD_DIR, exist_ok=True)

headers = {
    "User-Agent": "Mozilla/5.0"
}

all_pdfs = set()

print("Collecting PDF links...")

for page in SUBJECTS:
    print(f"Checking: {page}")

    html = requests.get(page, headers=headers).text
    soup = BeautifulSoup(html, "html.parser")

    for a in soup.find_all("a", href=True):
        href = a["href"]

        if "resource.cdn.icai.org" in href and href.lower().endswith(".pdf"):
            all_pdfs.add(href)

print(f"Found {len(all_pdfs)} PDFs")

for pdf_url in sorted(all_pdfs):

    filename = pdf_url.split("/")[-1]
    filepath = os.path.join(DOWNLOAD_DIR, filename)

    if os.path.exists(filepath):
        continue

    print(f"Downloading {filename}")

    try:
        response = requests.get(pdf_url, stream=True)

        with open(filepath, "wb") as f:
            for chunk in response.iter_content(8192):
                f.write(chunk)

    except Exception as e:
        print("Error:", e)

print("Done")