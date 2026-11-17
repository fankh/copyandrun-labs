FROM debian:12-slim
ENV DEBIAN_FRONTEND=noninteractive
RUN echo "postfix postfix/main_mailer_type select Local only" | debconf-set-selections \
 && echo "postfix postfix/mailname string example.internal" | debconf-set-selections \
 && apt-get update \
 && apt-get install -y --no-install-recommends postfix opendkim opendkim-tools dnsmasq python3 bind9-dnsutils \
 && rm -rf /var/lib/apt/lists/*
COPY entrypoint.sh sign.conf verify.conf send-main.cf recv-main.cf dns.conf tamper.py headers.py bodyhash.py /opt/
RUN chmod +x /opt/entrypoint.sh && useradd -m carol
ENTRYPOINT ["/opt/entrypoint.sh"]
