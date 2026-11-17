-- 가짜 고객 5명을 넣습니다. 실행할 때 psql -v key=... 로 키를 넘깁니다(:'key' 는 클라이언트가 문자열로 펼칩니다).
INSERT INTO customers (name, phone_enc, phone_idx, phone_mask)
SELECT n,
       pgp_sym_encrypt(p, :'key', 'cipher-algo=aes256'),
       hmac(p, :'key', 'sha256'),
       regexp_replace(p, '^(\d{3}-)\d{4}(-\d{4})$', '\1****\2')
FROM (VALUES
  ('김하늘', '010-5550-1001'),
  ('이도윤', '010-5550-1002'),
  ('박서준', '010-5550-1003'),
  ('최지우', '010-5550-1004'),
  ('정민아', '010-5550-1005')
) AS t(n, p);
