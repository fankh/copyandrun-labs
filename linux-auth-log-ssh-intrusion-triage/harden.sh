#!/bin/sh
# 키 인증으로 전환합니다. B(10.89.40.22)에서 키를 만들어 서버 deploy 계정에 등록합니다.
SERVER=10.89.40.10
docker exec cr-f9-b ssh-keygen -q -t ed25519 -N '' -f /root/.ssh/id_ed25519
docker exec cr-f9-b cat /root/.ssh/id_ed25519.pub \
  | docker exec -i cr-f9-sshd sh -c 'install -d -m 700 -o deploy -g deploy /home/deploy/.ssh && cat > /home/deploy/.ssh/authorized_keys && chown deploy:deploy /home/deploy/.ssh/authorized_keys && chmod 600 /home/deploy/.ssh/authorized_keys'

# 설정을 적용하기 전에 키로 접속되는지 먼저 확인합니다. 실패하면 여기서 멈춥니다(성공하면 출력이 없습니다).
docker exec cr-f9-b ssh -o StrictHostKeyChecking=no -o PasswordAuthentication=no -o LogLevel=ERROR deploy@$SERVER true   || { echo '키 로그인에 실패해 설정을 적용하지 않았습니다.'; exit 1; }

# 서버 설정을 바꾸고 문법 확인 뒤 다시 읽게 합니다(PID 1 이 sshd 입니다).
docker cp hardening.conf cr-f9-sshd:/etc/ssh/sshd_config.d/10-hardening.conf
docker exec cr-f9-sshd sh -c 'sshd -t && kill -HUP 1'
sleep 1
docker exec cr-f9-sshd sshd -T | grep -E '^(passwordauthentication|permitrootlogin|maxauthtries|logingracetime) '

# 비밀번호 로그인은 거절되고 키 로그인은 됩니다.
echo '--- 비밀번호 로그인'
docker exec cr-f9-b sshpass -p Lab-Pass-2026 ssh -o StrictHostKeyChecking=no -o PubkeyAuthentication=no -o LogLevel=ERROR deploy@$SERVER true 2>&1
echo '--- 키 로그인'
docker exec cr-f9-b ssh -o StrictHostKeyChecking=no -o LogLevel=ERROR deploy@$SERVER 'echo 키 로그인 성공' 2>&1
