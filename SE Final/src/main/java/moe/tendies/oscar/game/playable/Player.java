package moe.tendies.oscar.game.playable;

import moe.tendies.oscar.game.world.World;
import moe.tendies.oscar.rendering.Window;
import moe.tendies.oscar.math.Transform;
import moe.tendies.oscar.rendering.Entity;
import moe.tendies.oscar.rendering.drawable.Animation;
import moe.tendies.oscar.rendering.camera.Camera;
import org.joml.Vector2f;
import org.joml.Vector3f;

import static org.lwjgl.glfw.GLFW.*;
import static org.lwjgl.glfw.GLFW.GLFW_KEY_DOWN;

public class Player extends Entity {
    public int choice = 0;
    public String charName;
    public static final int ANIM_UP = 0;
    public static final int ANIM_DOWN = 1;
    public static final int ANIM_LEFT = 2;
    public static final int ANIM_RIGHT = 3;
    public static final int ANIM_UPRIGHT = 4;
    public static final int ANIM_UPLEFT = 5;
    public static final int ANIM_DOWNRIGHT = 6;
    public static final int ANIM_DOWNLEFT = 7;
    public static final int ANIM_SIZE = 8;

    public Player(Transform transform, String characterName){
        super(ANIM_SIZE,transform);
        String prefix = characterName + "\\" + characterName;
        setAnimation(ANIM_UP,new Animation(1,1, prefix + "U"));
        setAnimation(ANIM_DOWN,new Animation(1,1,prefix + "D"));
        setAnimation(ANIM_LEFT,new Animation(1,1,prefix + "L"));
        setAnimation(ANIM_RIGHT,new Animation(1,1, prefix + "R"));
        setAnimation(ANIM_UPRIGHT,new Animation(1,1,prefix + "UR"));
        setAnimation(ANIM_UPLEFT,new Animation(1,1,prefix + "UL"));
        setAnimation(ANIM_DOWNRIGHT,new Animation(1,1,prefix + "DR"));
        setAnimation(ANIM_DOWNLEFT,new Animation(1,1,prefix + "DL"));
    }
    @Override
    public void update(float delta, Window window, Camera camera, World world){
        if(window.getInput().isKeyDown(GLFW_KEY_A)) {
            choice = choice + 1;
        }
        Vector2f movement = new Vector2f();

        if(window.getInput().isKeyDown(GLFW_KEY_LEFT)) {
            movement.add(-15*delta,0);
        }
        if(window.getInput().isKeyDown(GLFW_KEY_RIGHT)) {
            movement.add(15*delta,0);
        }
        if(window.getInput().isKeyDown(GLFW_KEY_UP)) {
            movement.add(0,15*delta);
        }
        if(window.getInput().isKeyDown(GLFW_KEY_DOWN)) {
            movement.add(0,-15*delta);
        }
        if(movement.x == 0 && movement.y < 0)
            useAnimation(ANIM_DOWN);
        else if(movement.x > 0 && movement.y < 0)
            useAnimation(ANIM_DOWNRIGHT);
        else if(movement.x < 0 && movement.y > 0)
            useAnimation(ANIM_UPLEFT);
        else if(movement.x < 0 && movement.y < 0)
            useAnimation(ANIM_DOWNLEFT);
        else if(movement.x > 0 && movement.y == 0)
            useAnimation(ANIM_RIGHT);
        else if(movement.x < 0 && movement.y == 0)
            useAnimation(ANIM_LEFT);
        else if(movement.x > 0 && movement.y > 0)
            useAnimation(ANIM_UPRIGHT);
        else if(movement.x == 0 && movement.y > 0)
            useAnimation(ANIM_UP);

        if(movement.x < 0 && movement.y > 0)
            transform.scale.set(2.5,2.5,1);
        else if(movement.x < 0 && movement.y < 0)
            transform.scale.set(2.5,2.5,1);
        else if(movement.x > 0 && movement.y < 0)
            transform.scale.set(2.5,2.5,1);
        else if(movement.x > 0 && movement.y > 0)
            transform.scale.set(2.5,2.5,1);
        else
            transform.scale.set(2.2,2.2,1);
        move(movement);
        super.update(delta, window, camera, world);
        camera.getPosition().lerp(transform.pos.mul(-world.getScale(), new Vector3f()),0.1f);
    }

}