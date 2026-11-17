import java.sql.Connection;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.List;
import java.util.concurrent.Callable;

/** 같은 입력을 취약 코드와 수정 코드에 넣고 결과를 표로 찍습니다. */
public class App {
    static String run(Callable<List<String>> job) {
        try {
            List<String> rows = job.call();
            return rows.size() + "행 " + rows;
        } catch (Exception e) {
            String msg = String.valueOf(e.getMessage()).replace('\n', ' ');
            return "오류 " + (msg.length() > 48 ? msg.substring(0, 48) + "..." : msg);
        }
    }

    static void row(String id, String input, String bad, String good) {
        System.out.println(id + " | " + input);
        System.out.println("     취약: " + bad);
        System.out.println("     수정: " + good);
    }

    public static void main(String[] args) throws SQLException {
        Db.init();
        try (Connection c = Db.appConnection()) {
            System.out.println("== 로그인 (users 3행) ==");
            String[][] logins = {
                {"L1 정상 입력", "alice", "alice-pw-1"},
                {"L2 틀린 비밀번호", "alice", "wrong"},
                {"L3 참 조건 덧붙이기", "alice", "' OR '1'='1"},
                {"L4 주석으로 뒤쪽 제거", "admin'--", "아무거나"},
            };
            for (String[] t : logins) {
                row(t[0], t[1] + " / " + t[2],
                    run(() -> Vulnerable.login(c, t[1], t[2])),
                    run(() -> Fixed.login(c, t[1], t[2])));
            }

            System.out.println("== 검색과 정렬 (items 5행) ==");
            String[][] searches = {
                {"S1 정상 검색", "키보드", "price"},
                {"S2 참 조건 덧붙이기", "zzz' OR '1'='1' -- ", "id"},
                {"S3 정렬 자리에 엉뚱한 값", "USB", "bogus"},
                {"S4 정렬 자리에 허용 안 된 식", "USB", "id, (SELECT 1)"},
            };
            for (String[] t : searches) {
                row(t[0], "키워드=" + t[1] + " 정렬=" + t[2],
                    run(() -> Vulnerable.search(c, t[1], t[2])),
                    run(() -> Fixed.search(c, t[1], t[2])));
            }

            System.out.println("== 바인딩이 해 주지 않는 것 ==");
            System.out.println("B1 LIKE 에 % 를 넣고 바인딩만 한 검색: "
                + run(() -> Fixed.searchNoEscape(c, "%")));
            System.out.println("B2 같은 입력을 % 이스케이프한 검색:    "
                + run(() -> Fixed.search(c, "%", "id")));
            System.out.println("B3 ORDER BY ? 에 price 를 바인딩:       "
                + run(() -> Fixed.sortByBinding(c, "price")));

            System.out.println("== 최소 권한 계정 lab_app ==");
            try (Statement st = c.createStatement()) {
                st.executeUpdate("DELETE FROM items");
                System.out.println("P1 DELETE: 실행됨");
            } catch (SQLException e) {
                System.out.println("P1 DELETE: 거부 (" + e.getMessage().split("\n")[0] + ")");
            }
        }
    }
}
