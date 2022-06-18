package moe.tendies.oscar.physics;

import org.joml.Vector2f;

public class Collision {
    public Vector2f distance;
    public boolean isIntersecting;
    public Collision(Vector2f distance, boolean intersects){
        this.distance = distance;
        this.isIntersecting = intersects;
    }
/*    moe.tendies.oscar.physics.AABB box1 = new moe.tendies.oscar.physics.AABB(new Vector2f(0,0),new Vector2f(1,1));
    moe.tendies.oscar.physics.AABB box2 = new moe.tendies.oscar.physics.AABB(new Vector2f(2,0),new Vector2f(1,1));

        if (box1.isIntersecting(box2))
            System.out.println("The boxes are intersecting");*/
}
