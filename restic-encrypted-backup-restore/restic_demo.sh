#!/usr/bin/env bash
# restic 으로 암호화 백업을 만들고, 두 번째 백업의 증가분, 복원 검증, 저장소 손상 감지, 오래된 스냅샷 정리까지 한다.
# 준비: Docker. restic 은 컨테이너(restic/restic)로 실행하고 모든 데이터는 도커 볼륨 안에서만 다룬다.
# 주의: 볼륨 osk_rs_repo, osk_rs_src, osk_rs_out 을 만들고 끝에서 지운다. 비밀번호는 실습용 값이다.
# 실행(Git Bash): bash restic_demo.sh   (약 1분)
set -u
export MSYS_NO_PATHCONV=1
PW="lab-only-restic-pass"
R() { docker run --rm -e RESTIC_PASSWORD="$PW" -v osk_rs_repo:/repo -v osk_rs_src:/data -v osk_rs_out:/out restic/restic -r /repo "$@"; }
SH() { docker run --rm -v osk_rs_repo:/repo -v osk_rs_src:/data -v osk_rs_out:/out alpine sh -c "$1"; }

docker volume rm osk_rs_repo osk_rs_src osk_rs_out >/dev/null 2>&1
docker volume create osk_rs_repo >/dev/null; docker volume create osk_rs_src >/dev/null; docker volume create osk_rs_out >/dev/null

echo "## 1. 백업할 원본 파일 만들기"
SH 'mkdir -p /data/docs /data/photos
for i in 1 2 3 4 5; do echo "회의록 $i: 이 파일은 실습용입니다." > /data/docs/note$i.txt; done
head -c 3000000 /dev/urandom > /data/photos/pic1.bin
head -c 2000000 /dev/urandom > /data/photos/pic2.bin
du -sk /data | cut -f1 | sed "s/^/원본 크기(KB): /"; find /data -type f | wc -l | sed "s/^/파일 수: /"'

echo "## 2. 저장소 만들기(init)와 첫 백업(--host lab 으로 이름을 고정해 이전 스냅샷과 비교되게 한다)"
R init 2>&1 | grep -E 'created restic repository'
R backup --host lab /data 2>&1 | grep -E 'Files:|Added to the repository|snapshot .* saved'

echo "## 3. 저장소 안을 들여다보기: 평문이 보이는가"
SH 'ls /repo | tr "
" " "; echo; grep -r -l "회의록" /repo 2>/dev/null | wc -l | sed "s/^/저장소 파일 중 평문 \"회의록\"이 든 것: /"'

echo "## 4. 파일 하나를 추가하고 하나를 고친 뒤 두 번째 백업(증가분만 저장되는가)"
SH 'echo "회의록 6: 새로 추가한 파일" > /data/docs/note6.txt; echo "수정함" >> /data/docs/note1.txt'
R backup --host lab /data 2>&1 | grep -E 'Files:|Added to the repository|snapshot .* saved'

echo "## 5. 복원하고 원본과 비교(diff)"
R restore latest --target /out 2>&1 | tail -1
SH 'diff -r /data /out/data && echo "원본과 복원본이 같다(diff 결과 없음)"'

echo "## 6. 잘못된 비밀번호"
docker run --rm -e RESTIC_PASSWORD="wrong" -v osk_rs_repo:/repo restic/restic -r /repo snapshots 2>&1 | tail -1

echo "## 7. 스냅샷을 세 개로 늘리고 두 개만 남기도록 정리(forget --keep-last 2 --prune)"
SH 'echo "회의록 7" > /data/docs/note7.txt'
R backup --host lab /data 2>&1 | grep -E 'snapshot .* saved'
R snapshots 2>&1 | grep -E 'snapshots$'
R forget --keep-last 2 --prune 2>&1 | grep -E 'keep|remove|snapshots$'
R snapshots 2>&1 | grep -E 'snapshots$'

echo "## 8. 저장소 점검(check)과 손상 감지(check --read-data)"
R check 2>&1 | tail -1
SH 'f=$(ls -S /repo/data/*/* | head -1); echo "가장 큰 데이터 파일을 손상시킨다: $(basename $f | cut -c1-16)..."; head -c 8 /dev/zero | dd of=$f bs=1 seek=100000 conv=notrunc 2>/dev/null'
echo "-- 기본 check (구조만 본다)"
R check 2>&1 | tail -1
echo "-- check --read-data (내용까지 읽는다)"
R check --read-data 2>&1 | grep -E 'Fatal|ciphertext verification failed' | head -2 | cut -c1-150
echo "-- 손상된 저장소에서 복원 시도"
R restore latest --target /out2 2>&1 | grep -E 'Fatal|error|ciphertext' | head -2 | cut -c1-150

docker volume rm osk_rs_repo osk_rs_src osk_rs_out >/dev/null && echo "## 정리: 시험 볼륨 삭제"
