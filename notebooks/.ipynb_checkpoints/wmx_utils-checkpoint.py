import rclpy
from rclpy.node import Node
from std_srvs.srv import SetBool
from wmx_r2_message.srv import SetEngine, LoadWmxParams, SetAxis
from wmx_r2_message.msg import AxisVelocity

class WmxClient(Node):
    """
    A shared ROS 2 client utility for Jupyter Notebooks to interact with the WMX3 motion engine.
    """
    def __init__(self, node_name='wmx_jupyter_client'):
        # Allow dynamic node names to avoid conflicts between different notebook kernels
        super().__init__(node_name)
        
        # Define target axes globally so they can be referenced across all steps
        self.axis_list = [0, 1] 

    def call(self, srv_type, srv_name, request):

        client = self.create_client(srv_type, srv_name)
        while not client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info(f"Waiting for '{srv_name}' service server...")
        
        future = client.call_async(request)
        rclpy.spin_until_future_complete(self, future)
        return future.result()