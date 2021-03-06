import os
import time
import requests
import schedule


token = os.getenv('TOKEN')
url = "https://mastodon.online/api/v1/statuses"


def monero():
    r = requests.get("https://moneroblocks.info/api/get_stats")
    q = requests.get("https://api.bitfinex.com/v1/pubticker/xmrusd")
    s = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=monero&vs_currencies=usd")
    
    dr = r.json()
    dq = q.json()
    ds = s.json()

    difficulty = dr["difficulty"]
    hashrate = dr["hashrate"]
    height = dr["height"]
    low = dq["low"]
    high = dq["high"]
    price = ds["monero"]["usd"]

    return f"Price = {price}$\nLow Price = {low} $\nHigh Price = {high} $\nHeight = {height}\nHashrate = {round(hashrate / 1000**3, 2)} Gh/s\nDifficulty = {round(difficulty / 1000**3, 2)} G\n\n#monero #xmr #coin #cryptocurrency"


def request(monero):
    headers = {"Authorization": "Bearer " + token}
    body = {"status": monero()}
    r = requests.post(url, headers = headers, json = body, timeout = 60)


def main():
    schedule.every().day.at("18:00").do(request, monero)

    while True:
        try:
            schedule.run_pending()
        
        except:
            print("--Request Error!--")
        
        else:
            print("--Request Ok!--")
        
        finally:
            time.sleep(15)


if __name__ == "__main__":
    main()