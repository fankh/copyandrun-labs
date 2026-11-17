# 풀기만 합니다. 푼 결과를 Invoke-Expression 으로 실행하지 않고 화면에 문자열로만 찍습니다.
$line = Get-Content ./samples/sample1.txt -Raw
$b64 = ($line -split 'EncodedCommand\s+')[1].Trim()
$text = [Text.Encoding]::Unicode.GetString([Convert]::FromBase64String($b64))
Write-Output "풀린 문자열: $text"
