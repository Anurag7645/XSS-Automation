#!/bin/bash

# ASCII Art
echo -e "\e[1;31m"
cat << "EOF"

____  ___  _________ _________  ____  __.___.____    .____     _____________________  
\   \/  / /   _____//   _____/ |    |/ _|   |    |   |    |    \_   _____/\______   \ 
 \     /  \_____  \ \_____  \  |      < |   |    |   |    |     |    __)_  |       _/ 
 /     \  /        \/        \ |    |  \|   |    |___|    |___  |        \ |    |   \ 
/___/\  \/_______  /_______  / |____|__ \___|_______ \_______ \/_______  / |____|_  / 
      \_/        \/        \/          \/           \/       \/        \/         \/  

                    by Zeus ⚡
EOF
echo -e "\e[0m"

# Start Tor service
echo "[⚡] Starting Tor service..."
sudo systemctl start tor
sleep 3  # Give Tor some time to initialize
echo "[✅] Tor service started!"

# Check if venv exists, if not create it
if [ ! -d "venv" ]; then
    echo "[⚡] Creating virtual environment..."
    python3 -m venv venv
    echo "[✅] Virtual environment created!"
fi

# Activate venv
echo "[⚡] Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "[⚡] Installing dependencies..."
pip install -r requirements.txt

# Run the tool
echo "[⚡] Running XSS Killer..."
python3 xss_tool.py "$1"

# Deactivate venv after execution
deactivate
echo "[✅] Execution completed. Virtual environment deactivated."

# Stop Tor service after execution
echo "[⚡] Stopping Tor service..."
sudo systemctl stop tor
echo "[✅] Tor service stopped."
