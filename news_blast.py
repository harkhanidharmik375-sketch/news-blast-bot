import requests
import xml.etree.ElementTree as ET
import time

TELEGRAM_BOT_TOKEN = "8947925352:AAH92xZTCpCdbzsI8KKhRhI520lEJ8ee_Bc"
TELEGRAM_CHAT_ID = "1906881906"

# 🟢 જે ન્યૂઝ સ્ટોકને રોકેટ બનાવે
SUPER_CATALYSTS = [
    "BAGS ORDER", "WINS CONTRACT", "ORDER OF", "AWARDED", "L1 BIDDER",
    "ANTI-DUMPING", "DGTR", "TARIFF", "USFDA", "EIR", "ZERO 483", 
    "APPROVAL", "DEMERGER", "SPIN OFF", "TAKEOVER", "ACQUISITION", "PATENT"
]

TRASH_BLACKLIST = [
    "LOSS OF SHARE", "DUPLICATE", "TRADING WINDOW", "RESIGNATION", 
    "POSTAL BALLOT", "CREDIT RATING", "MEETING SCHEDULE"
]

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": msg, "parse_mode": "HTML"}
    try:
        r = requests.post(url, data=payload, timeout=8)
        print(f"Telegram Delivery Status: {r.status_code}")
    except Exception as e:
        print(f"Telegram error: {e}")

def check_market_news():
    # ગૂગલ ન્યૂઝ લાઈવ RSS - આ ક્યારેય બ્લોક નહીં થાય!
    query = '("bags order" OR "secures contract" OR "wins order" OR "USFDA" OR "anti-dumping" OR "demerger") when:1d'
    rss_url = f"https://news.google.com/rss/search?q={query}&hl=en-IN&gl=IN&ceid=IN:en"
    
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    
    try:
        res = requests.get(rss_url, headers=headers, timeout=12)
        print(f"News Engine Status: {res.status_code}")
        
        if res.status_code == 200:
            root = ET.fromstring(res.content)
            items = root.findall('./channel/item')
            print(f"Successfully fetched {len(items)} live market catalysts!")
            
            # બોટ ચાલુ થયો છે તેની ખાતરી માટે ટેસ્ટ મેસેજ મોકલશે
            send_telegram("🤖 <b>News Blast Bot is LIVE!</b>\nConnected to Market Feed with 0% Block!")
            
            for item in items[:10]:
                title = item.find('title').text if item.find('title') is not None else ""
                link = item.find('link').text if item.find('link') is not None else ""
                title_upper = title.upper()

                if any(trash in title_upper for trash in TRASH_BLACKLIST):
                    continue

                if any(cat in title_upper for cat in SUPER_CATALYSTS):
                    alert_msg = (
                        f"🚨 <b>HIGH-VELOCITY BLAST NEWS!</b> 🚨\n\n"
                        f"⚡ <b>Catalyst:</b> {title}\n\n"
                        f"🔗 <a href='{link}'>Click to Read Live News</a>\n\n"
                        f"👉 <i>Check broker immediately!</i>"
                    )
                    send_telegram(alert_msg)
                    time.sleep(1)
                    break # એક રનમાં એક બેસ્ટ એલર્ટ
        else:
            send_telegram(f"⚠️ Feed error: Status {res.status_code}")
    except Exception as e:
        print(f"Error: {e}")
        send_telegram(f"⚠️ Script Error: {str(e)[:80]}")

if __name__ == "__main__":
    check_market_news()
