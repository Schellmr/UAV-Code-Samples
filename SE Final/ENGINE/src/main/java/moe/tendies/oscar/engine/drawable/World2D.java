package moe.tendies.oscar.engine.drawable;

import lombok.Getter;
import lombok.Setter;
import moe.tendies.oscar.engine.Window;
import moe.tendies.oscar.engine.camera.Camera;
import moe.tendies.oscar.engine.drawable.rendering.Shader;
import moe.tendies.oscar.engine.drawable.rendering.background.Background2D;
import moe.tendies.oscar.engine.drawable.rendering.background.BackgroundRenderer;
import moe.tendies.oscar.engine.drawable.rendering.background.BackgroundTile;
import moe.tendies.oscar.engine.drawable.rendering.entity.Entity2D;
import moe.tendies.oscar.engine.physics.AABB;
import org.joml.Matrix4f;
import org.joml.Vector3f;

import java.util.ArrayList;
import java.util.List;

public abstract class World2D {
    protected int tileRenderDistance;
    @Getter
    protected List<Entity2D> entityList;
    @Getter
    protected Background2D background;
    @Getter
    protected AABB[][] boundingBoxes;
    @Getter
    protected final int tileRows, tileColumns;
    @Getter
    @Setter
    protected int scale;
    @Getter
    protected Matrix4f world;

    public World2D(int tileRows, int tileColumns, int scale) {
        this.tileRows = tileRows;
        this.tileColumns = tileColumns;
        this.scale = scale;
        this.tileRenderDistance = 64;

        this.entityList = new ArrayList<>();
        this.background = new Background2D(tileRows, tileColumns, 10);

        world = new Matrix4f().setTranslation(new Vector3f(0));
        world.scale(scale);
    }

    public void render(Shader shader, Camera cam, Window window) {
        int posX = ((int) cam.getPosition().x + (window.getWidth() / 2)) / (scale * 2);
        int posY = ((int) cam.getPosition().y - (window.getHeight() / 2)) / (scale * 2);
        for (int i = 0; i < tileRenderDistance; i++) {
            for (int j = 0; j < tileRenderDistance; j++) {
                BackgroundTile tile = background.getTile(i - posX, j + posY);
                if (tile != null) {
                    background.render(tile, i - posX, j + posY, shader, world, cam);
                }
            }
        }
        for (Entity2D entity : entityList) {
            entity.render(shader, cam, this);
        }
    }
    public void correctCamera(Camera camera, Window window) {
        Vector3f pos = camera.getPosition();

        int w = -tileRows * scale * 2;
        int h = tileColumns * scale * 2;

        if (pos.x > -(window.getWidth() / 2) + scale) {
            pos.x = -(window.getWidth() / 2) + scale;
        }
        if (pos.x < w + (window.getWidth() / 2) + scale) {
            pos.x = w + (window.getWidth() / 2) + scale;
        }

        if (pos.y < (window.getHeight() / 2) - scale) {
            pos.y = (window.getHeight() / 2) - scale;
        }
        if (pos.y > h - (window.getHeight() / 2) - scale) {
            pos.y = h - (window.getHeight() / 2) - scale;
        }
    }
    public void updateEntities(float delta, Window window, Camera camera, World2D world) {
        for (Entity2D entity : entityList) {
            entity.update(delta, window, camera, world);
        }
    }

    protected abstract void setTiles();
}
