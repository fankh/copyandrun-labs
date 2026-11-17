-- 암호문 컬럼의 검색 한계를 확인합니다. 표를 직접 읽어야 하므로 DB 소유자(postgres)로 실행하고, 키는 환경 변수에서 읽습니다.
\getenv key LAB_KEY
SELECT set_config('app.key', $1, false) IS NOT NULL AS key_set \bind :key \g

-- 1) 같은 값을 두 번 암호화하면 암호문이 다릅니다.
SELECT pgp_sym_encrypt('010-5550-1001', current_setting('app.key'))
     = pgp_sym_encrypt('010-5550-1001', current_setting('app.key')) AS same_ciphertext;

-- 2) 암호문 컬럼에 대한 직접 비교는 일치하는 행이 없습니다.
SELECT count(*) AS direct_match FROM customers
WHERE phone_enc = pgp_sym_encrypt('010-5550-1001', current_setting('app.key'));

-- 3) 복호화해서 비교하면 맞지만 모든 행을 풀어 봅니다(인덱스를 못 씁니다).
SET enable_seqscan = off;
EXPLAIN (COSTS OFF)
SELECT id FROM customers
WHERE pgp_sym_decrypt(phone_enc, current_setting('app.key')) = '010-5550-1003';

-- 4) 해시 컬럼 phone_idx 로는 같은 값 검색에 인덱스를 씁니다.
EXPLAIN (COSTS OFF)
SELECT id FROM customers
WHERE phone_idx = hmac('010-5550-1003', current_setting('app.key'), 'sha256');
SELECT id FROM customers
WHERE phone_idx = hmac('010-5550-1003', current_setting('app.key'), 'sha256');
