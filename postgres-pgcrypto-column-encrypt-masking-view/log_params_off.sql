-- 바인드 매개변수 값을 서버 로그에 남기지 않도록 합니다(0 이면 매개변수 값을 기록하지 않음).
ALTER SYSTEM SET log_parameter_max_length = 0;
SELECT pg_reload_conf();
