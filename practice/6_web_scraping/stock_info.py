"""
There is a list of most active Stocks on Yahoo Finance https://finance.yahoo.com/most-active.
You need to compose several sheets based on data about companies from this list.
To fetch data from webpage you can use requests lib. To parse html you can use beautiful soup lib or lxml.
Sheets which are needed:
1. 5 stocks with most youngest CEOs and print sheet to output. You can find CEO info in Profile tab of concrete stock.
    Sheet's fields: Name, Code, Country, Employees, CEO Name, CEO Year Born.
2. 10 stocks with best 52-Week Change. 52-Week Change placed on Statistics tab.
    Sheet's fields: Name, Code, 52-Week Change, Total Cash
3. 10 largest holds of Blackrock Inc. You can find related info on the Holders tab.
    Blackrock Inc is an investment management corporation.
    Sheet's fields: Name, Code, Shares, Date Reported, % Out, Value.
    All fields except first two should be taken from Holders tab.


Example for the first sheet (you need to use same sheet format):
==================================== 5 stocks with most youngest CEOs ===================================
| Name        | Code | Country       | Employees | CEO Name                             | CEO Year Born |
---------------------------------------------------------------------------------------------------------
| Pfizer Inc. | PFE  | United States | 78500     | Dr. Albert Bourla D.V.M., DVM, Ph.D. | 1962          |
...

About sheet format:
- sheet title should be aligned to center
- all columns should be aligned to the left
- empty line after sheet

Write at least 2 tests on your choose.
Links:
    - requests docs: https://docs.python-requests.org/en/latest/
    - beautiful soup docs: https://www.crummy.com/software/BeautifulSoup/bs4/doc/
    - lxml docs: https://lxml.de/
"""

import requests
from bs4 import BeautifulSoup
import time
import datetime
from urllib.request import urlopen

current_year = 2026
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1"
}

scraper_session = requests.Session()
scraper_session.headers.update(headers)

def get_tickers():
    url = "https://finance.yahoo.com/markets/stocks/most-active/"
    response = scraper_session.get(url, timeout=15) 
    soup = BeautifulSoup(response.content, 'lxml')

    tickers = []
    rows = soup.find_all("tr", class_ = "row yf-1og7bvd")
    for row in rows:
       name = row.find("div", class_ = "leftAlignHeader companyName yf-362rys enableMaxWidth")
       code = row.find("span", class_ = "symbol yf-1pdfbgz")
       tickers.append({
            "symbol": code.text.strip(),
            "name": name.text.strip() if name else "N/A"
           })
    return tickers


def clean_numeric(val_str):
    """Converts financial strings like '1.5B', '500M', or '+15.4%' to floats."""
    if not val_str or val_str in ["N/A", "NaN", "-"]:
        return 0.0
    val = val_str.replace('%', '').replace(',', '').replace('+', '')
    multiplier = 1
    if 'T' in val: multiplier = 1_000_000_000_000
    elif 'B' in val: multiplier = 1_000_000_000
    elif 'M' in val: multiplier = 1_000_000
    
    val = val.replace('T', '').replace('B', '').replace('M', '')
    try:
        return float(val) * multiplier
    except ValueError:
        return 0.0    


