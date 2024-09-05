import re
import requests
import pandas

from bs4 import BeautifulSoup as bs
from bs4 import Comment



def extractPhone(text):
    soup = bs(text, "html.parser")
    comments = soup.find_all(string=lambda text: isinstance(text, Comment))

    comments = [comment for comment in comments if "fa-phone" in comment]

    if len(comments) > 1:
        print("too many page for this name")
        return "an url"
    elif len(comments) == 1:
        soup = bs(comments[0], "html.parser")
        return soup.text.replace("_", "").strip()
    else:
        return "-"

    
def getProfile(keyword):
    keyword = keyword.lower().replace(" ", "+")

    # url = f"https://yankes.kemkes.go.id/klinik/cari?propinsi=&kabkota=&jenis=&nama={keyword}"
    url = f"https://yankes.kemkes.go.id/praktekmandiri/cari?propinsi=&kabkota=&jenis=&nama={keyword}"

    html = requests.get(url).text

    phone = extractPhone(html)

    if phone == "an url":
        phone = url
    print(f"phone: {phone}")
    
    return phone

def search(filename):
    df = pandas.read_csv(filename)

    # df = df.head(23)

    for index, row in df.iterrows():
        print(row["NAMA"])
        
        phone = getProfile(row['NAMA'])
        df.at[index, 'yankes'] = phone

        print(f"{index} of {len(df)} done")

    df.to_csv(f"{filename.replace('.csv', '')}_update.csv", index=False)
    