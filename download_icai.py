import requests
from bs4 import BeautifulSoup

url = "https://www.icai.org/post/sm-foundation-p1-may2026"

html = requests.get(url).text
soup = BeautifulSoup(html, "html.parser")

for a in soup.find_all("a", href=True):
    print(a.get_text(strip=True), "=>", a["href"])