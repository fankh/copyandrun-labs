FROM debian:12-slim
RUN apt-get update \
 && apt-get install -y --no-install-recommends nginx openssl python3 logrotate passwd \
 && rm -rf /var/lib/apt/lists/*
COPY weak_setup.sh check.py fix.sh /opt/
RUN chmod +x /opt/*.sh && sh /opt/weak_setup.sh
EXPOSE 443
CMD ["nginx", "-g", "daemon off;"]
