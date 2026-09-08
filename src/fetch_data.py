from pathlib import Path
import re
import calendar
import time
import argparse


import requests
from bs4 import BeautifulSoup

BASE = "https://www.caa.co.uk"
HEADERS = {"User-Agent":"Mozilla/5.0"}
RAW_DIR = Path("data/raw")


def month_page_url(year:int, month:str)-> str:
    return f"{BASE}/data-and-analysis/uk-aviation-market/airports/uk-airport-data/uk-airport-data-{year}/{month}-{year}/"


def get_csv_links(page_url:str) -> list[tuple[str,str]]:

    scrap = requests.get(page_url,headers=HEADERS,timeout=30)
    scrap.raise_for_status()
    soup = BeautifulSoup(scrap.text,'html.parser')

    links = []
    for a in soup.find_all('a',href=True):
        text = a.get_text(strip=True)
        if "(CSV" in text:

            table_name = re.sub(r'\s+\(CSV.*\)',"",text)

            href = a['href']
            if href.startswith('/'):
                href = BASE + href
            links.append((table_name,href))
    return links
            

def download_file(url : str, dest : Path):
    if dest.exists():
        return 

    csv = requests.get(url,headers = HEADERS,timeout=30)
    dest.parent.mkdir(parents=True,exist_ok=True) # creates parent directory; parents creates parents directories and exist_ok does not throw an error if already exists
    dest.write_bytes(csv.content) # .content encodes the data in bytes



def run(start_year : int, end_year : int, wanted_tables :list[str], delay: float=1.0):
    for year in range(start_year,end_year+1):
        for month_num in range(1,13):
            month_name = calendar.month_name[month_num].lower()
            page_url = month_page_url(year, month_name)

            try:
                links = get_csv_links(page_url)
            except requests.HTTPError as e:
                print(f" skip {year}--{month_num:02d}: {e}")
                continue
            except requests.RequestException as e:
                print(f" network error {year}--{month_num:02d}: {e}")
                continue

            for table_name, csv_url in links:

                if wanted_tables and not any(w.lower() in table_name.lower() for w in wanted_tables):
                    continue

                safe_table = re.sub(r'[^a-zA-Z0-9]+','_',table_name)
                dest = RAW_DIR / str(year) / month_name /f"_{safe_table}.csv"

                try:
                    download_file(csv_url, dest)
                    print(f" file save: {dest}")
                except requests.RequestException as e:
                    print(f" failed {csv_url}: {e}")
                    continue

            
            time.sleep(delay)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--start-year', type=int, required=True)
    parser.add_argument('--end-year', type=int, required=True)
    parser.add_argument('--tables', default=None, nargs="*" , help="Substrings to match the name:")
    parser.add_argument('--delay', default=1.0, type=float, help="Delay between downloads")

    args = parser.parse_args()

    run(args.start_year , args.end_year , args.tables, args.delay)
