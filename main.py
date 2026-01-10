import requests
import os

# --- YOUR WATCH LIST ---
# Paste the exact links of the watches you want to track below.
WATCH_URLS = [
    "https://www.hmtwatches.in/product_details?id=eyJpdiI6ImNMb0FkRGZpeWJUWkM0OENBT2p6aEE9PSIsInZhbHVlIjoidlZndzJwNFZ5Y3RmdTlxcndrWmJWdz09IiwibWFjIjoiY2NiYTE4MTFkZDYyMTBiZWRmODE4ZDA0YTI5OTFkYTk2OWE3Y2I5OTBjZjBhZGU0Y2UzODE2YTdhOWMwNWM2OCIsInRhZyI6IiJ9",
    "https://www.hmtwatches.in/product_details?id=eyJpdiI6IkJ6aEMzdlJ3dlBPb3V0SUt2Uzd6Qnc9PSIsInZhbHVlIjoiMW1WWU9NSGZsSUlzdllRT2FhMUNrUT09IiwibWFjIjoiMmNhYTFiMDJlOWI1YWIwZTAyMTEwYzRkOWQyYzJlYzg2ZWFiZjJlZGIxYzYzMzNhNjZlNjQwNDE1MTIxMGM0MiIsInRhZyI6IiJ9",
    "https://www.hmtwatches.in/product_details?id=eyJpdiI6IjQyOE1qTTlsOXZZN0t6akpXSytXbHc9PSIsInZhbHVlIjoiTlg2QTNEaEliRlJiQ3A1ZFpGOFpXdz09IiwibWFjIjoiZjRjNTZjNjkwZjI0YzkwNjlhZTE3ZDE1Mjc2Y2RlNWQzNjEwNjJmMGY5YTM3YjQ0NzI0NTAzMDY2YmU5YmVlNSIsInRhZyI6IiJ9",
    "https://www.hmtwatches.in/product_details?id=eyJpdiI6Ijl3YVA3RzFZZ1NDeW1YZU5pTmpGaXc9PSIsInZhbHVlIjoicnZZSjNhZE42M3kzMURoR1p4YXJDdz09IiwibWFjIjoiZTkwNTI4NDBhYTM5NWIxMDc2ODU3YTVjNTRlOTI3ZmQxZTViNmQ2MDRlZmMxZTlmYTY2NTcyYjZiOWZlNzcwNiIsInRhZyI6IiJ9",
    "https://www.hmtwatches.in/product_details?id=eyJpdiI6ImxWQTNKZ3RYbWZaS3hUREhSUXp1dlE9PSIsInZhbHVlIjoicVlleGdWNUJXMmhqWFNFSmszaFV5UT09IiwibWFjIjoiNDcwY2I2MTQ0MzRkNGZkMGFkNmI5MTUwNDdkMTRkZGUzZTMwNDdkMTI5YTk4MDA4NmExYjA3MTlhYzQ2MzZmOSIsInRhZyI6IiJ9",
    "https://www.hmtwatches.in/product_details?id=eyJpdiI6IkgvVEFUUWY2bHE5a25ybUF0QkY3alE9PSIsInZhbHVlIjoieklWeGgxMHVMSVBVcGtSR2VZUjhCUT09IiwibWFjIjoiNzRmMjY4NTQwNTIxMDAwY2I3YjI3NDQ5NjFmNzI2NTMzODE5ZDI5NDY2M2EyNjI2MDgwOWRlOTc5NzI5MjQ3NyIsInRhZyI6IiJ9",
    "https://www.hmtwatches.in/product_details?id=eyJpdiI6ImpwcUk0bmRoMEUrYWt2MzVzelZWN0E9PSIsInZhbHVlIjoiNlVNUXJxQ3ltampmdERrN1lrZjljZz09IiwibWFjIjoiZTQzZThlNDcwZDVhYzNlYzg1NDQzMmU0YTMxZDk0NzM5YjEwMTgwOGU0ZWVhMmViNThmYzQ5ZDViMjFiYzEwNiIsInRhZyI6IiJ9"
]

# --- THE LOGIC (DO NOT CHANGE) ---
TOKEN = os.environ['TELEGRAM_TOKEN']
CHAT_ID = os.environ['TELEGRAM_CHAT_ID']

def send_alert(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.get(url, params={"chat_id": CHAT_ID, "text": message})

def check_stock():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    for link in WATCH_URLS:
        try:
            print(f"Checking: {link}")
            response = requests.get(link, headers=headers)
            content = response.text.lower()
            
            # HMT logic: If "out of stock" text is NOT on the page, it might be available
            if "out of stock" not in content and "add to cart" in content:
                msg = f"🚨 HMT STOCK ALERT! \n\nWatch might be available!\nLink: {link}"
                send_alert(msg)
                print("Alert sent!")
            else:
                print("Still out of stock.")
                
        except Exception as e:
            print(f"Error checking link: {e}")

if __name__ == "__main__":
    check_stock()
