import urllib3
import gspread
from bs4 import BeautifulSoup
from oauth2client.service_account import ServiceAccountCredentials
from config import scope
from auth import google_keyFile


def find_row_in_dataframe(query, df, type_name):
    return df[df[type_name].str.contains(query, na=False, case=False)]


def render_image(base_web, name):
    http = urllib3.PoolManager()

    url = base_web + name
    response = http.request('GET', url)

    soup = BeautifulSoup(response.data)
    web_addr = soup.find("meta", property="og:image")

    return str(web_addr["content"].rsplit('.png', 1)[0]) + ".png"


def login():
    credentials = ServiceAccountCredentials.from_json_keyfile_name(google_keyFile, scope)
    return gspread.authorize(credentials)
