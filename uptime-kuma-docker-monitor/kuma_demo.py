"""Uptime Kuma 를 도커로 띄우고, 감시 대상 세 개를 만들어 정상 -> 장애 -> 복구를 기록하고, 볼륨 백업과 복원까지 확인한다.

준비: Docker, pip install "python-socketio[client]" websocket-client
주의: osk-kuma, osk-kuma-b, osk-target 컨테이너와 osk_kuma, osk_kuma_b 볼륨, osk-net-kuma 네트워크를 만들고 끝에서 모두 지운다.
      같은 이름이 이미 있으면 먼저 지운다. 127.0.0.1:3901 에만 연다.
실행: python -X utf8 kuma_demo.py   (약 4분)
"""
import subprocess
import time

import socketio

PORT = 3901
URL = f"http://127.0.0.1:{PORT}"
NET, TARGET, KUMA, VOL = "osk-net-kuma", "osk-target", "osk-kuma", "osk_kuma"
USER, PW = "admin", "Lab-Only-Pass-1"      # 실습용 값이다. 실제 계정에는 쓰지 않는다


def sh(*a, check=True):
    r = subprocess.run(a, capture_output=True, text=True)
    if check and r.returncode:
        raise RuntimeError(f"{a}: {r.stderr.strip()}")
    return r.stdout.strip()


def cleanup():
    for c in (KUMA, TARGET):
        sh("docker", "rm", "-f", c, check=False)
    sh("docker", "network", "rm", NET, check=False)
    sh("docker", "volume", "rm", VOL, "osk_kuma_b", check=False)


def wait_up():
    for _ in range(90):
        code = subprocess.run(["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", URL + "/"],
                              capture_output=True, text=True).stdout
        if code in ("200", "302"):
            return
        time.sleep(2)
    raise RuntimeError("Uptime Kuma 가 시작되지 않았다")


def connect():
    sio = socketio.Client()
    sio.beats = {}                                   # 감시 대상 번호 -> [(시각, 상태)]

    @sio.on("heartbeat")
    def _hb(b):
        sio.beats.setdefault(b["monitorID"], []).append((time.time(), b["status"], b.get("msg", ""), b.get("ping")))

    sio.connect(URL, transports=["websocket"])
    return sio


def call(sio, event, *args):
    box = {}
    sio.emit(event, args, callback=lambda r: box.update(r=r))
    for _ in range(100):
        if "r" in box:
            return box["r"]
        time.sleep(0.1)
    raise TimeoutError(event)


def monitor(name, url, **kw):
    m = {"type": "http", "name": name, "url": url, "method": "GET", "interval": 20, "retryInterval": 20,
         "resendInterval": 0, "maxretries": 0, "timeout": 10, "accepted_statuscodes": ["200-299"],
         "notificationIDList": {}, "ignoreTls": False, "upsideDown": False, "maxredirects": 10,
         "dns_resolve_type": "A", "dns_resolve_server": "1.1.1.1", "proxyId": None, "expiryNotification": False}
    m.update(kw)
    return m


def last(sio, mid):
    return sio.beats.get(mid, [(0, None, "", None)])[-1]


NAMES = {1: "정상 대상", 2: "없는 포트", 3: "키워드"}


def show(sio, title):
    print(f"-- {title}")
    for mid, name in NAMES.items():
        t, st, msg, ping = last(sio, mid)
        print(f"   {name:<8} status={st} ({'UP' if st == 1 else 'DOWN' if st == 0 else '기록 없음'}) ping={ping} msg={msg[:40]!r}")


cleanup()
print("## 1. 감시받을 nginx 와 Uptime Kuma 실행")
sh("docker", "network", "create", NET)
sh("docker", "run", "-d", "--name", TARGET, "--network", NET, "nginx:alpine")
sh("docker", "run", "-d", "--name", KUMA, "--network", NET, "-p", f"127.0.0.1:{PORT}:3001",
   "-v", f"{VOL}:/app/data", "louislam/uptime-kuma:1")
