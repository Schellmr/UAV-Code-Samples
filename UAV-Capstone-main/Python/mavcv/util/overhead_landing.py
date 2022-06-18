import math

# assume constant max magnitude as max pixels
MAX_MAG_NORTH = 240
MAX_MAG_EAST = 320

ASPECT_RATIO = 320 / 240

HORIZONTAL_ANGLE = 30
# VERTICAL_ANGLE = 2 * math.atan(math.tan(math.radians(HORIZONTAL_ANGLE)) * MAX_MAG_NORTH / MAX_MAG_EAST)
VERTICAL_ANGLE = 47


def position_overhead(mag_north, mag_east, prev_north, prev_east, alt, prev_alt):
    """
    Defines the second stage controller for off-board computer vision enabled landing
    Negative magnitudes indicate South or West.
    Error is always equal to magnitude -> seeking to minimize error so minimize magnitude

    :param mag_north: pixels in north-south axis
    :param mag_east: pixels in east-west axis
    :param prev_north: previous pixels in north-south axis (for derivative term)
    :param prev_east: previous pixels in east-west axis (for derivative term)
    :param alt: altitude from LIDAR or other sensor in some real measurement (meters)
    :param prev_alt: previous altitude (for derivative term)
    :return: velocities tuple for next state
    """
    # gain provides maximum velocity
    proportional_horizontal_gain = 5
    proportional_altitude_gain = .5
    derivative_horizontal_gain = .1
    derivative_altitude_gain = .1

    # set velocity
    set_velocity = .5

    # convert all magnitudes to distances based off of altitude
    max_distance_north, max_distance_east = pixels_to_distance(MAX_MAG_NORTH, MAX_MAG_EAST, alt)
    distance_north, distance_east = pixels_to_distance(mag_north, mag_east, alt)
    prev_distance_north, prev_distance_east = pixels_to_distance(prev_north, prev_east, prev_alt)

    # we normalize to camera FOV by dividing by the max magnitude of the error
    # this will cause issues when we get closer and closer to ground
    proportional_north = set_velocity * proportional_horizontal_gain * (distance_north / max_distance_north)
    proportional_east = set_velocity * proportional_horizontal_gain * (distance_east / max_distance_east)

    # don't allow the derivative term to grow too large
    derivative_north = 0
    derivative_east = 0
    if not abs(distance_north - prev_distance_north) > .1 * max_distance_north:
        derivative_north = set_velocity * derivative_horizontal_gain * (distance_north - prev_distance_north)
    if not abs(distance_east - prev_distance_east) > .1 * max_distance_east:
        derivative_east = set_velocity * derivative_horizontal_gain * (distance_east - prev_distance_east)

    velocity_north = proportional_north + derivative_north
    velocity_east = proportional_east + derivative_east

    velocity_altitude = 0
    if abs(mag_north) < .33 * MAX_MAG_NORTH and abs(mag_east) < .33 * MAX_MAG_EAST:
        # if we are 3 meters or less off the ground, descend at the set velocity and no more
        proportional_altitude = set_velocity
        derivative_altitude = 0
        if alt > .5:
            proportional_altitude = set_velocity * proportional_altitude_gain * alt
            # don't allow the derivative term to grow too large
            if not abs(alt - prev_alt) > 1:
                derivative_altitude = set_velocity * derivative_altitude_gain * (alt - prev_alt)

        velocity_altitude = proportional_altitude + derivative_altitude

    print("Velocities: " + str(velocity_north) + "n, " + str(velocity_east) + "e, " + str(velocity_altitude) + "z")
    return velocity_north, velocity_east, velocity_altitude


def pixels_to_distance(pixels_north, pixels_east, altitude):
    distance_north = pixels_north / MAX_MAG_NORTH * math.sin(math.radians(HORIZONTAL_ANGLE)) * altitude \
        / math.sin(math.radians(90 - VERTICAL_ANGLE))
    distance_east = pixels_east / MAX_MAG_EAST * math.sin(math.radians(VERTICAL_ANGLE)) * altitude \
        / math.sin(math.radians(90 - HORIZONTAL_ANGLE))

    return distance_north, distance_east
