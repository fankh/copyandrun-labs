-- 관리자 역할, 키를 환경 변수에서 읽어 바인드 매개변수로 넘기는 방식입니다(psql 16 이상).
\getenv key LAB_KEY
SELECT set_config('app.key', $1, false) IS NOT NULL AS key_set \bind :key \g
SELECT * FROM customers_plain ORDER BY id;
