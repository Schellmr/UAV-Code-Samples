package moe.tendies.oscar;

import moe.tendies.oscar.engine.OscarEngine;

public class Main {
    public static void main(String[] args) {
        OscarEngine gameEngine = new OscarEngine(1280, 720, "Hello World!");
        gameEngine.start();
    }
}
