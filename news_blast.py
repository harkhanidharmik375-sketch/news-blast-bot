import requests
import json
import time

TELEGRAM_BOT_TOKEN = "8947925352:AAH92xZTCpCdbzsl8KKhRhl520IEJ8ee_Bc"
TELEGRAM_CHAT_ID = "1906881906"

# 🟢 હાઈ-વેલોસિટી કેટાલિસ્ટ
SUPER_CATALYSTS = [
    "ORDER", "CONTRACT", "AWARD", "BAGS", "L1", "BIDDER",
    "ANTI-DUMPING", "DGTR", "TARIFF", "USFDA", "EIR", "ZERO 483", 
    "APPROVAL", "DEMERGER", "SPIN OFF", "TAKEOVER", "ACQUISITION", "PATENT"
]

TRASH_BLACKLIST = [
    "LOSS OF SHARE", "DUPLICATE", "TRADING WINDOW", 
    "POSTAL BALLOT", "RESIGNATION", "MEETING SCHEDULE", 
    "CREDIT RATING", "NEWSPAPER"
]

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": msg, "parse_mode": "HTML"}
    try:
        requests.post(url, data=payload, timeout=8)
    except:
        pass

def check_bse_news():
    # એન્ટિ-બ્લોકિંગ બ્રાઉઝર સેશન
    session = requests.Session()
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Referer": "https://www.bseindia.com/corporates/ann.html",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-US,en;q=0.9",
        "Origin": "https://www.bseindia.com"
    }
    
    url = "https://api.bseindia.com/BseIndiaAPI/api/AnnSubCategoryGetData/w?pageno=1&strCat=-1&strPrevDate=&strScrip=&strSearch=P&strToDate=&strType=C"
    
    try:
        res = session.get(url, headers=headers, timeout=15)
        print(f"BSE Response Status: {res.status_code}")
        
        if res.status_code == 200:
            announcements = res.json().get("Table", [])
            print(f"Fetched {len(announcements)} announcements successfully!")
            
            for item in announcements[:25]:
                headline = str(item.get("NEWSSUB", "")).upper()
                company = item.get("SLONGNAME", "")
                attachment = item.get("ATTACHMENTNAME", "")
                pdf_link = f"https://www.bseindia.com/xml-data/corpfiling/AttachLive/{attachment}"

                if any(trash in headline for trash in TRASH_BLACKLIST):
                    continue

                if any(cat in headline for cat in SUPER_CATALYSTS):
                    alert_text = (
                        f"🚨 <b>HIGH-VELOCITY BLAST NEWS!</b> 🚨\n\n"
                        f"🏢 <b>Stock:</b> {company}\n"
                        f"⚡ <b>Catalyst:</b> {headline}\n\n"
                        f"🔗 <a href='{pdf_link}'>Read BSE Filing</a>"
                    )
                    send_telegram(alert_text)
                    time.sleep(1)
        else:
            send_telegram(f"⚠️ BSE Server Connection Blocked: HTTP {res.status_code}")
    except Exception as e:
        print(f"Error: {e}")
        send_telegram(f"⚠️ Bot Alert Error: {str(e)[:100]}")

if __name__ == "__main__":
    check_bse_news()
