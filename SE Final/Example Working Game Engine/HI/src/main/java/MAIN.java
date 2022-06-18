import org.joml.Matrix4f;
import org.joml.Vector2f;
import org.joml.Vector3f;
import org.lwjgl.glfw.GLFW;
import org.lwjgl.opengl.GL;
import org.lwjgl.system.CallbackI;

import java.nio.ByteBuffer;

import static org.lwjgl.glfw.GLFW.*;
import static org.lwjgl.opengl.GL11.*;

public class MAIN {
    public String characterName = "USCGSmallboat";
    public int choice;
    public void Main() {
        Window.setCallbacks();

        if(!glfwInit()) {
            System.err.println("GLFW failed to initialize");
            System.exit(1);
        }

        Window win = new Window();
        win.setSize(1400,900);
        win.setFullscreen(false);
        win.createWindow("OSCAR");
        GL.createCapabilities();

        glEnable(GL_BLEND);
        glBlendFunc(GL_SRC_ALPHA,GL_ONE_MINUS_SRC_ALPHA);

        Camera camera = new Camera(win.getWidth(),win.getHeight());
        glEnable(GL_TEXTURE_2D);
        TileRenderer tiles = new TileRenderer();
        Entity.initAsset();
        Shader shader = new Shader("shader");

        World world = new World();

        Transform t = new Transform();
        t.scale.set(2.2, 2.2,1);
        Player player = new Player(t, characterName);


        for(int j = 0; j < 128;j++){
            world.setTile(Tile.left_land_tile,0,j);
            world.setTile(Tile.top_land_tile,j,0);
            world.setTile(Tile.right_land_tile,127,j);
            world.setTile(Tile.bottom_land_tile,j,127);
        }
        world.setTile(Tile.TLCorner_land_tile,0,0);
        world.setTile(Tile.BLCorner_land_tile,0,127);
        world.setTile(Tile.TRCorner_land_tile,127,0);
        world.setTile(Tile.BRCorner_land_tile,127,127);

        double frame_cap = 1.0/60.0;

        double frame_time = 0;
        int frames = 0;

        double time = Timer.getTime();
        double unprocessed = 0;

        while(!win.shouldClose()) {
            boolean can_render = false;
            double time_2 = Timer.getTime();
            double passed = time_2 - time;
            unprocessed += passed;
            frame_time += passed;

            time = time_2;

            while(unprocessed>=frame_cap){
                unprocessed -= frame_cap;
                can_render = true;

                if(win.getInput().isKeyPressed(GLFW_KEY_ESCAPE)) {
                    glfwSetWindowShouldClose(win.getWindow(),true);
                }

                player.update((float)frame_cap,win,camera,world);

                world.correctCamera(camera,win);

                win.update();
                if(frame_time >= 1.0){
                    frame_time = 0;
                    System.out.println("FPS: " + frames);
                    frames = 0;
                }
            }
            if(can_render) {
                glClear(GL_COLOR_BUFFER_BIT);

                world.render(tiles,shader,camera,win);

                player.render(shader,camera,world);
                win.swapBuffers();
                frames++;
            }
        }
        Entity.deleteAsset();
        glfwTerminate();
    }

    public static void main(String[] args) {
        MAIN main = new MAIN();
        main.Main();

    }
}
