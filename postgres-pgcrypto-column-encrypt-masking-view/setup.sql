-- 확장과 표를 만듭니다. 전화번호는 암호문(phone_enc), 검색용 해시(phone_idx), 마스킹 값(phone_mask)으로 나눠 저장합니다.
CREATE EXTENSION IF NOT EXISTS pgcrypto;
CREATE EXTENSION IF NOT EXISTS pg_stat_statements;

CREATE TABLE customers (
  id          serial PRIMARY KEY,
  name        text  NOT NULL,
  phone_enc   bytea NOT NULL,
  phone_idx   bytea NOT NULL,
  phone_mask  text  NOT NULL
);
CREATE INDEX customers_phone_idx ON customers (phone_idx);
