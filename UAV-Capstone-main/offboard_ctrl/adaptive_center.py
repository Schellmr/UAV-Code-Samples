def find_center(roll, pitch):
    # this can be taken out for final
    width = 320  # frame width
    height = 240  # frame height
    h_fov = 62.2  # horizontal deg fov
    v_fov = h_fov * height / width  # find vertical
    cX = int(width / 2 * (1 + roll * 2 / h_fov))
    cY = int(height / 2 * (1 + pitch * 2 / v_fov))

    if cX > 319:
        cX = 319

    if cX < 0:
        cX = 0

    if cY > 239:
        cY = 239

    if cY < 0:
        cY = 0

    return cX, cY
