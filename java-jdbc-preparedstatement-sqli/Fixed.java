import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;

/** 같은 기능을 PreparedStatement 로 고친 코드입니다. 값은 바인딩하고, 바인딩이 안 되는 자리는 허용 목록으로 고릅니다. */
public class Fixed {
    /** 정렬 기준 이름을 SQL 조각으로 바꾸는 허용 목록입니다. 사용자 입력은 키로만 쓰고 SQL 에 넣지 않습니다. */
    static final Map<String, String> SORT = Map.of("name", "name", "price", "price", "id", "id");

    static List<String> login(Connection c, String name, String password) throws SQLException {
        String sql = "SELECT name FROM users WHERE name = ? AND password = ?";
        try (PreparedStatement ps = c.prepareStatement(sql)) {
            ps.setString(1, name);
            ps.setString(2, password);
            return names(ps);
        }
    }

    static List<String> search(Connection c, String keyword, String sort) throws SQLException {
        String column = SORT.get(sort);
        if (column == null) throw new IllegalArgumentException("허용하지 않는 정렬 기준: " + sort);
        // LIKE 의 % 와 _ 도 값 안에서는 와일드카드이므로 \ 로 막고 ESCAPE 를 지정합니다.
        String escaped = keyword.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_");
        String sql = "SELECT name FROM items WHERE name LIKE ? ESCAPE '\\' ORDER BY " + column;
        try (PreparedStatement ps = c.prepareStatement(sql)) {
            ps.setString(1, "%" + escaped + "%");
            return names(ps);
        }
    }

    /** 비교용: 키워드를 바인딩만 하고 와일드카드는 막지 않은 검색입니다. */
    static List<String> searchNoEscape(Connection c, String keyword) throws SQLException {
        try (PreparedStatement ps = c.prepareStatement("SELECT name FROM items WHERE name LIKE ? ORDER BY id")) {
            ps.setString(1, "%" + keyword + "%");
            return names(ps);
        }
    }

    /** 비교용: ORDER BY 자리에 ? 를 쓴 잘못된 시도입니다. */
    static List<String> sortByBinding(Connection c, String sort) throws SQLException {
        try (PreparedStatement ps = c.prepareStatement("SELECT name FROM items ORDER BY ?")) {
            ps.setString(1, sort);
            return names(ps);
        }
    }

    private static List<String> names(PreparedStatement ps) throws SQLException {
        List<String> out = new ArrayList<>();
        try (ResultSet rs = ps.executeQuery()) {
            while (rs.next()) out.add(rs.getString(1));
        }
        return out;
    }
}
