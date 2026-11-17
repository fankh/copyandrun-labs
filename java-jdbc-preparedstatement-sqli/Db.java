import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;
import java.sql.Statement;

/** 연습용 H2 인메모리 DB. 비밀번호는 연습 편의상 평문으로 두었습니다(실제 저장 방식은 아닙니다). */
public class Db {
    // DB_CLOSE_DELAY 는 관리자만 줄 수 있는 옵션이므로 sa 연결에만 붙입니다.
    static final String ADMIN_URL = "jdbc:h2:mem:lab;DB_CLOSE_DELAY=-1";
    static final String APP_URL = "jdbc:h2:mem:lab";

    /** 관리 계정(sa)으로 표와 데이터를 만들고, 읽기 전용 계정 lab_app 을 만듭니다. */
    static void init() throws SQLException {
        try (Connection c = DriverManager.getConnection(ADMIN_URL, "sa", "");
             Statement s = c.createStatement()) {
            s.execute("CREATE TABLE users(id INT PRIMARY KEY, name VARCHAR(20), password VARCHAR(30), role VARCHAR(10))");
            s.execute("INSERT INTO users VALUES (1,'alice','alice-pw-1','user'), (2,'carol','carol-pw-2','user'), (3,'admin','admin-pw-3','admin')");
            s.execute("CREATE TABLE items(id INT PRIMARY KEY, name VARCHAR(30), owner VARCHAR(20), price INT)");
            s.execute("INSERT INTO items VALUES (1,'노트북 거치대','alice',32000), (2,'기계식 키보드','alice',89000),"
                    + " (3,'모니터 암','carol',54000), (4,'USB 허브','carol',21000), (5,'비공개 감사 자료','admin',0)");
            s.execute("CREATE USER lab_app PASSWORD 'lab-app-pw'");
            s.execute("GRANT SELECT ON users TO lab_app");
            s.execute("GRANT SELECT ON items TO lab_app");
        }
    }

    /** 앱이 쓰는 연결입니다. SELECT 권한만 가진 lab_app 으로 접속합니다. */
    static Connection appConnection() throws SQLException {
        return DriverManager.getConnection(APP_URL, "lab_app", "lab-app-pw");
    }
}
