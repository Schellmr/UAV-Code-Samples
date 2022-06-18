# Setting up Gazebo
* Copy `cga.world`, `cga_target.world`, and `cga_aruco_combined` into `PX4-Autopilot/Tools/sitl_gazebo/worlds/`.
* Copy the `quad` and `aruco_4x4_10` folders into `PX4-Autopilot/Tools/sitl/models/`.
* Edit `PX4-Autopilot/platforms/posix/cmake/sitl_target.cmake` to include `quad`, `cga`, `cga_target`, and `cga_aruco_combined` respectively.
* Copy `1234_quad` into `PX4-Autopilot/build/px4_sitl_default/etc/init.d-posix/airframes/`.
* Edit `PX4-Autopilot/build/px4_sitl_default/etc/init.d-posix/airframes/CMakeLists.txt` to include `1234_quad`.
* Copy `map_satellite...` into `.gazebo/models/`.

# Sample Commands
* These should be run from the root of `/PX4-Autopilot/`

* `make px4_sitl gazebo___cga`

* `make px4_sitl gazebo_quad__cga`

* `make px4_sitl gazebo_quad__cga_target`

* `make list_config_targets`

* ***be mindful of the number of underscores***

  
