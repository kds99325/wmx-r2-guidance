"""Helper utilities for Notebook 3 (Position vs. Velocity motion tests).

Mirrors the WmxClient pattern in wmx_utils.py: a small class owns the
`/wmx/axis/state` subscription and exposes a blocking `get_current_position()`
call, so the notebook cells stay focused on the motion commands themselves
instead of subscription bookkeeping.
"""

import rclpy
from wmx_r2_message.msg import AxisState


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