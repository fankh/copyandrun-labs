package lab;

import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;

/** 연습용 코드입니다. 일부러 취약하게 만들었으므로 실제 서비스에 쓰지 않습니다. */
public class PasswordUtil {
    public static String hash(String password) throws NoSuchAlgorithmException {
        MessageDigest md = MessageDigest.getInstance("MD5");
        byte[] out = md.digest(password.getBytes(StandardCharsets.UTF_8));
        StringBuilder sb = new StringBuilder();
        for (byte b : out) {
            sb.append(String.format("%02x", b));
        }
        return sb.toString();
    }
}
