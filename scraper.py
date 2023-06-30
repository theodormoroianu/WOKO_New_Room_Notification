import requests
from bs4 import BeautifulSoup
import bs4
import time
import sys

#######################################################
#                     PARAMETERS                      #
#######################################################

# How often to check for new rooms (in seconds).
# Setting this value too low might overload the WOKO servers,
# so please don't do that.
WAIT_TIME = 5

# How often to send a heartbeat notification, informing users that the
# script is still up and running.
HEARTBEAT_EVERY = 60 * 60 * 24

# Ntfy.sh channel used.
# This has to be the same channel (in that case "cazare_woko") as the
# one specified in the android / iOS application.
NTFY_CHANNEL = "https://ntfy.sh/cazare_woko"

# Ignores room announcements containing the string "Sublet", as they are
# most probably sublets for the summer, and not main tenant announcements.
IGNORE_SUBLET = True

#######################################################
#                  END OF PARAMETERS                  #
#######################################################


def send_notification(title, content):
    requests.post(
        NTFY_CHANNEL, data=content.encode(), headers={"Title": title.encode()}
    )


def extract_data_from_single_item(item: bs4.element.Tag):
    table_entries = item.find("table").findChildren("td")
    title = table_entries[0].text.strip()
    date = table_entries[1].text.strip()
    address = table_entries[3].text.strip()
    price = item.find("div", attrs={"class": "preis"}).text.strip()
    return title, date, address, price


listed = set()


def scrape():
    global listed
    url = "https://www.woko.ch/en/zimmer-in-zuerich"
    raw_html = requests.get(url).content.decode()
    html = BeautifulSoup(raw_html, features="lxml")

    lettings_list = html.body.find_all("div", attrs={"class": "inserat"})
    data = [extract_data_from_single_item(i) for i in lettings_list]

    if len(listed) == 0:
        for i in data:
            listed.add(i)

    for d in data:
        if d not in listed:
            listed.add(d)
            if IGNORE_SUBLET and "Sublet" in d[0]:
                continue
            send_notification(d[0] + " " + d[1], f"Price: {d[3]}, Address: {d[2]}")

    listed = set()
    for i in data:
        listed.add(i)

    return len(data)


raised_exception = False
nr_fetched, nr_failures = 0, 0
last_heatbeat = time.time()

start_message = f"Message: {sys.argv[1]}" if len(sys.argv) > 1 else ""
send_notification("Scraper Started", f"Started scraping every {WAIT_TIME}s\n{start_message}")

while True:
    nr_fetched += 1
    last_fetch_size = 0
    try:
        last_fetch_size = scrape()
    except Exception as e:
        nr_failures += 1
        # If an exception was already sent, don't spam the users.
        if raised_exception:
            print(f"Suppressed error: {e}")
            continue
        else:
            raised_exception = True
            print(f"Error: {e}")
            send_notification("ERROR", f"Failed to fetch data: {e}")

    print(
        f"Fetched for {nr_fetched} times, with {nr_failures} errors. Last fetch parsed {last_fetch_size} items."
    )

    if time.time() - last_heatbeat > HEARTBEAT_EVERY == 0:
        send_notification(
            "Heatbeat", f"Fetched {nr_fetched} times, encountered {nr_failures} errors."
        )
        last_heatbeat = time.time()
        
    time.sleep(WAIT_TIME)
