
#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from flask import Flask, request
from threading import Thread

app = Flask(__name__)
publisher = None

@app.route('/sort', methods=['POST'])
def sort():
    data = request.get_json(force=True)
    pin = data.get('pin', '')
    bin_id = data.get('bin', 'bin_default')
    rospy.loginfo(f'[WebBridge] Received sort request PIN={pin} BIN={bin_id}')
    publisher.publish(bin_id)
    return {'status': 'ok'}, 200

def run_flask():
    app.run(host='0.0.0.0', port=5005)

def main():
    global publisher
    rospy.init_node('web_bridge_node')
    publisher = rospy.Publisher('/web_sort_request', String, queue_size=10)
    t = Thread(target=run_flask)
    t.daemon = True
    t.start()
    rospy.loginfo('[WebBridge] Flask server started on port 5005')
    rospy.spin()

if __name__ == '__main__':
    main()
