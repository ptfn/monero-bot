import os
import csv
import time
import logging
import datetime
import requests
import schedule

token = os.getenv('TOKEN')
url = "https://mastodon.online/api/v1/statuses"


def get_date():
    today = datetime.date.today()
    return '{}.{}.{}'.format(today.day, today.month, today.year)


def monero_write_csv():
    csv_data = []
    csv_wfile = open("monero.csv", "a")
    csv_rfile = open("monero.csv", "r")

    csvwriter = csv.writer(csv_wfile)
    csvreader = csv.reader(csv_rfile)

    for row in csvreader:
        csv_data.append(row)

    if csv_data == []:
        csvwriter.writerow(["Date", "Price", "Low", "High",
                            "Height", "Hashrate", "Difficulty"])

    price, low, high, height, hashrate, difficulty = monero_requests()

    csvwriter.writerow([get_date(), price, low, high,
                        height, hashrate, difficulty])

    csv_wfile.close()
    csv_rfile.close()


def monero_requests():
    r = requests.get("https://moneroblocks.info/api/get_stats")
    q = requests.get("https://api.bitfinex.com/v1/pubticker/xmrusd")
    s = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=monero&vs_currencies=usd")

    dr = r.json()
    dq = q.json()
    ds = s.json()

    low = dq["low"]
    high = dq["high"]
    height = dr["height"]
    hashrate = dr["hashrate"]
    price = ds["monero"]["usd"]
    difficulty = dr["difficulty"]

    return price, low, high, height, hashrate, difficulty


def mastodon_request():
    price, low, high, height, hashrate, difficulty = monero_requests()
    string = f"Price = {price}$\nLow Price = {low} $\n\
High Price = {high} $\nHeight = {height}\n\
Hashrate = {round(hashrate / 1000**3, 2)} Gh/s\n\
Difficulty = {round(difficulty / 1000**3, 2)} G\n\n\
#monero #xmr #coin #cryptocurrency"

    headers = {"Authorization": "Bearer " + token}
    body = {"status": string}
    r = requests.post(url, headers=headers, json=body, timeout=60)


def main():
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        filename='monero-bot.log',
        filemode='w',
        level=logging.DEBUG,
    )
    schedule.every().day.at("18:00").do(mastodon_request)
    schedule.every().day.at("18:00").do(monero_write_csv)

    while True:
        try:
            schedule.run_pending()

        except Exception as e:
            logging.error(f"Request Error! {e}")

        finally:
            time.sleep(30)


if __name__ == "__main__":
    main()
