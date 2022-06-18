package moe.tendies.oscar.engine;

import lombok.Getter;
import moe.tendies.oscar.engine.io.Input;
import org.lwjgl.glfw.GLFWErrorCallback;
import org.lwjgl.glfw.GLFWVidMode;

import java.util.Objects;

import static org.lwjgl.glfw.GLFW.*;

public class Window {
    @Getter
    private long window;
    @Getter
    private int width, height;
    @Getter
    private boolean fullscreen;
    @Getter
    private Input input;

    public static void setCallbacks() {
        glfwSetErrorCallback(new GLFWErrorCallback() {
            @Override
            public void invoke(int error, long description) {
                throw new IllegalStateException(GLFWErrorCallback.getDescription(description));
            }
        });
    }

    public Window() {
        setSize(1280, 720);
        setFullscreen(false);
    }

    public void createWindow(String title) {

        window = glfwCreateWindow(width, height, title, fullscreen ? glfwGetPrimaryMonitor() : 0, 0);

        if (window == 0)
            throw new IllegalStateException("Failed to create window");

        if (!fullscreen) {
            GLFWVidMode vid = glfwGetVideoMode(glfwGetPrimaryMonitor());
            glfwSetWindowPos(window, (Objects.requireNonNull(vid).width() - width) / 2,
                    (vid.height() - height) / 2);
            glfwShowWindow(window);
        }
        glfwMakeContextCurrent(window);

        input = new Input(window);
    }

    public boolean shouldClose() {
        return glfwWindowShouldClose(window);
    }
    public void swapBuffers() {
        glfwSwapBuffers(window);
    }

    public void setSize(int width, int height) {
        this.width = width;
        this.height = height;
    }
    public void setFullscreen(boolean fullscreen) {
        this.fullscreen = fullscreen;
    }

    public void update() {
        input.update();
        glfwPollEvents();
    }
}
