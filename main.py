import requests as rq
import pandas as pd
import urllib.parse as up
import time
import re
import httpx

from fake_useragent import UserAgent as ua

# add selenium
from selenium import webdriver
from selenium.webdriver import ChromeOptions

session = rq.session()
header = {
    "User-Agent": ua().random
}

session.headers.update(header)


def getHTML(url):
    options = ChromeOptions()
    # options.add_argument("--headless")

    driver = webdriver.Chrome()
    driver.maximize_window()

    driver.get(url)
    print("opening...")

    html = driver.page_source

    driver.close()

    return html



def readData(filename):
    df = pd.read_csv(filename)

    df['url'] = df[['NAMA', 'ALAMAT', 'KABUPATEN/KOTA']].apply(lambda row: ' '.join(row.dropna().astype(str)), axis=1)

    df['url'] = df['url'].apply(lambda x: "https://www.google.com/search?q=" + up.quote_plus(x) )

    return df

def extractPhone(text):
    pattern = r'\b\d{4}-\d{4}-\d{4}\b'

    match = re.search(pattern, text)

    if match:
        return match.group().replace("-", "")
    else:
        return "-"

def getPhone(url):
    response = session.get(url)

    responseCode = response.status_code

    print(f"{responseCode}: {url}")

    if responseCode != 200:
        return "???"
    
    html = response.text

    phone = extractPhone(html)

    print(f"phone: {phone}")

    return phone

def googleSearch(filename, start, end):
    df = readData(filename)

    df = df.iloc[start:end]

    for index, row in df.iterrows():
        phone = getPhone(row['url'])
        df.at[index, 'phone'] = phone

        print(f"{index} done")


    df.to_csv(f"{filename.replace('.csv', '')}_updategmaps{start}-{end}.csv", index=False)

    print(f"finished for {start}-{end}")

if __name__ == "__main__":
    url = "https://www.google.com/search?q=anu"
    # url = "https://www.google.com/"
    chec = session.get(url, headers={"User-Agent": ua().random})

    print(chec.status_code)
    print(chec.request.headers)

