package moe.tendies.oscar.engine.drawable.rendering.background;

import lombok.Getter;

public class BackgroundTile {
    @Getter
    private final String texture;
    @Getter
    private final boolean isSolid;
    @Getter
    private final int id;

    public BackgroundTile(String texture, boolean isSolid, int id) {
        this.texture = texture;
        this.isSolid = isSolid;
        this.id = id;
    }
}
