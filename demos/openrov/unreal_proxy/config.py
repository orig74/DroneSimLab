# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

#pubsub
zmq_pub_drone_fdm=('172.17.0.2',5566)
#zmq_pub_drone_fdm=('127.0.0.1',12466)
topic_sitl_position_report=b'position_rep'

zmq_pub_unreal_proxy=('172.17.0.1',5577)
topic_unreal_state=b'unreal_state'
topic_unreal_drone_rgb_camera=b'rgb_camera_%d'

n_drones=1
