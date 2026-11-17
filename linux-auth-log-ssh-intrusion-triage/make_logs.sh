#!/bin/sh
# 시험 로그를 만듭니다. 비밀번호 틀린 시도 몇 번과 올바른 로그인 1번뿐이며 반복 도구는 쓰지 않습니다.
SERVER=10.89.40.10
SSH="ssh -o StrictHostKeyChecking=no -o PubkeyAuthentication=no -o LogLevel=ERROR"

# A(10.89.40.21): 계정을 바꿔 가며 4번 실패, 성공 없음
docker exec cr-f9-a sshpass -p wrong1 $SSH deploy@$SERVER true
docker exec cr-f9-a sshpass -p wrong2 $SSH deploy@$SERVER true
docker exec cr-f9-a sshpass -p wrong3 $SSH admin@$SERVER true
docker exec cr-f9-a sshpass -p wrong4 $SSH root@$SERVER true

# B(10.89.40.22): deploy 계정으로 3번 실패한 뒤 올바른 비밀번호로 로그인하고 명령 3개 실행
docker exec cr-f9-b sshpass -p guess1 $SSH deploy@$SERVER true
docker exec cr-f9-b sshpass -p guess2 $SSH deploy@$SERVER true
docker exec cr-f9-b sshpass -p guess3 $SSH deploy@$SERVER true
docker exec cr-f9-b sshpass -p Lab-Pass-2026 $SSH deploy@$SERVER \
  'echo Lab-Pass-2026 | sudo -S -p "" id; echo Lab-Pass-2026 | sudo -S -p "" cat /etc/shadow > /dev/null; echo Lab-Pass-2026 | sudo -S -p "" useradd -m svc-backup'
