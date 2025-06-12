def save_to_csv(data, filename):
    """Uloží data do CSV"""
    import pandas as pd
    import csv

    df = pd.DataFrame(data)
    df.to_csv(filename, index=False, quoting=csv.QUOTE_ALL)
    print(f"✅ Uloženo do {filename}")

def save_to_json(data, filename):
    """Uloží data do JSON"""
    import json

    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"✅ Uloženo do {filename}")

def save_to_html(data, filename):
    """Uloží data do HTML tabulky se stylem a interaktivitou"""
    import pandas as pd
    df = pd.DataFrame(data)
    html_table = df.to_html(index=False, escape=False, classes="display", table_id="quotesTable", border=0)

    styled_html = (
        "<!DOCTYPE html>\n"
        "<html lang=\"en\">\n"
        "<head>\n"
        "    <meta charset=\"UTF-8\">\n"
        "    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">\n"
        "    <title>Quotes Table</title>\n"
        "    <link href=\"https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap\" rel=\"stylesheet\">\n"
        "    <link rel=\"stylesheet\" href=\"https://cdn.datatables.net/1.13.6/css/jquery.dataTables.min.css\">\n"
        "    <style>\n"
        "        body {\n"
        "            font-family: 'Inter', sans-serif;\n"
        "            padding: 20px;\n"
        "            background-color: #f0f1f9;\n"
        "            color: #333;\n"
        "        }\n"
        "        h2 {\n"
        "            color: #2c3e50;\n"
        "        }\n"
        "        table.display {\n"
        "            width: 100%;\n"
        "            border-collapse: collapse;\n"
        "        }\n"
        "        th, td {\n"
        "            padding: 12px 15px;\n"
        "            border: 1px solid #ccc;\n"
        "            text-align: left;\n"
        "        }\n"
        "        thead {\n"
        "            background-color: #2980b9;\n"
        "            color: white;\n"
        "        }\n"
        "        tbody tr:nth-child(even) {\n"
        "            background-color: #ecf0f1;\n"
        "        }\n"
        "        tbody tr:hover {\n"
        "            background-color: #d0e4f5;\n"
        "        }\n"
        "        @media (max-width: 768px) {\n"
        "            table, thead, tbody, th, td, tr {\n"
        "                display: block;\n"
        "                width: 100%;\n"
        "            }\n"
        "            thead tr {\n"
        "                display: none;\n"
        "            }\n"
        "            td {\n"
        "                position: relative;\n"
        "                padding-left: 50%;\n"
        "                text-align: right;\n"
        "            }\n"
        "            td::before {\n"
        "                position: absolute;\n"
        "                left: 10px;\n"
        "                width: 45%;\n"
        "                white-space: nowrap;\n"
        "                font-weight: bold;\n"
        "                text-align: left;\n"
        "            }\n"
        "        }\n"
        "    </style>\n"
        "    <script src=\"https://code.jquery.com/jquery-3.7.0.min.js\"></script>\n"
        "    <script src=\"https://cdn.datatables.net/1.13.6/js/jquery.dataTables.min.js\"></script>\n"
        "    <script>\n"
        "        document.addEventListener(\"DOMContentLoaded\", function() {\n"
        "            $('#quotesTable').DataTable();\n"
        "        });\n"
        "    </script>\n"
        "</head>\n"
        "<body>\n"
        "    <div style=\"display: flex; align-items: center; gap: 16px; margin-bottom: 20px;\">\n"
        "      <img src=\"FAE54386-6232-41A3-A077-7AA2292B9E48.png\" alt=\"Logo\" style=\"height: 48px;\">\n"
        "      <h1 style=\"margin: 0;\">Quotes Table (Interactive)</h1>\n"
        "    </div>\n"
        # "    <h2>Quotes Table (Interactive)</h2>\n"
        f"{html_table}\n"
        "</body>\n"
        "</html>"
    )

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(styled_html)
    print(f"✅ Uloženo jako HTML do {filename}")

def get_quotes_from_page(url):
    import requests
    from bs4 import BeautifulSoup

    response = requests.get(url)
    if response.status_code != 200:
        print(f"❌ Chyba při načítání: {url}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    quotes = soup.find_all('div', class_='quote')

    results = []
    for quote in quotes:
        text = quote.find('span', class_='text').get_text(strip=True)
        author = quote.find('small', class_='author').get_text(strip=True)
        tags = [tag.get_text(strip=True) for tag in quote.select('.tags a.tag')]
        results.append({
            'Quote': text,
            'Author': author,
            'Tags': tags
        })

    return results

def main():
    print("📢 Spouštím scraper...")
    import argparse

    parser = argparse.ArgumentParser(description='Scraper citátů z quotes.toscrape.com')
    parser.add_argument('--pages', type=int, default=5, help='Počet stránek ke stažení (default: 5)')
    parser.add_argument('--output', choices=['csv', 'json', 'html'], default='csv', help='Formát výstupu (csv, json nebo html)')
    args = parser.parse_args()

    base_url = "http://quotes.toscrape.com/page/{}/"
    all_quotes = []

    for page in range(1, args.pages + 1):
        url = base_url.format(page)
        print(f"🔄 Načítám stránku {page}...")
        page_quotes = get_quotes_from_page(url)

        if not page_quotes:
            print("⚠️ Žádné citáty – ukončuji.")
            break

        all_quotes.extend(page_quotes)

    if args.output == 'csv':
        save_to_csv(all_quotes, 'quotes.csv')
    elif args.output == 'json':
        save_to_json(all_quotes, 'quotes.json')
    elif args.output == 'html':
        save_to_html(all_quotes, 'quotes.html')
    else:
        print("❌ Neznámý formát. Použij csv, json nebo html.")

if __name__ == '__main__':
    main()