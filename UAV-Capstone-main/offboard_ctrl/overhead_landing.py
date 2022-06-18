def position_overhead(mag_north, mag_east, prev_north, prev_east, alt, prev_alt):
    """
    Defines the second stage controller for off-board computer vision enabled landing
    Negative magnitudes indicate South or West.
    Error is always equal to magnitude -> seeking to minimize error so minimize magnitude

    :param mag_north: pixels in north-south axis
    :param mag_east: pixels in east-west axis
    :param prev_north: previous pixels in north-south axis (for derivative term)
    :param prev_east: previous pixels in east-west axis (for derivative term)
    :param alt: altitude from LIDAR or other sensor in some real measurement
    :param prev_alt: previous altitude (for derivative term)
    :return:
    """
    # gain provides maximum velocity
    proportional_horizontal_gain = 2.0
    proportional_altitude_gain = 2.0
    derivative_horizontal_gain = 0.1
    derivative_altitude_gain = 0.1

    # set velocity
    set_velocity = 0.5

    # sanity check - we have lost sight of the landing point or have an invalid response
    # if mag_north > MAX_MAG_NORTH or mag_east > MAX_MAG_EAST:
    #     return 0, 0, 0

    # we normalize to camera FOV by dividing by the max magnitude of the error
    # this will cause issues when we get closer and closer to ground
    proportional_north = set_velocity * proportional_horizontal_gain * mag_north
    proportional_east = set_velocity * proportional_horizontal_gain * mag_east

    # don't allow the derivative term to grow too large
    # derivative_north = 0
    # derivative_east = 0

    # if not abs(mag_north - prev_north) > .1 * MAX_MAG_NORTH:
    derivative_north = set_velocity * derivative_horizontal_gain * (mag_north - prev_north)
    # if not abs(mag_east - prev_east) > .1 * MAX_MAG_EAST:
    derivative_east = set_velocity * derivative_horizontal_gain * (mag_east - prev_east)

    velocity_north = proportional_north + derivative_north
    velocity_east = proportional_east + derivative_east

    # if we are 3 meters or less off the ground, descend at the set velocity and no more
    proportional_altitude = set_velocity
    derivative_altitude = 0
    if alt > 5:
        proportional_altitude = set_velocity * proportional_altitude_gain * alt

        # don't allow the derivative term to grow too large
        if not abs(alt - prev_alt) > 1:
            derivative_altitude = set_velocity * derivative_altitude_gain * (alt - prev_alt)

    velocity_altitude = proportional_altitude + derivative_altitude

    return velocity_north, velocity_east, 0
