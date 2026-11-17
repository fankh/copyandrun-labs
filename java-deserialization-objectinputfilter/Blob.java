package com.example;

import java.io.Serializable;

public class Blob implements Serializable {
    private static final long serialVersionUID = 1L;

    public final byte[] data;
    public final Safe tail = new Safe("tail", 0);

    public Blob(int size) {
        this.data = new byte[size];
    }
}
