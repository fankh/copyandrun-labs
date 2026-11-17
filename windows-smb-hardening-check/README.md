# Windows SMB 점검: SMBv1 끄기, 서명 요구, 공유 감사

Windows 11에서 SMBv1이 꺼져 있는지, 서버와 클라이언트가 서명을 요구하는지, 사용자가 만든 공유가 있는지, 공유 접근 감사가 켜져 있는지를 PowerShell 스크립트 하나로 읽고 결과를 해석합니다.

글: https://copyandrun.com/blog/windows-smb-hardening-check/

## 파일

- `Get-SmbHardening.ps1`
- `Test-SmbChanges.ps1`

## 사용 방법

글의 순서대로 이 폴더에서 명령을 실행합니다.

연습용 코드입니다. 취약한 예제와 실습용 비밀번호가 들어 있으므로 운영 환경에 쓰지 않습니다. 개인키와 비밀번호 파일은 포함하지 않았습니다.
