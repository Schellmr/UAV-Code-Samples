package moe.tendies.oscar.engine.camera;

import lombok.Getter;
import lombok.Setter;
import org.joml.Matrix4f;
import org.joml.Vector3f;

public class Camera {
    @Getter
    @Setter
    private Vector3f position;
    private final Matrix4f projection;

    public Camera(float width, float height) {
        position = new Vector3f(0, 0, 0);
        projection = new Matrix4f().setOrtho2D(-width / 2, width / 2, -height / 2, height / 2);
    }

    public Matrix4f getProjection() {
        return projection.translate(position, new Matrix4f());
    }
}
