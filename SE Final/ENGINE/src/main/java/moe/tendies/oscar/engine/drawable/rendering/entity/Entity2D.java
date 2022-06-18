package moe.tendies.oscar.engine.drawable.rendering.entity;

import lombok.Getter;
import lombok.Setter;
import moe.tendies.oscar.engine.Window;
import moe.tendies.oscar.engine.camera.Camera;
import moe.tendies.oscar.engine.drawable.World2D;
import moe.tendies.oscar.engine.drawable.rendering.Animation;
import moe.tendies.oscar.engine.drawable.rendering.Model;
import moe.tendies.oscar.engine.drawable.rendering.Shader;
import moe.tendies.oscar.engine.math.Transform;
import moe.tendies.oscar.engine.physics.AABB;
import moe.tendies.oscar.engine.physics.Collision;
import org.joml.Matrix4f;
import org.joml.Vector2f;
import org.joml.Vector3f;

public class Entity2D {
    private final Model model;
    protected Animation[] animations;
    @Setter
    @Getter
    protected int animationIndex;
    protected Transform transform;
    protected AABB boundingBox;

    public Entity2D(Transform transform, int numAnimations) {
        this.animations = new Animation[numAnimations];
        animationIndex = 0;
        this.transform = transform;

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
        model = new Model(vertices, texture, indices);

        boundingBox = new AABB(new Vector2f(transform.pos.x, transform.pos.y),
                new Vector2f(transform.scale.x, transform.scale.y));
    }

    public void move(Vector2f direction) {
        transform.pos.add(new Vector3f(direction, 0));
        boundingBox.getCenter().set(transform.pos.x, transform.pos.y);
    }
    public void collide(World2D world) {
        AABB[] collisionBoxes = new AABB[4];
        for (int r = 0; r < 2; r++) {
            for (int c = 0; c < 2; c++) {
                collisionBoxes[r + c * 2] = world.getBoundingBoxes()
                        [(int) (((transform.pos.x / 2) + 0.5f) - 1) + r]
                        [(int) (((-transform.pos.y / 2) + 0.5f) - 1) + c];
            }
        }

        AABB collisionBox = null;
        for (AABB box : collisionBoxes) {
            if (collisionBox == null) {
                collisionBox = box;
            }
            Vector2f length1 = collisionBox.getCenter().sub(transform.pos.x, transform.pos.y, new Vector2f());
            Vector2f length2 = box.getCenter().sub(transform.pos.x, transform.pos.y, new Vector2f());
            if (length1.lengthSquared() > length2.lengthSquared()) {
                collisionBox = box;
            }
        }

        Collision data = boundingBox.getCollision(collisionBox);
        if (data.isIntersecting) {
            boundingBox.correctPosition(collisionBox, data);
            transform.pos.set(boundingBox.getCenter(), 0);
        }
        for (AABB box : collisionBoxes) {
            if (box != null) {
                Vector2f length1 = collisionBox.getCenter().sub(transform.pos.x, transform.pos.y, new Vector2f());
                Vector2f length2 = box.getCenter().sub(transform.pos.x, transform.pos.y, new Vector2f());
                if (length1.lengthSquared() > length2.lengthSquared()) {
                    collisionBox = box;
                }
            }
        }
        data = boundingBox.getCollision(collisionBox);
        if (data.isIntersecting) {
            boundingBox.correctPosition(collisionBox, data);
            transform.pos.set(boundingBox.getCenter(), 0);
        }
    }
    public void update(float positionDelta, Window window, Camera camera, World2D world) {
        //collide(world);
    }
    public void render(Shader shader, Camera camera, World2D world) {
        Matrix4f target = camera.getProjection();
        target.mul(world.getWorld());
        shader.bind();
        shader.setUniform("sampler", 0);
        shader.setUniform("projection", transform.getProjection(target));
        animations[animationIndex].bind(0);
        model.render();
    }

    protected void setAnimation(int index, Animation animation){
        animations[index] = animation;
    }
}
