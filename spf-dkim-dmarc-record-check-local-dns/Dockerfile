FROM debian:12-slim
RUN apt-get update \
 && apt-get install -y --no-install-recommends dnsmasq python3-dnspython \
 && rm -rf /var/lib/apt/lists/*
COPY dnsmasq.conf /etc/dnsmasq.conf
COPY check_mail_dns.py show_txt.py /opt/
CMD ["dnsmasq", "--keep-in-foreground", "--conf-file=/etc/dnsmasq.conf"]
