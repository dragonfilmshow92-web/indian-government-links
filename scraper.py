import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

start_urls = [
    "https://www.india.gov.in",
    "https://www.nic.in",
    "https://data.gov.in",
]

allowed_domains = [".gov.in", ".nic.in"]

visited = set()
collected_links = set()

def collect_links(url):
    try:
        print("Scanning:", url)
        r = requests.get(url, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")

        for a in soup.find_all("a", href=True):
            link = urljoin(url, a['href'])
            if any(dom in link for dom in allowed_domains):
                collected_links.add(link)
                if link not in visited:
                    visited.add(link)
                    collect_links(link)
    except:
        pass

for url in start_urls:
    collect_links(url)

with open("gov_links.txt", "w", encoding="utf-8") as f:
    for link in sorted(collected_links):
        f.write(link + "\n")

print("Total links:", len(collected_links))
