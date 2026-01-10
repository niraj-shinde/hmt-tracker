import requests
import os
from bs4 import BeautifulSoup # This tool parses the HTML code

# --- YOUR WATCH LIST (PAIRS OF NAME + URL) ---
# Update this list with the watches you want to track.
WATCHES = [
    {
        "name": "HMT Tareeq Quartz Turquoise Blue",
        "url": "https://www.hmtwatches.in/product_details?id=eyJpdiI6ImNMb0FkRGZpeWJUWkM0OENBT2p6aEE9PSIsInZhbHVlIjoidlZndzJwNFZ5Y3RmdTlxcndrWmJWdz09IiwibWFjIjoiY2NiYTE4MTFkZDYyMTBiZWRmODE4ZDA0YTI5OTFkYTk2OWE3Y2I5OTBjZjBhZGU0Y2UzODE2YTdhOWMwNWM2OCIsInRhZyI6IiJ9"
    },
    {
        "name": "HMT Kohinoor Quartz B1 Maroon",
        "url": "https://www.hmtwatches.in/product_details?id=eyJpdiI6IkJ6aEMzdlJ3dlBPb3V0SUt2Uzd6Qnc9PSIsInZhbHVlIjoiMW1WWU9NSGZsSUlzdllRT2FhMUNrUT09IiwibWFjIjoiMmNhYTFiMDJlOWI1YWIwZTAyMTEwYzRkOWQyYzJlYzg2ZWFiZjJlZGIxYzYzMzNhNjZlNjQwNDE1MTIxMGM0MiIsInRhZyI6IiJ9"
    },
    {
        "name": "HMT Kohinoor Quartz B1 Light Blue Sunray",
        "url": "https://www.hmtwatches.in/product_details?id=eyJpdiI6IjQyOE1qTTlsOXZZN0t6akpXSytXbHc9PSIsInZhbHVlIjoiTlg2QTNEaEliRlJiQ3A1ZFpGOFpXdz09IiwibWFjIjoiZjRjNTZjNjkwZjI0YzkwNjlhZTE3ZDE1Mjc2Y2RlNWQzNjEwNjJmMGY5YTM3YjQ0NzI0NTAzMDY2YmU5YmVlNSIsInRhZyI6IiJ9"
    },
    {
        "name": "HMT Janata Automatic White",
        "url": "https://www.hmtwatches.in/product_details?id=eyJpdiI6Ijl3YVA3RzFZZ1NDeW1YZU5pTmpGaXc9PSIsInZhbHVlIjoicnZZSjNhZE42M3kzMURoR1p4YXJDdz09IiwibWFjIjoiZTkwNTI4NDBhYTM5NWIxMDc2ODU3YTVjNTRlOTI3ZmQxZTViNmQ2MDRlZmMxZTlmYTY2NTcyYjZiOWZlNzcwNiIsInRhZyI6IiJ9"
    },
    {
        "name": "HMT Himalaya Quartz Silver IPS",
        "url": "https://www.hmtwatches.in/product_details?id=eyJpdiI6ImxWQTNKZ3RYbWZaS3hUREhSUXp1dlE9PSIsInZhbHVlIjoicVlleGdWNUJXMmhqWFNFSmszaFV5UT09IiwibWFjIjoiNDcwY2I2MTQ0MzRkNGZkMGFkNmI5MTUwNDdkMTRkZGUzZTMwNDdkMTI5YTk4MDA4NmExYjA3MTlhYzQ2MzZmOSIsInRhZyI6IiJ9"
    },
    {
        "name": "HMT Stellar DASS 06 Screw White",
        "url": "https://www.hmtwatches.in/product_details?id=eyJpdiI6IkgvVEFUUWY2bHE5a25ybUF0QkY3alE9PSIsInZhbHVlIjoieklWeGgxMHVMSVBVcGtSR2VZUjhCUT09IiwibWFjIjoiNzRmMjY4NTQwNTIxMDAwY2I3YjI3NDQ5NjFmNzI2NTMzODE5ZDI5NDY2M2EyNjI2MDgwOWRlOTc5NzI5MjQ3NyIsInRhZyI6IiJ9"
    },
    {
        "name": "HMT Stellar DASS 04",
        "url": "https://www.hmtwatches.store/product/b8fbabdb-a49d-4e5d-92c6-71eda34c9382"
    }
]

# --- CONFIGURATION ---
TOKEN = os.environ['TELEGRAM_TOKEN']
CHAT_ID = os.environ['TELEGRAM_CHAT_ID']

def send_alert(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    try:
        requests.get(url, params={"chat_id": CHAT_ID, "text": message})
    except Exception as e:
        print(f"Telegram Error: {e}")

def check_stock():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    print("Starting smart scan...")
    
    for item in WATCHES:
        name = item['name']
        link = item['url']
        
        try:
            print(f"Scanning: {name}")
            response = requests.get(link, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Smart Check: Look for specific clickable buttons
            clickable_tags = soup.find_all(['button', 'a', 'input'])
            
            found_button = False
            for tag in clickable_tags:
                # Check text inside tags
                if tag.string and "add to cart" in tag.string.lower():
                    found_button = True
                    break
                # Check value attribute
                if tag.get('value') and "add to cart" in tag.get('value').lower():
                    found_button = True
                    break
            
            if found_button:
                # --- NEW MESSAGE FORMAT ---
                msg = f"🚨 IN STOCK: {name} \n\nGo grab it!\nLink: {link}"
                send_alert(msg)
                print(f">>> FOUND {name}! Alert sent.")
            else:
                print(f"{name} is not available.")
                
        except Exception as e:
            print(f"Error checking {name}: {e}")

if __name__ == "__main__":
    check_stock()
