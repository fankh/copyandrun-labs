package com.example;

import java.io.Serializable;

public class Node implements Serializable {
    private static final long serialVersionUID = 1L;

    public final String label;
    public final Node next;

    public Node(String label, Node next) {
        this.label = label;
        this.next = next;
    }

    public static Node chain(int length) {
        Node head = null;
        for (int i = length; i >= 1; i--) {
            head = new Node("n" + i, head);
        }
        return head;
    }
}
