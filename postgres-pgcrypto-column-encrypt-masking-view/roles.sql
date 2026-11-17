-- 상담원(cr_agent)은 마스킹 뷰만, 관리자(cr_admin)는 복호화 뷰까지 읽습니다.
CREATE ROLE cr_agent LOGIN;
CREATE ROLE cr_admin LOGIN;

REVOKE ALL ON customers FROM PUBLIC;

CREATE VIEW customers_masked AS
  SELECT id, left(name, 1) || '**' AS name, phone_mask AS phone
  FROM customers;

CREATE VIEW customers_plain AS
  SELECT id, name, pgp_sym_decrypt(phone_enc, current_setting('app.key')) AS phone
  FROM customers;

GRANT SELECT ON customers_masked TO cr_agent, cr_admin;
GRANT SELECT ON customers_plain  TO cr_admin;
