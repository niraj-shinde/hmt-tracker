import requests
import os
from bs4 import BeautifulSoup

# --- YOUR WATCH LIST ---
WATCHES = [
    {
        "name": "HMT Tareeq Quartz Turquoise Blue",
        "url": "https://www.hmtwatches.in/product_details?id=eyJpdiI6ImNMb0FkRGZpeWJUWkM0OENBT2p6aEE9PSIsInZhbHVlIjoidlZndzJwNFZ5Y3RmdTlxcndrWmJWdz09IiwibWFjIjoiY2NiYTE4MTFkZDYyMTBiZWRmODE4ZDA0YTI5OTFkYTk2OWE3Y2I5OTBjZjBhZGU0Y2UzODE2YTdhOWMwNWM2OCIsInRhZyI6IiJ9"
    },
    {
        "name": "HMT Tareeq Quartz Turquoise Blue From Store",
        "url": "https://www.hmtwatches.store/product/7281c42e-604a-4bd9-b011-066aa202eddd"
    },
    {
        "name": "HMT Kohinoor Quartz B1 Maroon Sunray From Store",
        "url": "https://www.hmtwatches.store/product/0035cf80-48d5-4cf3-a02f-1f36b01071a5"
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
            
            is_new_store = "hmtwatches.store" in link
            found_button = False
            is_explicitly_out_of_stock = False
            
            # 1. NEW STORE OVERRIDE: Check if the exact "Out of Stock" badge is on the page
            if is_new_store:
                for tag in soup.find_all(['button', 'div', 'span']):
                    # Clean the text up to check exactly for "out of stock"
                    clean_text = tag.get_text(strip=True).lower().replace('\xa0', ' ')
                    if clean_text == "out of stock":
                        is_explicitly_out_of_stock = True
                        break
            
            # 2. STANDARD CHECK: Look for valid, clickable Add to Cart / Buy Now buttons
            clickable_tags = soup.find_all(['button', 'a', 'input'])
            
            for tag in clickable_tags:
                # IMPORTANT: Skip buttons that are turned off/disabled in the background code
                if tag.has_attr('disabled') or tag.get('aria-disabled') == 'true':
                    continue
                
                text = ""
                if tag.name == 'input':
                    text = tag.get('value', '').lower().strip()
                else:
                    text = tag.get_text(separator=' ', strip=True).lower()
                
                if "add to cart" in text or "buy now" in text:
                    found_button = True
                    break
            
            # 3. THE FINAL DECISION
            if is_new_store and is_explicitly_out_of_stock:
                print(f"{name} is explicitly marked Out of Stock on the Store. Skipping alerts.")
            elif found_button:
                msg = f"🚨 IN STOCK: {name} \n\nGo grab it!\nLink: {link}"
                send_alert(msg)
                print(f">>> FOUND {name}! Alert sent.")
            else:
                print(f"{name} is not available.")
                
        except Exception as e:
            print(f"Error checking {name}: {e}")

if __name__ == "__main__":
    check_stock()
