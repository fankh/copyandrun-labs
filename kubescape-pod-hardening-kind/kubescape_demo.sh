#!/usr/bin/env bash
# 약한 파드와 단단하게 만든 파드를 kubescape 로 점검하고, kind 클러스터의 Pod Security Admission 으로 실제 배포 결과와 대조한다.
# 준비: Docker, kind 0.33.0(PATH 에 있거나 KIND 환경 변수로 지정), kubectl, python, 같은 폴더에 weak.yaml, hardened.yaml, ks_summary.py.
# 주의: 내 kubectl 의 현재 컨텍스트(회사 클러스터 등)를 건드리지 않도록 모든 kubectl 에 --kubeconfig 를 붙인다.
# 실행(Git Bash): bash kubescape_demo.sh   (약 3분)
export MSYS_NO_PATHCONV=1
HERE="$(pwd)"
OUT=../osk-ks-out                      # 결과 폴더는 매니페스트 폴더 밖에 둔다
rm -rf "$OUT"; mkdir -p "$OUT"; ABS="$(cd "$OUT" && pwd)"
KIND="${KIND:-kind}"
KC="$ABS/kubeconfig"
K() { kubectl --kubeconfig "$KC" "$@"; }
cleanup() { "$KIND" delete cluster --name osk-sec --kubeconfig "$KC" >/dev/null 2>&1; }
cleanup

echo "## 1. kubescape 로 매니페스트 파일 점검(클러스터 없이)"
for n in weak hardened; do
  docker run --rm -v "$HERE:/w:ro" -v "$ABS:/out" quay.io/kubescape/kubescape-cli:latest \
    scan /w/$n.yaml --format json --output /out/$n.json >/dev/null 2>&1
  python ks_summary.py "$OUT/$n.json" | sed -n '1,3p'
  python ks_summary.py "$OUT/$n.json" >/dev/null; echo "  필수 통제 게이트 종료 코드: $?"
done

echo "## 2. kind 클러스터에서 실제 배포 결과 대조"
"$KIND" create cluster --name osk-sec --kubeconfig "$KC" --wait 120s >/dev/null 2>&1
K create namespace lab >/dev/null
K label namespace lab pod-security.kubernetes.io/enforce=restricted >/dev/null
K create namespace lab-open >/dev/null
echo "  lab 네임스페이스: Pod Security 'restricted' 강제, lab-open: 제한 없음"

echo "### 2-1. weak 를 lab 에 배포"
K apply -f weak.yaml 2>&1 | cut -c1-200
echo "### 2-2. hardened 를 lab 에 배포"
K apply -f hardened.yaml
K -n lab wait --for=condition=Ready pod/hardened --timeout=90s >/dev/null
echo "### 2-3. weak 를 제한 없는 lab-open 에 배포"
sed 's/namespace: lab$/namespace: lab-open/' weak.yaml | K apply -f -
K -n lab-open wait --for=condition=Ready pod/weak --timeout=90s >/dev/null

echo "## 3. 두 파드 안에서 실제로 확인"
for spec in "lab hardened" "lab-open weak"; do
  set -- $spec
  echo "### $2"
  echo -n "  사용자: ";           K -n $1 exec $2 -- id
  echo -n "  CapEff: ";           K -n $1 exec $2 -- sh -c "grep CapEff /proc/self/status | cut -f2"
  echo -n "  / 에 파일 쓰기: ";   K -n $1 exec $2 -- sh -c 'touch /probe && echo 성공' 2>&1 | grep -E 'Read-only|성공'
done
cleanup
echo "## 끝"
