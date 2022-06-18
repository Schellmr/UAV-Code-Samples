from mavlink.mavlink_class import MavRcvr

Drone = MavRcvr()

Drone.set_offboard_mode()

while True:
    Drone.set_velocity(-1.0, 0.0, 0.0, 0.0)

# from pymavlink import mavutil, mavwp
# import pymavlink
# import time
# from threading import Thread
#
# mav = mavutil.mavlink_connection('udpin:localhost:14540')
# mav.wait_heartbeat()
# print("Mavlink connected.")
#
# msg = mav.recv_match(type=['LOCAL_POSITION_NED'],blocking=True)
# print('LOCAL_POSITION_NED: ', msg.time_boot_ms)
# px4_time_boot_ms = msg.time_boot_ms
#
#
# def set_velocity(vx, vy, vz, yaw):
#     # global initial_msec, time_boot_ms, px4_time_boot_ms
#     initial_msec = 0
#     now_msec = int(round(time.time()*1000))
#     if initial_msec == 0:
#         time_boot_ms = 0
#         initial_msec = now_msec
#     else:
#         time_boot_ms = now_msec - initial_msec + px4_time_boot_ms
#
#         # type_mask = ~(1 << 3 | 1 << 4 | 1 << 5  | 1<< 10)
#     type_mask = 0b0000101111000111
#     # mav.mav.set_position_target_local_ned_send(time_boot_ms, 1, 1, mavutil.mavlink.MAV_FRAME_BODY_FRD,
#     #                                            type_mask, 0, 0, 0, vx, vy, vz, 0, 0, 0, yaw, 0)
#     mav.mav.set_position_target_local_ned_send(time_boot_ms, 1, 1, mavutil.mavlink.MAV_FRAME_LOCAL_NED,
#                                                type_mask, 0, 0, 0, vx, vy, vz, 0, 0, 0, yaw*3.14159265358979323846/180, 0)
# # ARM
# # print ("ARM")
# # mav.mav.command_long_send(1, 1, mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM, 0,
# #                           1,
# #                           0, 0, 0, 0, 0, 0)
# #
# # msg = mav.recv_match(type=['COMMAND_ACK'],blocking=True)
# # print(msg)
#
#
# PX4_MAV_MODE = 1
# PX4_CUSTOM_SUB_MODE_OFFBOARD = 6
#
# mav.mav.command_long_send(1, 1, mavutil.mavlink.MAV_CMD_DO_SET_MODE, 0,
#                           PX4_MAV_MODE,
#                           PX4_CUSTOM_SUB_MODE_OFFBOARD, 0, 0, 0, 0, 0)
#
# # mav.mav.command_long_send(1, 1, mavutil.mavlink.MAV_CMD_DO_SET_MODE, 216,
# #                           0,
# #                           0, 0, 0, 0, 0, 0)
#
# while True:
#     set_velocity(1.0, 0, 0, 0)