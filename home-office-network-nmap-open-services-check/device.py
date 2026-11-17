"""사무실 기기를 흉내 내는 연습용 서버입니다. 지정한 포트에서 짧은 응답만 돌려줍니다.

사용법: python device.py 21:ftp 23:telnet 80:router 631:printer 445:tcp 9100:tcp
종류: ftp(FTP 인사말), telnet(로그인 프롬프트), router(관리 화면 HTML), printer(프린터 웹 화면), tcp(연결만 받음)
실제 서비스가 아니며 로그인 기능이 없습니다. 연습용 점검 대상으로만 씁니다.
"""
import socket
import sys
import threading

ROUTER_PAGE = """<html><head><title>Office Router Admin</title></head>
<body><h1>Office Router</h1><p>관리자 로그인 (연습용 화면, 입력은 처리하지 않습니다)</p>
<form><input name="user"><input name="pw" type="password"><button>Login</button></form></body></html>"""
PRINTER_PAGE = "<html><head><title>Office Printer</title></head><body><h1>Printer status: Ready</h1></body></html>"


def http_reply(server, body):
    data = body.encode("utf-8")
    head = f"HTTP/1.1 200 OK\r\nServer: {server}\r\nContent-Type: text/html; charset=utf-8\r\nContent-Length: {len(data)}\r\nConnection: close\r\n\r\n"
    return head.encode("ascii") + data


def handle(conn, kind):
    try:
        conn.settimeout(3)
        if kind == "ftp":
            conn.sendall(b"220 vsFTPd 3.0.5 ready\r\n")
            conn.recv(256)
            conn.sendall(b"530 Please login with USER and PASS.\r\n")
        elif kind == "telnet":
            conn.sendall(b"\xff\xfd\x18\xff\xfd\x20\r\nOffice Router\r\nlogin: ")
            conn.recv(256)
        elif kind == "router":
            conn.recv(1024)
            conn.sendall(http_reply("lab-httpd", ROUTER_PAGE))
        elif kind == "printer":
            conn.recv(1024)
            conn.sendall(http_reply("CUPS/2.4 IPP/2.1", PRINTER_PAGE))
        else:
            conn.recv(256)
    except OSError:
        pass
    finally:
        conn.close()


def serve(port, kind):
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(("0.0.0.0", port))
    s.listen(16)
    while True:
        conn, _ = s.accept()
        threading.Thread(target=handle, args=(conn, kind), daemon=True).start()


def main():
    specs = [a.split(":") for a in sys.argv[1:]]
    for port, kind in specs:
        threading.Thread(target=serve, args=(int(port), kind), daemon=True).start()
    print("listening:", " ".join(sys.argv[1:]) or "(none)", flush=True)
    threading.Event().wait()


if __name__ == "__main__":
    main()