def get_stock_data(ticker_info):
    symbol = ticker_info['symbol']
    data = {**ticker_info, 
            "country": "N/A", 
            "employees": "N/A", 
            "ceo_name": "N/A", 
            "ceo_age": 0, 
            "change_52w": 0.0, 
            "total_cash": "N/A", 
            "blackrock": {}
            }
    

    #Profile_Tab
    p_url = f"https://finance.yahoo.com/quote/{symbol}/profile/"

    try:
        response = scraper_session.get(p_url, timeout=15)
        if response.status_code != 200:
            print(f"DEBUG: {symbol} | HTTP Error {response.status_code}")
            return data
        
        p_soup = BeautifulSoup(response.content, 'lxml')
        
        profile_div = p_soup.find(attrs={"data-testid": "asset-profile"})
        if profile_div:
            addr = profile_div.find("div", class_=lambda x: x and 'address' in x)
            if addr:
                divs = addr.find_all("div")
                if divs:
                    data["country"] = divs[-1].get_text(strip=True)

            emp_label = profile_div.find("dt", string=lambda t: t and "Full Time Employees" in t)
            if emp_label:
                data["employees"] = emp_label.find_next_sibling("dd").get_text(strip=True)

        
        exec_table = p_soup.find("table")
        if exec_table:
            rows = exec_table.find_all("tr")
        if len(rows) > 1:
            cols = rows[1].find_all("td")
            data["ceo_name"] = cols[0].text
            age_text = cols[4].text
            if int(age_text):
                data["ceo_age"] = current_year - int(age_text) 

    except Exception as e:
        print(f"ERROR: {symbol} | {e}")
        
    



    #Statistics Tab
    try:
        s_url = f"https://finance.yahoo.com/quote/{symbol}/key-statistics"
        s_resp = scraper_session.get(s_url, timeout=10)
        if s_resp.status_code == 200:
            s_soup = BeautifulSoup(s_resp.content, "lxml")
            for row in s_soup.find_all("tr"):
                cells = row.find_all("td")
                if len(cells) < 2: continue

                label = cells[0].get_text(strip=True)
                if "Total Cash" in label:
                    data["total_cash"] = cells[1].get_text(strip=True)
                elif "52 Week Change" in label:
                    data["change_52w"] = clean_numeric(cells[1].get_text(strip=True))
                
    except Exception as e:
        print(f"Error on Stats for {symbol}: {e}")

    

    #Holders Tab
    try:
        h_url = f"https://finance.yahoo.com/quote/{symbol}/holders"
        h_resp = scraper_session.get(h_url, timeout=10)
        if h_resp.status_code == 200:
            h_soup = BeautifulSoup(h_resp.content, "lxml")  
            for row in h_soup.find_all("tr"):
                row_text = row.get_text().lower()
                if "blackrock" in row_text:
                    cols = row.find_all("td")
                    if len(cols) >=5:
                        data["blackrock"] = {
                            "shares": cols[1].get_text(strip=True), 
                            "date_rep": cols[2].get_text(strip=True),
                            "pct_out": cols[3].get_text(strip=True), 
                            "value": clean_numeric(cols[4].get_text(strip=True)),
                        }
                        break

    except Exception as e:
        print(f"Error on Holders for {symbol}: {e}")

    return data
    
    
def print_sheet(title, headers, rows, col_widths, file = None):
    """Formats the ASCII sheet as requested."""
    print(f" {title} ".center(130, "="), file = file)
    header_str = "|"
    for i, h in enumerate(headers):
        header_str += f" {h:<{col_widths[i]}} |"
    
    print(header_str, file=file)
    print("-" * len(header_str), file=file)
    
    for row in rows:
        row_str = "|"
        for i, item in enumerate(row):
            row_str += f" {str(item):<{col_widths[i]}} |"
        print(row_str, file=file)
    print("\n", file=file)


if __name__ == "__main__":

    tickers = get_tickers()
    all_stock_data = []

    for t in tickers:
        all_stock_data.append(get_stock_data(t))
        time.sleep(2)

    with open("stock_report.txt", "w", encoding = "utf-8") as f:

        #Sheet_1
        youngest_ceo = sorted([d for d in all_stock_data if d['ceo_age'] > 0], key = lambda x: x['ceo_age'])[:5]
        rows1 = [[d['name'], d['symbol'], d['country'], d['employees'], d['ceo_name'], d['ceo_age']] for d in youngest_ceo]
        print_sheet("5 stocks with most youngest CEOs", ["Name", "Code", "Country", "Employees", "CEO Name", "CEO Year Born"], rows1, [30, 10, 15, 12, 45, 8], file=f)

        # #Sheet_2
        best_change = sorted(all_stock_data, key = lambda x: x['change_52w'], reverse = True )[:10]
        rows2 = [[d['name'], d['symbol'], f"{d['change_52w']}%", d['total_cash']] for d in best_change]
        print_sheet("10 stocks with best 52-Week Change", ["Name", "Code", "52-Week Change", "Total Cash"], rows2,[30, 10, 15, 15], file=f)

        #Sheet_3
        br_holds = [d for d in all_stock_data if d.get('blackrock') and 'value' in d['blackrock']]
        br_sorted = sorted(br_holds, key = lambda x: x['blackrock'].get('value', 0), reverse = True)[:10]
        if not br_sorted:
            print("\n[!] No BlackRock data was found for any stocks.")
        else:
            rows3 = [[d['name'], d['symbol'], d['blackrock']['shares'], d['blackrock']['date_rep'], d['blackrock']['pct_out'], d['blackrock']['value']] for d in br_sorted]
            print_sheet("10 largest holds of Blackrock Inc", ["Name", "Code", "Shares", "Date Reported", "% Out", "Value"], rows3, [30, 10, 15, 15, 15, 15], file=f)

