import time
import os  # Import the os module.
from dotenv import load_dotenv  # Import load_dotenv function from dotenv module.

from utility import get_sec, get_new_unix_timestamp
from browser_starter import init_browser

import discord  # discord bot imports

# Loads the .env file that resides on the same level as the script.
load_dotenv()
# Grab the API token from the .env file.
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
DEFAULT_CHANNEL = os.getenv("DEFAULT_CHANNEL")  # TODO: look for better way to add a list of servers to post to.
intents = discord.Intents.default()
bot = discord.Client(intents=intents)

urlString = 'https://www.light.gg'
vendors = ['banshee', 'xurv2']


def check_vendor(vendor_name, html_data):
    output_string = ""
    try:
        vendor_list = html_data.find('ul', {'class': vendor_name.lower()})

        list_of_s_tiers = vendor_list.find_all('img', {'class': 'pop-rank', 'alt': 'Very Popular (S)'})

        if len(list_of_s_tiers) != 0:

            display_name = "Xur" if vendor_name == "xurv2" else vendor_name.title()

            output_text = f"{display_name} is selling the following S-tiers:\n"
            print(output_text)
            output_string += output_text

            for S_tier in list_of_s_tiers:
                parent = S_tier.parent
                link = parent['href']
                item_name = parent.find('img')['alt']

                time_left = parent.parent.parent.find('li', {"class": "countdown"}).find("span").text
                time_left_sec = get_sec(time_left)  # convert to seconds
                true_time = get_new_unix_timestamp(time_left_sec)  # add to unix timestamp
                remaining_ts = f"<t:{true_time}:R>"  # read on the timestamp flag here:
                # https://gist.github.com/LeviSnoot/d9147767abeef2f770e9ddcd91eb85aa

                output_text = f"> {item_name} @ <{urlString}{link}> rerolling:{remaining_ts}\n"
                print(output_text)
                output_string += output_text
        else:
            print(f"{vendor_name} is not selling S tiers.")
    except AttributeError:
        print(f"{vendor_name} not available")

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
    rounded_time = round(end - start, 2)
    print(f"bot took {rounded_time}s to retrieve info")


bot.run(DISCORD_TOKEN)
