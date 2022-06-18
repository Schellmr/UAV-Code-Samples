package moe.tendies.oscar.math;

public class Timer {
    public static double getTime() {
        return (double)System.nanoTime() / (double)1000000000L;
    }
}
