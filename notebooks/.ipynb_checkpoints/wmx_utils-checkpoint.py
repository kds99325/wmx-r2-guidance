import time

import rclpy
from rclpy.node import Node

from std_srvs.srv import SetBool
from wmx_r2_message.srv import SetEngine, LoadWmxParams, SetAxis
from wmx_r2_message.msg import AxisVelocity


class WmxClient(Node):
    def __init__(self, node_name='wmx_jupyter_client'):
        super().__init__(node_name)
        self.axis_list = [0, 1]
        self._wmx_clients = {}

    def call(self, srv_type, srv_name, request, timeout_sec=5.0):
        client = self._wmx_clients.get(srv_name)
        if client is None:
            client = self.create_client(srv_type, srv_name)
            if not client.wait_for_service(timeout_sec=timeout_sec):
                raise RuntimeError(f"Service '{srv_name}' not available after {timeout_sec}s")
            self._wmx_clients[srv_name] = client

        future = client.call_async(request)
        start = time.time()
        while not future.done():
            rclpy.spin_once(self, timeout_sec=0.1)
            if time.time() - start > timeout_sec:
                raise TimeoutError(f"No response from '{srv_name}' within {timeout_sec}s")

        return future.result()

class PositionReader:
    """Reads actual_pos from /wmx/axis/state on demand.

    Usage:
        pos_reader = PositionReader(wmx)
        before = pos_reader.get_current_position()
    """

    def __init__(self, wmx_client, topic='/wmx/axis/state',
                 timeout_tries=20, timeout_sec=0.1):
        self._wmx = wmx_client
        self._latest_msg = None
        self._timeout_tries = timeout_tries
        self._timeout_sec = timeout_sec
        self._sub = wmx_client.create_subscription(
            AxisState, topic, self._callback, 10)

    def _callback(self, msg):
        self._latest_msg = msg

    def get_current_position(self):
        """Return the current actual_pos as a list (one value per axis)."""
        self._latest_msg = None
        for _ in range(self._timeout_tries):
            rclpy.spin_once(self._wmx, timeout_sec=self._timeout_sec)
            if self._latest_msg is not None:
                return list(self._latest_msg.actual_pos)
        raise RuntimeError("No state received. Is /wmx/axis/state publishing?")