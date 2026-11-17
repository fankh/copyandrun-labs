package com.example;

import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import java.io.InvalidClassException;
import java.io.ObjectInputFilter;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.util.ArrayList;
import java.util.List;

public class App {
    static byte[] toBytes(Object o) throws Exception {
        ByteArrayOutputStream buf = new ByteArrayOutputStream();
        try (ObjectOutputStream out = new ObjectOutputStream(buf)) {
            out.writeObject(o);
        }
        return buf.toByteArray();
    }

    // pattern 이 null 이면 필터를 따로 지정하지 않습니다(JVM 전역 필터가 있으면 그것이 적용됩니다).
    static void tryRead(String title, byte[] data, String pattern) {
        System.out.println("== " + title + " | 필터: " + (pattern == null ? "지정 안 함" : pattern) + " | " + data.length + " bytes");
        try (ObjectInputStream in = new ObjectInputStream(new ByteArrayInputStream(data))) {
            if (pattern != null) {
                in.setObjectInputFilter(ObjectInputFilter.Config.createFilter(pattern));
            }
            Object o = in.readObject();
            System.out.println("  결과: " + o.getClass().getSimpleName() + " 객체가 만들어졌습니다. " + (o instanceof Node ? "" : o));
        } catch (InvalidClassException e) {
            System.out.println("  거절됨: InvalidClassException " + e.getMessage());
        } catch (Exception e) {
            System.out.println("  오류: " + e);
        }
    }

    public static void main(String[] args) throws Exception {
        String scenario = args.length > 0 ? args[0] : "basic";
        byte[] safe = toBytes(new Safe("report", 3));
        byte[] dangerous = toBytes(new Dangerous("연습용 데이터"));

        switch (scenario) {
            case "basic" -> {
                String allow = "com.example.Safe;!*";
                tryRead("Safe 바이트", safe, null);
                tryRead("Dangerous 바이트", dangerous, null);
                tryRead("Safe 바이트", safe, allow);
                tryRead("Dangerous 바이트", dangerous, allow);
            }
            case "cast" -> {
                System.out.println("== Dangerous 바이트를 필터 없이 읽고 Safe 로 형변환");
                try (ObjectInputStream in = new ObjectInputStream(new ByteArrayInputStream(dangerous))) {
                    Safe s = (Safe) in.readObject();
                    System.out.println("  " + s);
                } catch (ClassCastException e) {
                    System.out.println("  형변환 실패: ClassCastException (readObject 코드는 이미 실행된 뒤입니다)");
                }
            }
            case "limits" -> {
                String rule = "maxdepth=5;maxarray=1000;com.example.*;!*";
                tryRead("Node 3단계", toBytes(Node.chain(3)), rule);
                tryRead("Node 10단계", toBytes(Node.chain(10)), rule);
                tryRead("Blob 배열 100개", toBytes(new Blob(100)), rule);
                tryRead("Blob 배열 5000개", toBytes(new Blob(5000)), rule);
                String bytesRule = "maxbytes=1000;com.example.*;!*";
                tryRead("Blob 배열 100개", toBytes(new Blob(100)), bytesRule);
                tryRead("Blob 배열 5000개", toBytes(new Blob(5000)), bytesRule);
            }
            case "pitfall" -> {
                tryRead("Dangerous 바이트", dangerous, "com.example.Safe");
                byte[] list = toBytes(new ArrayList<>(List.of(new Safe("a", 1), new Safe("b", 2))));
                tryRead("Safe 목록(ArrayList)", list, "com.example.Safe;!*");
                tryRead("Safe 목록(ArrayList)", list, "com.example.Safe;java.util.ArrayList;java.lang.Object;!*");
            }
            case "global" -> {
                System.out.println("== JVM 전역 필터: " + ObjectInputFilter.Config.getSerialFilter());
                tryRead("Safe 바이트", safe, null);
                tryRead("Dangerous 바이트", dangerous, null);
            }
            default -> System.out.println("사용법: App basic | cast | limits | pitfall | global");
        }
    }
}
