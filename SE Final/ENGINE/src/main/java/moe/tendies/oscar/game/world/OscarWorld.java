package moe.tendies.oscar.game.world;

import moe.tendies.oscar.engine.drawable.World2D;
import moe.tendies.oscar.engine.math.Transform;
import moe.tendies.oscar.game.playable.Player;

public class OscarWorld extends World2D {
    public OscarWorld(int tileRows, int tileColumns, int scale) {
        super(tileRows, tileColumns, scale);

        Transform t = new Transform();
        t.pos.x = 5;
        t.pos.y = -5;
        t.scale.set(2.2, 2.2,1);

        entityList.add(new Player(t, "USCGSmallboat"));
    }

    @Override
    public void setTiles() {
        for(int i = 0; i < 128; i++){
            getBackground().setTile(i, 0, background.BOTTOM_LAND_TILE.getId());
            getBackground().setTile(i, tileColumns - 1, background.TOP_LAND_TILE.getId());
            getBackground().setTile(0, i, background.LEFT_LAND_TILE.getId());
            getBackground().setTile(tileRows - 1, i, background.RIGHT_LAND_TILE.getId());
        }
        getBackground().setTile(0, 0, background.TL_CORNER_LAND_TILE.getId());
        getBackground().setTile(0, tileRows - 1, background.TR_CORNER_LAND_TILE.getId());
        getBackground().setTile(tileColumns - 1, tileRows - 1, background.BR_CORNER_LAND_TILE.getId());
        getBackground().setTile(0, 0, background.BL_CORNER_LAND_TILE.getId());
    }
}
