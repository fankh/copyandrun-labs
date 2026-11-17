package com.example;

import java.io.IOException;
import java.io.ObjectInputStream;
import java.io.Serializable;

// 연습용 클래스입니다. readObject 에서 로그 한 줄만 남기며, 그 외에는 아무 일도 하지 않습니다.
public class Dangerous implements Serializable {
    private static final long serialVersionUID = 1L;

    public final String note;

    public Dangerous(String note) {
        this.note = note;
    }

    private void readObject(ObjectInputStream in) throws IOException, ClassNotFoundException {
        in.defaultReadObject();
        System.out.println("  [Dangerous.readObject] 역직렬화 중에 이 코드가 실행되었습니다. note=" + note);
    }

    @Override
    public String toString() {
        return "Dangerous[note=" + note + "]";
    }
}
