import requests
from bs4 import BeautifulSoup

KEYWORD = "nike"
WEBHOOK_URL = "https://discord.com/api/webhooks/1387918125776764938/jTWexWXpu8GmybHtdLFIV6PkOe8Ta0EpxeaPcH0ZbjurQYvIHy85BzIFo5akCTrbkwtg"

def scrape_vinted():
    url = f"https://www.vinted.fr/vetements?search_text={KEYWORD}"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")
    links = soup.find_all("a", href=True)
    found = []

    for link in links:
        href = link["href"]
        if href.startswith("/items/") and href not in found:
            found.append("https://www.vinted.fr" + href)

    return found

def send_to_discord(message):
    data = {"content": message}
    response = requests.post(WEBHOOK_URL, json=data)
    print(f"🟢 Discord status: {response.status_code}")

if __name__ == "__main__":
    annonces = scrape_vinted()
    if annonces:
        for a in annonces:
            send_to_discord(a)
    else:
        send_to_discord("Aucune annonce trouvée.")
