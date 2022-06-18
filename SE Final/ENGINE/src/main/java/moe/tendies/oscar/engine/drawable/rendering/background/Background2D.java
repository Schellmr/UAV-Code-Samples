package moe.tendies.oscar.engine.drawable.rendering.background;

import lombok.Getter;
import moe.tendies.oscar.engine.camera.Camera;
import moe.tendies.oscar.engine.drawable.rendering.Shader;
import org.joml.Matrix4f;

public class Background2D {
    @Getter
    private final BackgroundRenderer backgroundRenderer;
    @Getter
    private final BackgroundTile[] tileRegister;
    @Getter
    private final int[][] map;
    private int numberOfBackgroundTiles;

    public final BackgroundTile WATER_TILE;
    public final BackgroundTile TOP_LAND_TILE;
    public final BackgroundTile BOTTOM_LAND_TILE;
    public final BackgroundTile LEFT_LAND_TILE;
    public final BackgroundTile RIGHT_LAND_TILE;
    public final BackgroundTile TL_CORNER_LAND_TILE;
    public final BackgroundTile BL_CORNER_LAND_TILE;
    public final BackgroundTile TR_CORNER_LAND_TILE;
    public final BackgroundTile BR_CORNER_LAND_TILE;

    public Background2D(int rows, int columns, int uniqueTiles) {
        System.out.println("background rows: " + rows + ", columns: " + columns);
        map = new int[rows][columns];

        tileRegister = new BackgroundTile[uniqueTiles];
        numberOfBackgroundTiles = 0;

        backgroundRenderer = new BackgroundRenderer();

        WATER_TILE = addBackgroundTile("water", false);
        TOP_LAND_TILE = addBackgroundTile("top_land_tile", true);
        BOTTOM_LAND_TILE = addBackgroundTile("bottom_land_tile", true);
        LEFT_LAND_TILE = addBackgroundTile("left_land_tile", true);
        RIGHT_LAND_TILE = addBackgroundTile("right_land_tile", true);
        TL_CORNER_LAND_TILE = addBackgroundTile("TLCorner_land_tile", true);
        BL_CORNER_LAND_TILE = addBackgroundTile("BLCorner_land_tile", true);
        TR_CORNER_LAND_TILE = addBackgroundTile("TRCorner_land_tile", true);
        BR_CORNER_LAND_TILE = addBackgroundTile("BRCorner_land_tile", true);
    }

    public BackgroundTile getTile(int r, int c) {
        try {
            return tileRegister[map[r][c]];
        } catch (ArrayIndexOutOfBoundsException e) {
            return null;
        }
    }

    public void setTile(int r, int c, int id) {
        map[r][c] = id;
        System.out.println("set " + r + ", " + c + " to " + id);
    }

    public void render(BackgroundTile tile, int x, int y, Shader shader, Matrix4f world, Camera cam) {
        backgroundRenderer.renderTile(tile, x, y, shader, world, cam);
    }

    private BackgroundTile addBackgroundTile(String texture, boolean isSolid) {
        BackgroundTile newTile = new BackgroundTile(texture, isSolid, numberOfBackgroundTiles);
        System.out.println("Created newTile, it is " + newTile);

        if (tileRegister[numberOfBackgroundTiles] != null) {
            throw new IllegalStateException("Tile at " + numberOfBackgroundTiles + " already used.");
        }
        tileRegister[numberOfBackgroundTiles] = newTile;

        backgroundRenderer.updateTiles(tileRegister);

        numberOfBackgroundTiles++;

        return newTile;
    }
}
