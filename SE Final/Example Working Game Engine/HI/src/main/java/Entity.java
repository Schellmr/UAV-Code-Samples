import org.joml.Matrix4f;
import org.joml.Vector2f;
import org.joml.Vector3f;

import static org.lwjgl.glfw.GLFW.*;
import static org.lwjgl.glfw.GLFW.GLFW_KEY_DOWN;

public class Entity {

    private static Model model;
    //private Texture texture;
    protected Animation[] animations;
    private int use_animation;
    protected Transform transform;
    protected AABB bounding_box;
    private int field = 5;
    public boolean start = true;
    public boolean start_game;

    public Entity(int max_animations,Transform transform){
        this.animations = new Animation[max_animations];
        this.transform = transform;
        this.use_animation = 0;

        bounding_box = new AABB(new Vector2f(transform.pos.x,transform.pos.y),new Vector2f(transform.scale.x,transform.scale.y));
    }

    public void move(Vector2f direction){
        transform.pos.add(new Vector3f(direction,0));

        bounding_box.getCenter().set(transform.pos.x,transform.pos.y);
    }

    protected void setAnimation(int index,Animation animation){
        animations[index] = animation;
    }

    public void useAnimation(int index){
        this.use_animation = index;
    }

    public void collideWithTiles(World world){
        AABB[] boxes = new AABB[field*field];
        for(int i = 0;i<field;i++){
            for (int j = 0;j<field;j++){
                boxes[i+j*field] = world.getTileBoundingBox(
                        (int)(((transform.pos.x/2)+0.5f)-(field/2)) + i,
                        (int)(((-transform.pos.y/2)+0.5f)-(field/2)) + j
                );
            }
        }

        AABB box = null;
        for(int i = 0; i < boxes.length;i++){
            if (boxes[i] != null){
                if (box == null) box = boxes[i];
                Vector2f length1 = box.getCenter().sub(transform.pos.x,transform.pos.y,new Vector2f());
                Vector2f length2 = boxes[i].getCenter().sub(transform.pos.x,transform.pos.y,new Vector2f());
                if(length1.lengthSquared()>length2.lengthSquared()){
                    box = boxes[i];
                }
            }
        }
        if(box != null) {
            Collision data = bounding_box.getCollision(box);
            if (data.isIntersecting) {
                bounding_box.correctPosition(box, data);
                transform.pos.set(bounding_box.getCenter(),0);
            }
            for(int i = 0; i < boxes.length;i++){
                if (boxes[i] != null){
                    if (box == null) box = boxes[i];
                    Vector2f length1 = box.getCenter().sub(transform.pos.x,transform.pos.y,new Vector2f());
                    Vector2f length2 = boxes[i].getCenter().sub(transform.pos.x,transform.pos.y,new Vector2f());
                    if(length1.lengthSquared()>length2.lengthSquared()){
                        box = boxes[i];
                    }
                }
            }
            data = bounding_box.getCollision(box);
            if (data.isIntersecting) {
                bounding_box.correctPosition(box, data);
                transform.pos.set(bounding_box.getCenter(),0);
            }
        }
    }
    public void update(float delta, Window window, Camera camera,World world){
        collideWithTiles(world);
    }

    public void render(Shader shader,Camera camera,World world){
        Matrix4f target = camera.getProjection();
        target.mul(world.getWorldMatrix());
        shader.bind();
        shader.setUniform("sampler",0);
        shader.setUniform("projection", transform.getProjection(target));
        animations[use_animation].bind(0);
        model.render();
    }

public static void initAsset(){
    float[] vertices = new float[] {
            -1f,1f,0,
            1f,1f,0,
            1f,-1f,0,
            -1f,-1f,0,
    };
    float[] texture = new float[] {
            0,0,
            1,0,
            1,1,
            0,1,
    };
    int[] indices = new int[] {
            0,1,2,
            2,3,0
    };
    model = new Model(vertices, texture, indices);
}

public static void deleteAsset(){
        model = null;
    }
}