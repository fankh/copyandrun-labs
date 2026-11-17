package lab;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;

public class UserRepo {
    private final String url;

    public UserRepo(String url) {
        this.url = url;
    }

    public String findEmail(String name) throws SQLException {
        String password = System.getenv("DB_PASSWORD");
        if (password == null) {
            throw new IllegalStateException("DB_PASSWORD 환경 변수가 필요합니다");
        }
        try (Connection conn = DriverManager.getConnection(url, "app", password);
             PreparedStatement st = conn.prepareStatement("SELECT email FROM users WHERE name = ?")) {
            st.setString(1, name);
            try (ResultSet rs = st.executeQuery()) {
                return rs.next() ? rs.getString(1) : null;
            }
        }
    }
}
