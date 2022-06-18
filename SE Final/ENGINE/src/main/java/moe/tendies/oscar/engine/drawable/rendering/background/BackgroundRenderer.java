package moe.tendies.oscar.engine.drawable.rendering.background;

import moe.tendies.oscar.engine.camera.Camera;
import moe.tendies.oscar.engine.drawable.rendering.Model;
import moe.tendies.oscar.engine.drawable.rendering.Shader;
import moe.tendies.oscar.engine.drawable.rendering.Texture;
import org.joml.Matrix4f;
import org.joml.Vector3f;

import java.util.HashMap;

public class BackgroundRenderer {
    private final HashMap<String, Texture> tileTextures;
    private final Model genericTileModel;

    public BackgroundRenderer() {
        tileTextures = new HashMap<>();

        float[] vertices = new float[]{
                -1f, 1f, 0,
                1f, 1f, 0,
                1f, -1f, 0,
                -1f, -1f, 0,
        };
        float[] texture = new float[]{
                0, 0,
                1, 0,
                1, 1,
                0, 1,
        };
        int[] indices = new int[]{
                0, 1, 2,
                2, 3, 0
        };

        genericTileModel = new Model(vertices, texture, indices);
    }

    public void updateTiles(BackgroundTile[] tiles) {
        for (BackgroundTile tile : tiles) {
            if (tile != null) {
                if (!tileTextures.containsKey(tile.getTexture())) {
                    String tex = tile.getTexture();
                    tileTextures.put(tex, new Texture(tex + ".png"));
                }
            }
        }
    }

    public void renderTile(BackgroundTile tile, int x, int y, Shader shader, Matrix4f world, Camera cam) {
        shader.bind();
        if (tileTextures.containsKey(tile.getTexture())) {
            tileTextures.get(tile.getTexture()).bind(0);
        }

        Matrix4f tile_pos = new Matrix4f().translate(new Vector3f(x * 2, y * 2, 0));
        Matrix4f target = new Matrix4f();

        cam.getProjection().mul(world, target);
        target.mul(tile_pos);

        shader.setUniform("sampler", 0);
        shader.setUniform("projection", target);

        genericTileModel.render();
    }
}
