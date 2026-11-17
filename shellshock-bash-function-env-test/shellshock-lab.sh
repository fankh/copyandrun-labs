#!/bin/sh
# 사용: sh shellshock-lab.sh
# 공식 bash 이미지 세 개(3.2, 4.3, 5.2)에서 같은 폴더의 shellshock-check.sh 를 실행하고,
# 마지막에 취약한 bash 를 흉내 내는 fake-bash.sh 로 취약 판정 경로도 확인한다. 네트워크는 쓰지 않는다.
# Git Bash 에서는 경로 변환을 끈다.
export MSYS_NO_PATHCONV=1
for v in 3.2 4.3 5.2; do
  echo "== bash:$v"
  docker run --rm --network none -v "$(pwd)":/w bash:$v sh /w/shellshock-check.sh
done
echo "== 취약한 bash 흉내"
docker run --rm --network none -v "$(pwd)":/w bash:5.2 sh -c "cp /w/fake-bash.sh /tmp/fake-bash && chmod +x /tmp/fake-bash && sh /w/shellshock-check.sh /tmp/fake-bash"
