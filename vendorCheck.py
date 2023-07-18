# scraper imports
import time
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

# discord bot imports
import discord
# Import the os module.
import os
# Import load_dotenv function from dotenv module.
from dotenv import load_dotenv

# Loads the .env file that resides on the same level as the script.
load_dotenv()
# Grab the API token from the .env file.
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
DEFAULT_CHANNEL = os.getenv("DEFAULT_CHANNEL")
intents = discord.Intents.default()
bot = discord.Client(intents=intents)

urlString = 'https://www.light.gg'
vendors = ['banshee', 'xurv2']


def init_browser(url_string):
    # start by defining the options
    options = webdriver.ChromeOptions()
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/87.0.4280.88 Safari/537.36")
    chrome_path = ChromeDriverManager().install()
    chrome_service = Service(chrome_path)
    # pass the defined options and service objects to initialize the web driver
    driver = Chrome(options=options, service=chrome_service)
    driver.get(url_string)
    time.sleep(5)
    html = driver.page_source
    driver.quit()
    soup = BeautifulSoup(html, features="html.parser")
    return soup


def check_vendor(vendor_name, html_data):
    output_string = ""
    vendor_list = html_data.find('ul', {'class': vendor_name.lower()})
    list_of_s_tiers = vendor_list.find_all('img', {'class': 'pop-rank', 'alt': 'Very Popular (S)'})

    if len(list_of_s_tiers) != 0:

        if vendor_name == "xurv2":
            display_name = "Xur"
        else:
            display_name = vendor_name.title()

        output_string += display_name + " is selling the following S-tiers: \n"
        for S_tier in list_of_s_tiers:
            parent = S_tier.parent
            link = parent['href']
            item_name = parent.find('img')['alt']
            output_string += "> " + item_name + " @ <" + urlString + link + ">\n"

    return output_string


@bot.event
async def on_ready():
    print(f"Retrieving data from {urlString}...")
    start = time.time()
    session = init_browser(urlString)
    msg = ""
    for vendor in vendors:
        msg += check_vendor(vendor, session)

    if len(msg) != 0:
        await bot.get_channel(int(DEFAULT_CHANNEL)).send("@here\n" + msg)

    end = time.time()
    rounded_time = round(end-start, 2)
    print(f"bot took {rounded_time}s to retrieve info")

bot.run(DISCORD_TOKEN)
