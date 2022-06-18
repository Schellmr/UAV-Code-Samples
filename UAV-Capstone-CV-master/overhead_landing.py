import collections

# assuming 10 Hz refresh rate, errors over the last 5 seconds.
errors_north = collections.deque(50*[0], 50)
errors_east = collections.deque(50*[0], 50)


def position_overhead(mag_north, mag_east, prev_north, prev_east, alt, prev_alt):
    """
    Defines the second stage controller for off-board computer vision enabled landing
    Negative magnitudes indicate South or West.
    Error is always equal to magnitude -> seeking to minimize error so minimize magnitude
    The integral components have 50 elements of maximum 3. With a gain of .05, we have a max integral
    velocity commanded of 7.5 m/s.

    :param mag_north: pixels in north-south axis
    :param mag_east: pixels in east-west axis
    :param prev_north: previous pixels in north-south axis (for derivative term)
    :param prev_east: previous pixels in east-west axis (for derivative term)
    :param alt: altitude from LIDAR or other sensor in some real measurement
    :param prev_alt: previous altitude (for derivative term)

    :return: velocities to be commanded
    """

    # update integral term list only if we are within 3 meters to begin with.
    if mag_north < 3:
        errors_north.appendleft(mag_north)
    else:
        errors_north.appendleft(0)

    if mag_east < 3:
        errors_east.appendleft(mag_east)
    else:
        errors_east.appendleft(0)

    # gain provides maximum velocity
    proportional_horizontal_gain = 0.5
    proportional_altitude_gain = 5.0
    derivative_horizontal_gain = 0.0
    derivative_altitude_gain = 1.0
    integral_horizontal_gain = 0.05

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

    # be very careful with integral term gains
    integral_north = set_velocity * integral_horizontal_gain * sum(errors_north) / len(errors_north)
    integral_east = set_velocity * integral_horizontal_gain * sum(errors_east) / len(errors_east)

    velocity_north = proportional_north + derivative_north + integral_north
    velocity_east = proportional_east + derivative_east + integral_east

    # if we are 3 meters or less off the ground, descend at the set velocity and no more
    proportional_altitude = set_velocity
    derivative_altitude = 0
    if alt > 5:
        proportional_altitude = set_velocity * proportional_altitude_gain * alt

        # don't allow the derivative term to grow too large
        if not abs(alt - prev_alt) > 1:
            derivative_altitude = set_velocity * derivative_altitude_gain * (alt - prev_alt)

    velocity_altitude = proportional_altitude + derivative_altitude

    if abs(velocity_north) > 2:
        velocity_north = velocity_north / abs(velocity_north) * 2
    if abs(velocity_east) > 2:
        velocity_north = velocity_east / abs(velocity_east) * 2

    return -velocity_north, -velocity_east, 0
