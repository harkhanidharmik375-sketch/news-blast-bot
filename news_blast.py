import requests
import json
import time

# --- તમારા ઓરિજિનલ ક્રેડેન્શિયલ્સ (ઓલરેડી સેટ થઈ ગયા છે) ---
TELEGRAM_BOT_TOKEN = "8947925352:AAH92xZTCpCdbzsl8KKhRhl520IEJ8ee_Bc"
TELEGRAM_CHAT_ID = "1906881906"

# 🟢 જે ન્યૂઝ સ્ટોકને રોકેટ બનાવે (Super Catalysts)
SUPER_CATALYSTS = [
    "ORDER", "CONTRACT", "AWARD", "BAGS", "L1 BIDDER",
    "ANTI-DUMPING", "DGTR", "TARIFF",
    "USFDA", "EIR", "ZERO 483", "ANDA APPROVAL",
    "DEMERGER", "SPIN OFF", "TAKEOVER", "ACQUISITION",
    "PATENT", "PLI", "CAPEX"
]

# 🔴 કચરો અને ટ્રેપ ન્યૂઝ (તરત બ્લોક કરશે)
TRASH_BLACKLIST = [
    "LOSS OF SHARE", "DUPLICATE", "TRADING WINDOW", 
    "POSTAL BALLOT", "RESIGNATION", "MEETING SCHEDULE", 
    "CREDIT RATING REAFFIRMED", "INVESTOR PRESENTATION", 
    "ESOP ALLOTMENT", "NEWSPAPER PUBLICATION"
]

def send_alert(company, headline, pdf_link):
    msg = (
        f"🚨 <b>HIGH-VELOCITY BLAST NEWS!</b> 🚨\n\n"
        f"🏢 <b>Stock:</b> {company}\n"
        f"⚡ <b>Catalyst:</b> {headline}\n\n"
        f"🔗 <a href='{pdf_link}'>Read BSE Announcement</a>\n\n"
        f"👉 <i>Check broker immediately! If stock is +1% to +3%, it's an entry!</i>"
    )
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": msg, "parse_mode": "HTML"}
    try:
        requests.post(url, data=payload, timeout=5)
    except Exception as e:
        print(f"Telegram error: {e}")

def check_bse_news():
    url = "https://api.bseindia.com/BseIndiaAPI/api/AnnSubCategoryGetData/w?pageno=1&strCat=-1&strPrevDate=&strScrip=&strSearch=P&strToDate=&strType=C"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        res = requests.get(url, headers=headers, timeout=10)
        announcements = res.json().get("Table", [])
        for item in announcements[:15]:
            headline = str(item.get("NEWSSUB", "")).upper()
            company = item.get("SLONGNAME", "")
            attachment = item.get("ATTACHMENTNAME", "")
            pdf_link = f"https://www.bseindia.com/xml-data/corpfiling/AttachLive/{attachment}"

            # જો કચરો ન્યૂઝ હોય તો છોડી દો
            if any(trash in headline for trash in TRASH_BLACKLIST):
                continue

            # જો બ્લાસ્ટ ન્યૂઝ હોય તો ટેલિગ્રામ પર મોકલો
            if any(cat in headline for cat in SUPER_CATALYSTS):
                send_alert(company, headline, pdf_link)
                time.sleep(1)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_bse_news()
