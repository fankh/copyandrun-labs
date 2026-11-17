package lab;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;

/** 연습용 코드입니다. 일부러 취약하게 만들었으므로 실제 서비스에 쓰지 않습니다. */
public class UserRepo {
    private static final String DB_PASSWORD = "Lab-Pass-2026";

    private final String url;

    public UserRepo(String url) {
        this.url = url;
    }

    public String findEmail(String name) throws SQLException {
        try (Connection conn = DriverManager.getConnection(url, "app", DB_PASSWORD);
             Statement st = conn.createStatement();
             ResultSet rs = st.executeQuery("SELECT email FROM users WHERE name = '" + name + "'")) {
            return rs.next() ? rs.getString(1) : null;
        }
    }
}
