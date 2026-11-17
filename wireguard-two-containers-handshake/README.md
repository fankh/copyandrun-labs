# WireGuard 터널 컨테이너 두 개로 만들기: 핸드셰이크

컨테이너 두 개 사이에 WireGuard 터널을 만들고, 정상 설정과 공개키를 잘못 적은 설정, 허용 주소를 잘못 적은 설정을 같은 점검으로 비교합니다. 핸드셰이크가 되어도 ping이 실패하는 경우와 터널 안의 내용이 겉에서 보이지 않는 것을 tcpdump로 확인하고, 결과를 종료 코드로 바꿉니다.

## 링크

- 글: [https://copyandrun.com/blog/wireguard-two-containers-handshake/](https://copyandrun.com/blog/wireguard-two-containers-handshake/)
- 한 번에 받기: [wireguard-two-containers-handshake.zip](https://copyandrun.com/code-zip/wireguard-two-containers-handshake.zip)
- GitHub 폴더: [copyandrun-labs/wireguard-two-containers-handshake](https://github.com/fankh/copyandrun-labs/tree/main/wireguard-two-containers-handshake)
- 전체 목록: [https://fankh.github.io/copyandrun-labs/](https://fankh.github.io/copyandrun-labs/)

## 파일

| 파일 | 내려받기 | GitHub에서 보기 |
| --- | --- | --- |
| `wg_demo.sh` | <a href="https://fankh.github.io/copyandrun-labs/wireguard-two-containers-handshake/wg_demo.sh" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/wireguard-two-containers-handshake/wg_demo.sh) |
| `wg_summary.py` | <a href="https://fankh.github.io/copyandrun-labs/wireguard-two-containers-handshake/wg_summary.py" download>내려받기</a> | [보기](https://github.com/fankh/copyandrun-labs/blob/main/wireguard-two-containers-handshake/wg_summary.py) |

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
