# XSS Tester 🕵️‍♂️

An automated XSS injection tool with IP rotation & payload encoding.

## Please use it for ethical purpose only, this is only for educational purpose.

## Features
✅ Multi-threading for fast scanning  
✅ Encodes payloads (Base64, URL encoding, HTML entities)  
✅ Custom payload support  
✅ Tor-based IP rotation  

## Installation  
### Using Python  
```bash
git clone https://github.com/your-username/xss-tester.git
cd xss-tester
pip install -r requirements.txt
python xss_tool.py "http://example.com"
```

### Using Docker
```bash 
docker build -t xss-tester .
docker run --rm xss-tester
```

### For Custom Payloads
```bash
docker run --rm -v $(pwd)/payloads.txt:/app/payloads.txt xss-tester

