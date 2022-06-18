def expanding_square(increment_meters, max_distance):
    """
    Expanding square returns a list of deviations for a given increment in meters.
    Meant to be interrupted upon detection of some target.

    :param increment_meters: Meters to expand the square by
    :param max_distance: Max distance to travel from the origin
    :return: a list of waypoints detailing the expanding square pattern.
    """

    deviation_north = 0
    deviation_east = 0
    distance_from_origin = 0
    waypoints = []
    counter = 0

    while distance_from_origin <= max_distance:  # generate waypoints until we reach max distance.
        waypoints.append((deviation_north, deviation_east))
        counter += 1

        if counter % 2 != 0:  # deal with either moving north south or east west first
            if counter % 4 == 1:  # if the count is 1, 5, 9, etc, increment by +increment
                deviation_north = abs(deviation_north) + increment_meters
            else:  # else increment by - increment.
                deviation_north = -1 * abs(deviation_north) - increment_meters
        else:
            if counter % 4 == 2:  # if count is 2, 6, 10, etc, increment by + increment.
                deviation_east = abs(deviation_east) + increment_meters
            else:  # increment by - increment
                deviation_east = -1 * abs(deviation_east) - increment_meters

        distance_from_origin = max(abs(deviation_north), abs(deviation_east))

    return waypoints
