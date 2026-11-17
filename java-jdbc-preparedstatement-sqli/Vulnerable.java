import java.sql.Connection;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.ArrayList;
import java.util.List;

/** 연습용 취약 코드입니다. 입력을 문자열로 이어 붙여 SQL 을 만듭니다. 실제 서비스에 쓰지 마십시오. */
public class Vulnerable {
    /** 로그인에 성공한 행의 이름 목록을 돌려줍니다. */
    static List<String> login(Connection c, String name, String password) throws SQLException {
        String sql = "SELECT name FROM users WHERE name = '" + name + "' AND password = '" + password + "'";
        return names(c, sql);
    }

    static List<String> search(Connection c, String keyword, String sort) throws SQLException {
        String sql = "SELECT name FROM items WHERE name LIKE '%" + keyword + "%' ORDER BY " + sort;
        return names(c, sql);
    }

    private static List<String> names(Connection c, String sql) throws SQLException {
        List<String> out = new ArrayList<>();
        try (Statement st = c.createStatement(); ResultSet rs = st.executeQuery(sql)) {
            while (rs.next()) out.add(rs.getString(1));
        }
        return out;
    }
}
