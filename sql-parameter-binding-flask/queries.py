import sqlite3

SQL_LOG = []  # 테스트 전용: 실행 직전의 (SQL 문장, 파라미터)를 남긴다.
# 운영 환경에서는 비밀번호 같은 파라미터를 로그에 남기지 마세요


def run(db_path, sql, params=()):
    SQL_LOG.append((sql, params))
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    try:
        return conn.execute(sql, params).fetchall()
    finally:
        conn.close()


def init_db(db_path):
    conn = sqlite3.connect(db_path)
    conn.executescript("""
    DROP TABLE IF EXISTS members;
    CREATE TABLE members (id INTEGER PRIMARY KEY, name TEXT, username TEXT, password TEXT, joined TEXT);
    """)
    conn.executemany("INSERT INTO members (name, username, password, joined) VALUES (?, ?, ?, ?)", [
        ("kim", "kim", "pw-kim", "2024-03-01"),
        ("lee", "lee", "pw-lee", "2024-01-15"),
        ("park", "park", "pw-park", "2024-02-10"),
        ("O'Brien", "obrien", "pw-obrien", "2024-04-05"),
        ("a_b", "ab", "pw-ab", "2024-05-20"),
    ])
    conn.commit()
    conn.close()


SEARCH_SQL = {
    "name": "SELECT id, name FROM members WHERE name LIKE ? ESCAPE '!' ORDER BY name",
    "joined": "SELECT id, name FROM members WHERE name LIKE ? ESCAPE '!' ORDER BY joined",
}


def escape_like(text):
    return text.replace("!", "!!").replace("%", "!%").replace("_", "!_")


def search_members(db_path, name, sort):
    if sort not in SEARCH_SQL:
        raise ValueError("허용되지 않는 정렬 기준입니다")
    return run(db_path, SEARCH_SQL[sort], ("%" + escape_like(name) + "%",))


def find_user(db_path, username, password):
    rows = run(db_path, "SELECT id, username FROM members WHERE username = ? AND password = ?",
               (username, password))
    return rows[0] if rows else None