wait_up()
print("Uptime Kuma 응답 확인:", sh("docker", "inspect", "-f", "{{.State.Status}}", KUMA))

print("## 2. 관리자 계정과 감시 대상 세 개 만들기(소켓 API)")
sio = connect()
print("setup:", call(sio, "setup", USER, PW).get("ok"))
print("login:", call(sio, "login", {"username": USER, "password": PW, "token": ""}).get("ok"))
for name, url, extra in (("정상 대상", f"http://{TARGET}/", {}),
                         ("없는 포트", f"http://{TARGET}:3999/", {}),
                         ("키워드", f"http://{TARGET}/", {"type": "keyword", "keyword": "Welcome to nginx"})):
    r = call(sio, "add", monitor(name, url, **extra))
    print(f"add {name}: ok={r.get('ok')} id={r.get('monitorID')}")
time.sleep(45)
show(sio, "45초 뒤")

print("## 3. 장애 만들기: 감시 대상 nginx 를 멈춘다")
t0 = time.time()
sh("docker", "stop", TARGET)
detected = None
while time.time() - t0 < 90:
    if last(sio, 1)[1] == 0 and last(sio, 1)[0] > t0:
        detected = last(sio, 1)[0] - t0
        break
    time.sleep(1)
print(f"정상 대상이 DOWN 으로 기록되기까지 {detected:.0f}초 (감시 주기 20초)" if detected else "90초 안에 DOWN 이 기록되지 않음")
time.sleep(22)                                   # 감시 대상마다 확인 시각이 달라, 한 주기 더 기다린 뒤 읽는다
show(sio, "장애 중")

print("## 4. 복구: nginx 를 다시 시작한다")
t1 = time.time()
sh("docker", "start", TARGET)
back = None
while time.time() - t1 < 90:
    if last(sio, 1)[1] == 1 and last(sio, 1)[0] > t1:
        back = last(sio, 1)[0] - t1
        break
    time.sleep(1)
print(f"UP 으로 돌아오기까지 {back:.0f}초" if back else "90초 안에 UP 으로 돌아오지 않음")
sio.disconnect()

print("## 5. 볼륨 백업과 복원: 컨테이너와 볼륨을 지운 뒤 같은 데이터로 다시 띄운다")
sh("docker", "stop", KUMA)
sh("docker", "run", "--rm", "-v", f"{VOL}:/data", "-v", "osk_kuma_b:/bk", "alpine", "sh", "-c",
   "cp -a /data/. /bk/ && ls /bk | tr '\n' ' '")
print("복사한 파일:", sh("docker", "run", "--rm", "-v", "osk_kuma_b:/bk", "alpine", "ls", "/bk").replace("\n", " "))
sh("docker", "rm", "-f", KUMA)
sh("docker", "volume", "rm", VOL)
sh("docker", "run", "-d", "--name", KUMA, "--network", NET, "-p", f"127.0.0.1:{PORT}:3001",
   "-v", "osk_kuma_b:/app/data", "louislam/uptime-kuma:1")
wait_up()
sio = connect()
print("복원 뒤 login:", call(sio, "login", {"username": USER, "password": PW, "token": ""}).get("ok"))
time.sleep(5)
sio.disconnect()
sio2 = socketio.Client()
lists = {}
sio2.on("monitorList", lambda d: lists.update(d=d))
sio2.connect(URL, transports=["websocket"])
call(sio2, "login", {"username": USER, "password": PW, "token": ""})
time.sleep(4)
print("복원된 감시 대상:", sorted(m["name"] for m in lists.get("d", {}).values()))
sio2.disconnect()

print("## 6. 정리")
cleanup()
print("남은 osk 컨테이너:", len(sh("docker", "ps", "-a", "--filter", "name=osk-", "--format", "{{.Names}}").split()))
