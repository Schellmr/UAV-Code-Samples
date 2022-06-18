
public class Tile {
    public static Tile tiles[] = new Tile[16];
    public static byte number_of_tiles = 0;

    public static final Tile water_tile = new Tile("water");
    public static final Tile top_land_tile = new Tile("top_land_tile").setSolid();
    public static final Tile bottom_land_tile = new Tile("bottom_land_tile").setSolid();
    public static final Tile left_land_tile = new Tile("left_land_tile").setSolid();
    public static final Tile right_land_tile = new Tile("right_land_tile").setSolid();
    public static final Tile TLCorner_land_tile = new Tile("TLCorner_land_tile").setSolid();
    public static final Tile BLCorner_land_tile = new Tile("BLCorner_land_tile").setSolid();
    public static final Tile TRCorner_land_tile = new Tile("TRCorner_land_tile").setSolid();
    public static final Tile BRCorner_land_tile = new Tile("BRCorner_land_tile").setSolid();


    private byte id;
    private boolean solid;
    private String texture;


    public Tile(String texture) {
        this.id = number_of_tiles;
        number_of_tiles++;
        this.texture = texture;
        this.solid = false;
        if(tiles[id] != null)
            throw new IllegalStateException("Tiles at ["+id+"] is already being used");
        tiles[id] = this;
    }

    public Tile setSolid(){this.solid = true; return this;}
    public boolean isSolid(){return solid;}

    public byte getId() {
        return id;
    }

    public String getTexture() {
        return texture;
    }
}
