package com.example;

import java.io.Serializable;

public class Safe implements Serializable {
    private static final long serialVersionUID = 1L;

    public final String name;
    public final int count;

    public Safe(String name, int count) {
        this.name = name;
        this.count = count;
    }

    @Override
    public String toString() {
        return "Safe[name=" + name + ", count=" + count + "]";
    }
}
