import requests
import urllib.parse
import base64
import threading
import argparse
import time
from html import escape

# Configure Tor proxy
PROXIES = {
    "http": "socks5h://127.0.0.1:9050",
    "https": "socks5h://127.0.0.1:9050"
}

# Encode the payloads in different formats
def encode_payloads(payload):
    return {
        "original": payload,
        "url_encoded": urllib.parse.quote(payload),
        "base64": base64.b64encode(payload.encode()).decode(),
        "html_encoded": escape(payload)
    }

# Perform the XSS test request
def test_xss(url, payload):
    encoded_variants = encode_payloads(payload)
    
    for encoding, encoded_payload in encoded_variants.items():
        try:
            target_url = url.replace("XSS_PAYLOAD", encoded_payload)
            response = requests.get(target_url, proxies=PROXIES, timeout=5)

            if payload in response.text:
                print(f"[✅] XSS Vulnerability Detected! ({encoding}) ➜ {target_url}")
                with open("xss_results.log", "a") as log:
                    log.write(f"[✅] {target_url}\n")
            else:
                print(f"[❌] Not Vulnerable: {target_url}")

        except requests.RequestException as e:
            print(f"[⚠️] Request Failed: {e}")

# Multi-threaded scanning
def start_scan(url, payloads, threads):
    def worker(payload):
        test_xss(url, payload)

    with threading.Semaphore(threads):
        for payload in payloads:
            threading.Thread(target=worker, args=(payload,)).start()

# CLI Argument Parsing
def main():
    parser = argparse.ArgumentParser(description="Automated XSS Scanner with IP Rotation")
    parser.add_argument("url", help="Target URL (Use 'XSS_PAYLOAD' as the injection point)")
    parser.add_argument("-p", "--payloads", help="Custom payload file", default="payloads.txt")
    parser.add_argument("-t", "--threads", type=int, default=5, help="Number of concurrent threads")

    args = parser.parse_args()

    # Load payloads
    with open(args.payloads, "r") as f:
        payloads = [line.strip() for line in f.readlines() if line.strip()]

    print(f"[🚀] Scanning {args.url} with {args.threads} threads using {len(payloads)} payloads...")
    
    # Start scanning
    start_scan(args.url, payloads, args.threads)

if __name__ == "__main__":
    main()
