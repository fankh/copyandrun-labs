#!/bin/sh
# 역할(send, recv, dns)에 맞는 설정을 넣고 서비스를 띄웁니다.
ROLE=$1
KEYDIR=/etc/opendkim/keys/example.internal
mkdir -p /run/opendkim && chown opendkim:opendkim /run/opendkim

case "$ROLE" in
  send)
    cp /opt/sign.conf /etc/opendkim.conf
    cp /opt/send-main.cf /etc/postfix/main.cf
    mkdir -p $KEYDIR
    if [ ! -f $KEYDIR/s2026a.private ]; then
      opendkim-genkey -b 2048 -d example.internal -s s2026a -D $KEYDIR
    fi
    chown -R opendkim:opendkim /etc/opendkim
    chmod 700 $KEYDIR && chmod 600 $KEYDIR/s2026a.private
    opendkim -x /etc/opendkim.conf
    exec postfix start-fg
    ;;
  recv)
    cp /opt/verify.conf /etc/opendkim.conf
    cp /opt/recv-main.cf /etc/postfix/main.cf
    opendkim -x /etc/opendkim.conf
    exec postfix start-fg
    ;;
  dns)
    exec dnsmasq -k --conf-file=/opt/dns.conf
    ;;
  *)
    echo "역할은 send, recv, dns 중 하나입니다." >&2
    exit 2
    ;;
esac
