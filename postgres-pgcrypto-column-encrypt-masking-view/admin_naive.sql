-- 관리자 역할, 키를 SQL 문에 직접 쓰는 방식입니다. 서버 로그에 키가 남습니다.
SET app.key = 'lab-key-2026';
SELECT * FROM customers_plain ORDER BY id;
