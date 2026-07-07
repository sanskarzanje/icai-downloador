import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

URL = "https://boslive.icai.org/study_material_new_paper_details.php?c=foundation&language=English&year=Applicable+for+May+2026+Exam+Onwards"

DOWNLOAD_DIR = "CA_Foundation_Study_Material"

os.makedirs(DOWNLOAD_DIR, exist_ok=True)

headers = {
    "User-Agent": "Mozilla/5.0"
}

print("Fetching page...")

response = requests.get(URL, headers=headers)
response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")

pdf_links = []

for link in soup.find_all("a", href=True):
    href = link["href"]

    if ".pdf" in href.lower():
        pdf_url = urljoin(URL, href)
        pdf_links.append(pdf_url)

print(f"Found {len(pdf_links)} PDF files")

for pdf_url in pdf_links:
    filename = pdf_url.split("/")[-1].split("?")[0]
    filepath = os.path.join(DOWNLOAD_DIR, filename)

    if os.path.exists(filepath):
        print(f"Skipping: {filename}")
        continue

    print(f"Downloading: {filename}")

    try:
        pdf_response = requests.get(pdf_url, headers=headers, stream=True)
        pdf_response.raise_for_status()

        with open(filepath, "wb") as f:
            for chunk in pdf_response.iter_content(chunk_size=8192):
                f.write(chunk)

    except Exception as e:
        print(f"Failed: {filename}")
        print(e)

print("Done!")