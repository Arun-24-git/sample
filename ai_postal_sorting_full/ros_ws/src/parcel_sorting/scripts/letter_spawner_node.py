
#!/usr/bin/env python
import rospy, os, rospkg
from std_msgs.msg import String
from gazebo_msgs.srv import SpawnModel, DeleteModel
from geometry_msgs.msg import Pose

class LetterSpawner:
    def __init__(self):
        rospy.init_node('letter_spawner_node')
        self.model_xml = self.load_model()
        self.spawn_srv = rospy.ServiceProxy('/gazebo/spawn_sdf_model', SpawnModel)
        self.del_srv = rospy.ServiceProxy('/gazebo/delete_model', DeleteModel)
        rospy.wait_for_service('/gazebo/spawn_sdf_model')
        rospy.Subscriber('/web_sort_request', String, self.cb)
        rospy.loginfo('[LetterSpawner] Ready, waiting for bin requests')
        rospy.spin()

    def load_model(self):
        rospack = rospkg.RosPack()
        model_path = os.path.join(rospack.get_path('parcel_sorting'), 'models', 'letter_box', 'model.sdf')
        if not os.path.exists(model_path):
            rospy.logwarn('Letter model not found, using simple box')
            # fallback: simple box SDF
            return """<?xml version='1.0'?>
<sdf version='1.6'>
  <model name='letter_box'>
    <static>false</static>
    <link name='link'>
      <collision name='collision'>
        <geometry><box><size>0.1 0.05 0.005</size></box></geometry>
      </collision>
      <visual name='visual'>
        <geometry><box><size>0.1 0.05 0.005</size></box></geometry>
      </visual>
    </link>
  </model>
</sdf>"""
        with open(model_path) as f:
            return f.read()

    def cb(self, msg):
        bin_id = msg.data
        pose = Pose()
        pose.position.x = 0  # spawn above conveyor; modify as needed
        pose.position.y = 0
        pose.position.z = 0.3
        model_name = f'letter_{rospy.Time.now().to_nsec()}'
        try:
            self.spawn_srv(model_name, self.model_xml, '', pose, 'world')
            rospy.loginfo(f'[LetterSpawner] Spawned {model_name} for {bin_id}')
        except Exception as e:
            rospy.logerr(f'Spawn failed: {e}')

if __name__ == '__main__':
    LetterSpawner()
