import requests
import csv
import os
from dotenv import load_dotenv

def run_stock_job():
    load_dotenv()

    POLYGON_API_KEY = os.getenv("POLYGON_API_KEY")
    print(POLYGON_API_KEY)

    LIMIT = 100
    url = f'https://api.polygon.io/v3/reference/tickers?market=stocks&active=true&order=asc&limit={LIMIT}&sort=ticker&apiKey={POLYGON_API_KEY}'
    response = requests.get(url)
    tickers = []

    data = response.json()
    for ticker in data['results']:
        tickers.append(ticker)

    while 'next_url' in data:
        print('requesting next page', data['next_url'])
        response = requests.get(data['next_url'] + f'&apiKey={POLYGON_API_KEY}')
        data = response.json()

        if 'error' in data:
            print("API Error:", data['error'])
            break

        for ticker in data['results']:
            tickers.append(ticker)

    print(len(tickers))

    example_ticker = {
        'ticker': 'BIOX',
        'name': 'Bioceres Crop Solutions Corp. Ordinary Shares',
        'market': 'stocks',
        'locale': 'us',
        'primary_exchange': 'XNAS',
        'type': 'CS',
        'active': True,
        'currency_name': 'usd',
        'cik': '0001769484',
        'last_updated_utc': '2025-09-23T06:05:27.601485969Z'
    }
    fieldnames = list(example_ticker.keys())

    rows_written = 0
    with open('tickers.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for t in tickers:
            row = {key: t.get(key, '') for key in fieldnames}
            writer.writerow(row)
            rows_written += 1

    print(f"Wrote {rows_written} rows to tickers.csv")

# Optional: Run manually if script is executed directly
if __name__ == "__main__":
    run_stock_job()
