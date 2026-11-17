import com.sun.net.httpserver.HttpExchange;
import com.sun.net.httpserver.HttpServer;
import java.io.IOException;
import java.net.InetSocketAddress;
import java.net.URLDecoder;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.List;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.apache.logging.log4j.core.LoggerContext;

public class WebApp {
    private static final Logger log = LogManager.getLogger(WebApp.class);
    private static final Path LOG_FILE = Path.of("/tmp/app.log");
    private static final String CSS = "body{font-family:'Malgun Gothic',sans-serif;max-width:720px;margin:40px auto;color:#1f2933}"
            + "h1{font-size:24px}.ver{color:#52606d;font-size:14px}input{display:block;margin:8px 0 16px;padding:10px;width:100%;"
            + "box-sizing:border-box;font-size:16px}button{padding:10px 20px;font-size:16px}"
            + "pre{background:#0d1117;color:#e6edf3;padding:16px;overflow:auto;font-size:14px;line-height:1.6}"
            + ".err{color:#b42318;font-weight:bold}a{color:#1d4ed8}";

    public static void main(String[] args) throws IOException {
        HttpServer server = HttpServer.create(new InetSocketAddress(8080), 0);
        server.createContext("/", WebApp::index);
        server.createContext("/login", WebApp::login);
        server.createContext("/logs", WebApp::logs);
        server.start();
        log.info("started");
    }

    private static String version() {
        String v = LoggerContext.class.getPackage().getImplementationVersion();
        return v == null ? "unknown" : v;
    }

    private static String esc(String s) {
        return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;");
    }

    private static String page(String body) {
        return "<!doctype html><html lang=ko><meta charset=utf-8><title>Log4j 시험 앱</title><style>" + CSS + "</style>"
                + "<h1>Log4j 시험 앱</h1><div class=ver>log4j-core " + version() + "</div>" + body;
    }

    private static void send(HttpExchange ex, String html) throws IOException {
        byte[] out = html.getBytes(StandardCharsets.UTF_8);
        ex.getResponseHeaders().add("Content-Type", "text/html; charset=utf-8");
        ex.sendResponseHeaders(200, out.length);
        ex.getResponseBody().write(out);
        ex.close();
    }

    private static void index(HttpExchange ex) throws IOException {
        send(ex, page("<h2>로그인</h2><form method=post action=/login>"
                + "아이디<input name=username autocomplete=off>"
                + "암호<input name=password type=password>"
                + "<button>로그인</button></form><p><a href=/logs>서버 로그 보기</a></p>"));
    }

    private static void login(HttpExchange ex) throws IOException {
        String body = new String(ex.getRequestBody().readAllBytes(), StandardCharsets.UTF_8);
        String username = "";
        for (String pair : body.split("&")) {
            if (pair.startsWith("username=")) {
                username = URLDecoder.decode(pair.substring(9), StandardCharsets.UTF_8);
            }
        }
        // 사용자가 보낸 값을 그대로 로그 메시지에 붙이는 흔한 실수
        log.error("login failed, user: " + username);
        send(ex, page("<p class=err>로그인에 실패했습니다.</p><p><a href=/logs>서버 로그 보기</a> | <a href=/>다시 시도</a></p>"));
    }

    private static void logs(HttpExchange ex) throws IOException {
        List<String> lines = Files.exists(LOG_FILE) ? Files.readAllLines(LOG_FILE) : List.of();
        List<String> tail = lines.subList(Math.max(0, lines.size() - 12), lines.size());
        send(ex, page("<h2>서버 로그</h2><pre>" + esc(String.join("\n", tail)) + "</pre><p><a href=/>처음으로</a></p>"));
    }
}
