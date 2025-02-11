FROM python:3.10

RUN apt-get update && apt-get install -y \
    tor \
    && rm -rf /var/lib/apt/lists/*

COPY torrc /etc/tor/torrc

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY xss_tool.py /app/xss_tool.py
COPY payloads.txt /app/payloads.txt

WORKDIR /app

EXPOSE 9050

CMD service tor start && python xss_tool.py
