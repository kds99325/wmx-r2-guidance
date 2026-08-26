# wmx-r2-guidance

An interactive guide using Jupyter Notebook and Python to easily set up and test the **Movensys WMX R2** ROS 2 EtherCAT motion control environment.

## 📓 Notebooks

Step numbers carry across the whole guide (01-05 = Steps 1-20), so once an axis is Servo-On you never re-learn the same call twice — later notebooks reuse it.

1. **[01 — System Bring-up](notebooks/01_wmx_system_startup.ipynb)** (Steps 1-4): Launch ROS 2 nodes, allocate the WMX3 engine, start EtherCAT communication, and load the XML parameter file.
2. **[02 — Axis Activation & Coordinate Alignment](<notebooks/02_Axis_Activation&Coordinate_Alignment.ipynb>)** (Steps 5-8): Clear alarms, execute Servo On, perform Homing, and set the control mode.
3. **[03 — Motor Control](notebooks/03_Motion_for_py.ipynb)** (Steps 9-12): Velocity Mode jogging with a threaded HMI dashboard + hardware E-Stop, then Position Mode absolute moves.
4. **[04 — Manipulator Control](notebooks/04_Manipulator.ipynb)** (Steps 13-15): Drive a 6-DOF Dobot CR3A through both WMX R2 architectures — Proprietary Trajectory Control and standard `ros2_control`.
5. **[05 — Visualization & Data Logging](notebooks/05_Visualization_and_Data_Logging.ipynb)** (Steps 16-20): Auto-drive a smooth trajectory, plot live velocity/torque telemetry, then export/reload it as CSV.

🚧 **Roadmap:** a future notebook (06+) will connect this guide to `wmx-intelligent`, driving motion through natural-language commands via an AI API. See `notebooks/00_Plan.md` for the full design notes and open questions.

## 🛠️ Quick Start

**Prerequisites:** Ubuntu 22.04/24.04, ROS 2 (Humble/Jazzy), WMX3 Engine, JupyterLab

```bash
mkdir -p ~/workspaces/movensys_ws/src
git clone [https://github.com/kds99325/wmx-r2-guidance.git](https://github.com/kds99325/wmx-r2-guidance.git)
cd wmx-r2-guidance
jupyter lab
```
