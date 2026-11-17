package lab;

import java.util.Random;

/** 화면 배지 색만 고르는 코드입니다. 보안 값 생성에는 쓰지 않습니다. */
public class BadgeColor {
    private static final String[] COLORS = {"blue", "green", "orange", "gray"};
    private static final Random RANDOM = new Random();

    public static String pick() {
        return COLORS[RANDOM.nextInt(COLORS.length)];
    }
}
