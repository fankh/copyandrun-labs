#!/bin/sh
# 연습용 ext4 이미지를 만듭니다. 마운트하지 않고 mke2fs -d 와 debugfs 만 씁니다.
set -e
export TZ=UTC
chmod u+w evidence.img 2>/dev/null || true
rm -rf tree evidence.img evidence.sha256 debugfs.cmd
mkdir -p tree/docs tree/tmp

# 1. 이미지에 넣을 시험 파일 (모두 직접 만든 가짜 내용)
printf 'Quarterly report draft\nline 2\n' > tree/docs/report.txt
printf 'Meeting memo: lab schedule moved to Friday\n' > tree/docs/memo.txt
printf 'test-token=NOT-A-REAL-SECRET-0000\n' > tree/tmp/scratch.txt
printf 'keep this file\n' > tree/readme.txt

# 2. 파일 시간 고정 (touch -d)
touch -d '2026-10-20 09:00:00' tree/docs/report.txt tree/readme.txt
touch -d '2026-10-21 10:15:00' tree/docs/memo.txt
touch -d '2026-10-22 11:00:00' tree/tmp/scratch.txt

# 3. 8MB ext4 이미지 생성 (-I 256 은 생성 시각(crtime)을 담는 inode 크기)
truncate -s 8M evidence.img
mke2fs -q -t ext4 -I 256 -O ^has_journal -L LABTEST -d tree evidence.img

# 4. debugfs 로 나머지 시간을 고정하고, 수정과 삭제 흔적을 만듭니다
#    ctime 은 파일을 고치거나 지울 때 커널이 바꾸는 값을 흉내 내어 직접 적습니다
cat > debugfs.cmd <<'CMD'
sif /readme.txt crtime 20261020090000
sif /readme.txt ctime 20261020090000
sif /docs/report.txt crtime 20261020090000
sif /docs/report.txt mtime 20261025143000
sif /docs/report.txt ctime 20261025143000
sif /docs/memo.txt crtime 20261021101500
sif /tmp/scratch.txt crtime 20261022110000
sif /lost+found mtime 20261020090000
sif /lost+found ctime 20261020090000
sif /lost+found atime 20261020090000
sif /lost+found crtime 20261020090000
sif /docs atime 20261020090000
sif /docs crtime 20261020090000
sif /tmp atime 20261020090000
sif /tmp crtime 20261020090000
sif /docs/memo.txt ctime 20261027184000
sif /docs mtime 20261027184000
sif /docs ctime 20261027184000
set_current_time 20261027184000
rm /docs/memo.txt
sif /tmp/scratch.txt ctime 20261027184500
sif /tmp mtime 20261027184500
sif /tmp ctime 20261027184500
set_current_time 20261027184500
rm /tmp/scratch.txt
CMD
debugfs -w -f debugfs.cmd evidence.img > /dev/null

# 5. 원본 해시를 먼저 기록하고 읽기 전용으로 둡니다
sha256sum evidence.img > evidence.sha256
chmod 444 evidence.img
cat evidence.sha256
