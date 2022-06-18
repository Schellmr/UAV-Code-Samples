package moe.tendies.oscar.engine;

import lombok.Getter;
import lombok.Setter;
import moe.tendies.oscar.engine.camera.Camera;
import moe.tendies.oscar.engine.drawable.World2D;
import moe.tendies.oscar.engine.drawable.rendering.Shader;
import moe.tendies.oscar.engine.math.Timer;
import moe.tendies.oscar.game.world.OscarWorld;
import org.lwjgl.opengl.GL;

import static org.lwjgl.glfw.GLFW.*;
import static org.lwjgl.glfw.GLFW.glfwTerminate;
import static org.lwjgl.opengl.GL11.*;

public class OscarEngine extends Thread {
    private final double frameCap;
    private final int windowWidth, windowHeight;
    private final String windowName;
    private Shader shader;
    private Camera camera;

    @Getter
    @Setter
    private World2D world;

    public OscarEngine(int windowWidth, int windowHeight, String windowName) {
        Window.setCallbacks();

        if (!glfwInit()) {
            System.err.println("GLFW failed to initialize");
            System.exit(1);
        }

        this.frameCap = 1.0 / 144.0;
        this.windowWidth = windowWidth;
        this.windowHeight = windowHeight;
        this.windowName = windowName;

        this.world = null;
    }

    public void run() {
        Window win = new Window();
        win.setSize(windowWidth, windowHeight);
        win.setFullscreen(false);
        win.createWindow(windowName);
        GL.createCapabilities();

        glEnable(GL_BLEND);
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);

        glEnable(GL_TEXTURE_2D);

        this.shader = new Shader("shader");
        camera = new Camera(windowWidth, windowHeight);

        OscarWorld world = new OscarWorld(128, 128, 24);
        world.setTiles();
        setWorld(world);

        double frameTime = 0;
        int frames = 0;

        double time = Timer.getTime();
        double unprocessed = 0;

        while (!win.shouldClose()) {
            boolean canRender = false;
            double time2 = Timer.getTime();
            double passed = time2 - time;

            unprocessed += passed;
            frameTime += passed;
            time = time2;

            while (unprocessed >= frameCap) {
                unprocessed -= frameCap;
                canRender = true;

                if (win.getInput().isKeyPressed(GLFW_KEY_ESCAPE)) {
                    glfwSetWindowShouldClose(win.getWindow(), true);
                }

                world.updateEntities((float) frameCap, win, camera, world);
                world.correctCamera(camera,win);

                win.update();
                if (frameTime >= 1.0) {
                    frameTime = 0;

                    System.out.println("FPS: " + frames);
                    frames = 0;
                }
            }

            if (canRender) {
                glClear(GL_COLOR_BUFFER_BIT);

                world.render(shader, camera, win);

                win.swapBuffers();
                frames++;
            }
        }
        glfwTerminate();
    }
}
