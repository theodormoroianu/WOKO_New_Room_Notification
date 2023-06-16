# WOKO New Room Notifier

_Python script sending push notifications whenever a new room is published on the WOKO (student asociation for housing in Zurich) website._

## What this Script Does

This script continuously fetches the WOKO website for rooms available in Zurich. Whenever a new room is available, the script sends a push notification to phones properly set-up (in a subscriber / publisher fashion).

Assuming you already have an available VM on the cloud (if you don't get one ASAP), deploying this script requires ~5 mins.

## Running the Script

Steps for running the script locally are:

1. Install `bs4` and `lxml` with `pip3 install bs4 lxml` or `pip3 install -r requirements.txt`.
2. Install the push-notification app companion, [**Ntfy.sh**](https://ntfy.sh/). The Android app is [here](https://play.google.com/store/apps/details?id=io.heckel.ntfy).
3. Open the **Ntfy.sh** app, and add subscribe to the topic "_cazare_woko_" (or whatever string is at the top of [scraper.py](./scraper.py)).
4. Run the `scraper.py` file, with `python3 scraper.py`.
5. ???
6. Enjoy

## Running the script on the cloud

I highly recommend running the script on a cloud VM. This ensures the script runs 100% of the time.

As it's really tiny, any VM will work, including the free ones given by AWS or Oracle Cloud (I ran this script on an Oracle Cloud instance with one CPU and 1GB of RAM). The steps to do so are:

1. Create the VM.
2. Copy the scraper.py file to the VM by running `scp scraper.py ubuntu@[YOUR VM IP]:/home/ubuntu/scraper.py`.
3. SSH into the VM.
4. Install `bs4` and `lxml` by running `pip3 install bs4 lxml`.
4. Open a `TMUX` shell. This ensures the script keeps running even after closing the terminal: `tmux new -s "scraper"`.
5. Run the scraper: `python3 scraper.py`.
6. Exit from the tmux shell, by either closing the terminal, or pressing `CTRL+B` followed by `D`. DO NOT type `exit`, as it will terminate the shell.
7. For attaching back to the TMUX shell, simply type in the SSH window `tmux attach -t "scraper"`.