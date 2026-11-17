-- 상담원 역할로 실행합니다. 첫 문장만 성공하고 나머지 둘은 권한 오류가 나야 합니다.
SELECT * FROM customers_masked ORDER BY id;
SELECT * FROM customers;
SELECT * FROM customers_plain;
