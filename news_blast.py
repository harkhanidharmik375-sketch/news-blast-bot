import requests
import json
from datetime import datetime
import time

TELEGRAM_BOT_TOKEN = "8947925352:AAH92xZTCpCdbzsI8KKhRhI520lEJ8ee_Bc"
TELEGRAM_CHAT_ID = "1906881906"

# 🟢 જે ન્યૂઝ સ્ટોકને રોકેટ બનાવે
SUPER_CATALYSTS = [
    "ORDER", "CONTRACT", "AWARD", "BAGS", "L1", "BIDDER",
    "ANTI-DUMPING", "DGTR", "TARIFF", "USFDA", "EIR", "ZERO 483", 
    "APPROVAL", "DEMERGER", "SPIN OFF", "TAKEOVER", "ACQUISITION", "PATENT"
]

TRASH_BLACKLIST = [
    "LOSS OF SHARE", "DUPLICATE", "TRADING WINDOW", "RESIGNATION", 
    "POSTAL BALLOT", "CREDIT RATING", "MEETING SCHEDULE", "NEWSPAPER"
]

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": msg, "parse_mode": "HTML"}
    try:
        requests.post(url, data=payload, timeout=8)
    except:
        pass

def scrape_bse_direct():
    today_str = datetime.now().strftime("%Y%m%d") # આજની તારીખ આપોઆપ લેશે
    session = requests.Session()
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9"
    }

    # ૧. પહેલું સ્ટેપ: BSE સર્વર સાથે કૂકીઝ (Handshake) કનેક્ટ કરશે
    try:
        session.get("https://www.bseindia.com/corporates/ann.html", headers=headers, timeout=10)
    except:
        pass

    # ૨. બીજું સ્ટેપ: સીધા સત્તાવાર BSE API પરથી આજની લાઈવ PDF ફાઈલો ખેંચશે
    api_headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Referer": "https://www.bseindia.com/corporates/ann.html",
        "Origin": "https://www.bseindia.com",
        "Accept": "application/json, text/plain, */*"
    }
    
    api_url = f"https://api.bseindia.com/BseIndiaAPI/api/AnnSubCategoryGetData/w?pageno=1&strCat=-1&strPrevDate={today_str}&strScrip=&strSearch=P&strToDate={today_str}&strType=C&subcategory="

    try:
        res = session.get(api_url, headers=api_headers, timeout=15)
        print(f"BSE Direct API Status: {res.status_code}")

        if res.status_code == 200:
            announcements = res.json().get("Table", [])
            print(f"Successfully fetched {len(announcements)} direct BSE filings!")

            # ટેસ્ટ મેસેજ
            send_telegram(f"🏢 <b>BSE Direct Point-Zero Connected!</b>\nScanning {len(announcements)} live official filings for today!")

            for item in announcements[:25]:
                headline = str(item.get("NEWSSUB", "")).upper()
                company = item.get("SLONGNAME", "")
                attachment = str(item.get("ATTACHMENTNAME", ""))
                pdf_link = f"https://www.bseindia.com/xml-data/corpfiling/AttachLive/{attachment}"

                if any(trash in headline for trash in TRASH_BLACKLIST):
                    continue

                if any(cat in headline for cat in SUPER_CATALYSTS):
                    alert_msg = (
                        f"🚨 <b>POINT-ZERO BSE BLAST!</b> 🚨\n\n"
                        f"🏢 <b>Company:</b> {company}\n"
                        f"⚡ <b>Filing:</b> {headline}\n\n"
                        f"🔗 <a href='{pdf_link}'>Open Official BSE PDF</a>\n\n"
                        f"👉 <i>Direct from BSE within 60 seconds!</i>"
                    )
                    send_telegram(alert_msg)
                    time.sleep(1)
                    break
        else:
            print(f"BSE returned: {res.status_code}")
    except Exception as e:
        print(f"BSE Scraper Error: {e}")

if __name__ == "__main__":
    scrape_bse_direct()
