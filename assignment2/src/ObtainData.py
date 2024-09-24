import requests
from bs4 import BeautifulSoup as bs

# Define the function to obtain data from HKTide
def obtainData(url = "https://www.hko.gov.hk/tide/KCTtextPH2024_uc.htm"):
    response = requests.get(url)

    content = response.text
    soup = bs(content, "html.parser")

    tideData = []
    tides = soup.findAll("td")
    for tide in tides:
        tideValue = tide.string
        if tideValue != None and tideValue[0] == " ":
            tideData.append(float(tideValue.strip()))
    return tideData


