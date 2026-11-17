#!/usr/bin/env bash
# sops 와 age 로 설정 파일의 비밀 값만 암호화하고, 복호화, 키 없음/틀린 키, 변조 감지, 값 수정, 받는 사람 추가까지 확인한다.
# 준비: Docker. 모든 작업은 일회용 alpine 컨테이너 안에서 하고(age, sops 를 설치), 파일은 컨테이너와 함께 사라진다.
# 주의: 이 파일의 키와 비밀 값은 모두 실습용이다. 실제 비밀을 넣지 않는다.
# 실행(Git Bash): bash sops_demo.sh   (약 1분)
export MSYS_NO_PATHCONV=1
docker run --rm -i alpine sh -s <<'INNER'
apk add --no-cache age sops >/dev/null 2>&1
export SOPS_DISABLE_VERSION_CHECK=1 2>/dev/null
cd /tmp && mkdir w && cd w

echo "## 1. 도구 버전과 키 만들기"
echo "age $(age --version), $(sops --version 2>&1 | head -1)"
age-keygen -o key.txt 2>&1 | sed 's/^Public key: /공개 키(받는 사람 주소): /'
PUB=$(grep -o 'age1[a-z0-9]*' key.txt | head -1)

echo "## 2. 평문 설정 파일(secrets.yaml)"
cat > secrets.yaml <<Y
app:
  name: payroll
  debug: false
db:
  host: db.internal
  user: app
  password: S3cr3t-DB-Pass
api:
  token: tok_live_ABC123XYZ
Y
cat secrets.yaml

echo "## 3. .sops.yaml 규칙: password 와 token 값만 암호화"
cat > .sops.yaml <<Y
creation_rules:
  - path_regex: secrets(\.enc)?\.yaml\$
    encrypted_regex: '^(password|token)\$'
    age: $PUB
Y
cat .sops.yaml | sed "s/age1[a-z0-9]*/age1.../"
sops -e secrets.yaml > secrets.enc.yaml
echo "-- 암호화된 파일(secrets.enc.yaml)"
sed 's/ENC\[AES256_GCM,data:\([^,]\{6\}\)[^]]*\]/ENC[...\1...]/; s/age1[a-z0-9]*/age1.../; s/mac: .*/mac: ENC[...]/; s/enc: .*/enc: (age 가 감싼 데이터 키)/' secrets.enc.yaml | grep -v -E '^\s+(-----|[A-Za-z0-9+/=]{20,}$)'
echo "평문 비밀이 파일에 남았나: password=$(grep -c 'S3cr3t' secrets.enc.yaml) token=$(grep -c 'ABC123' secrets.enc.yaml)  (0 이면 남지 않음)"

echo "## 4. 복호화"
SOPS_AGE_KEY_FILE=key.txt sops -d secrets.enc.yaml | grep -E 'password|token'
echo "-- 값 하나만 꺼내기(--extract)"
SOPS_AGE_KEY_FILE=key.txt sops -d --extract '["db"]["password"]' secrets.enc.yaml; echo

echo "## 5. 키가 없거나 틀리면"
echo "-- 키 없음"
sops -d secrets.enc.yaml 2>&1 | head -2 | cut -c1-110
age-keygen -o other.txt >/dev/null 2>&1
echo "-- 다른 사람의 키"
SOPS_AGE_KEY_FILE=other.txt sops -d secrets.enc.yaml 2>&1 | grep -m2 -E 'Failed|did not match' | cut -c1-110

echo "## 6. 변조 감지: 암호화되지 않은 줄(host)과 암호화된 값(token)을 각각 바꿔 본다"
sed 's/host: db.internal/host: evil.example/' secrets.enc.yaml > t1.yaml
SOPS_AGE_KEY_FILE=key.txt sops -d t1.yaml 2>&1 | head -1 | cut -c1-110
awk '/token: ENC/ { sub(/data:./, "data:Z"); } { print }' secrets.enc.yaml > t2.yaml
SOPS_AGE_KEY_FILE=key.txt sops -d t2.yaml 2>&1 | head -1 | cut -c1-110

echo "## 7. 값 수정(sops set)과 변경된 줄 수"
cp secrets.enc.yaml before.yaml
SOPS_AGE_KEY_FILE=key.txt sops set secrets.enc.yaml '["db"]["password"]' '"N3w-DB-Pass"'
echo "-- 바뀐 줄(diff -u 의 - 와 + 줄, 앞 40글자만)"
diff -u before.yaml secrets.enc.yaml | grep '^[-+] ' | cut -c1-40
SOPS_AGE_KEY_FILE=key.txt sops -d --extract '["db"]["password"]' secrets.enc.yaml; echo

echo "## 8. 받는 사람 추가(updatekeys): 팀원의 키로도 열 수 있게"
PUB2=$(grep -o 'age1[a-z0-9]*' other.txt | head -1)
sed "s/age: \(age1[a-z0-9]*\)/age: \1,$PUB2/" .sops.yaml > .sops.yaml.new && mv .sops.yaml.new .sops.yaml
SOPS_AGE_KEY_FILE=key.txt sops updatekeys -y secrets.enc.yaml 2>&1 | tail -1
echo "받는 사람 수: $(grep -c 'recipient: age1' secrets.enc.yaml)"
echo "-- 새 키(other.txt)로 복호화"
SOPS_AGE_KEY_FILE=other.txt sops -d --extract '["api"]["token"]' secrets.enc.yaml; echo
INNER
