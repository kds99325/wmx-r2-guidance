# wmx-r2-guidance

**wmx-r2-guidance** is an interactive, Jupyter Notebook-based guide designed for setting up, debugging, and controlling the **Movensys WMX R2** ROS 2 EtherCAT motion control interface. 

By leveraging Python and Jupyter's cell-by-cell execution model, this repository simplifies complex industrial hardware bringing-up sequences and makes real-time debugging incredibly intuitive.

---

## 🚀 Key Advantages of WMX R2 on Jupyter

1. **Python-Based Interactive Prototyping**
   - Eliminates the need to build and compile heavy C++ ROS 2 nodes for initial tests.
   - Developers and students can interactively call services, publish topics, and manipulate WMX parameters using python-based rapid prototyping.

2. **Step-by-Step Granular Debugging**
   - Traditional automation scripts run all-at-once, making it difficult to pinpoint whether an error stems from ROS 2 communication, WMX3 engine memory, EtherCAT master-slave states, or the physical motors themselves.
   - Dividing the bringing-up sequence into separate, execution-focused Jupyter cells allows developers to test, verify, and isolate hardware issues instantly before moving to the next phase.

---

## 📂 Completed Notebook Overview

This repository currently features the finalized **Notebook 1, 2, and 3**, covering the complete low-level hardware bringing-up and basic safety verification pipeline.

### 📓 Notebook 1: WMX3 System Bring-up
*Focuses on setting up the control infrastructure and launching the underlying software engine.*
- **ROS 2 Backend Activation:** Spawns communication nodes to manage high-level/low-level data exchange.
- **WMX3 Memory & EtherCAT Initialization:** Allocates motion controller memory and activates the EtherCAT network to establish physical master-slave connectivity.
- **Parameter Loading:** Dynamically imports hardware-specific properties (e.g., electronic gear ratios, software safety limits) from an XML configuration file.

### 📓 Notebook 2: Axis Activation & Coordinate Alignment
*Transitions passive robotic axes into an active, controlled, and synchronized operational state.*
- **Alarm Clearance:** Automatically detects and clears any lingering physical or safety-induced driver alarms.
- **Servo On & Joint Locking:** Applies motor current to lock the joint actuators physically into place.
- **Axis Homing (Digital Zero Alignment):** Performs origin search routines to align the physical motor position with the digital absolute "zero" coordinate.
- **Position Mode Configuration:** Sets the axis control modes to Position Control, establishing the foundation for smooth, repeatable multi-axis motion.

### 📓 Notebook 3: Simple Motor Control & Keyboard Jogging
*Implements initial motor handling, terminal-driven controls, and safety loop verifications.*
- **Interactive Keyboard Jogging:** Spawns a keyboard-driven jogging console to safely control motor rotation forward/backward in real time.
- **Safety Watchdog Testing:** Demonstrates the core "Deadman's Switch" mechanism—ensuring the motors automatically and safely decelerate to a complete stop if communication packets lag or the focus is lost.
- **Multi-Axis CLI Control:** Explains how to bypass single-axis jogging limitations and command multiple motors simultaneously using ROS 2 CLI topic broadcasting.

---

## 🛠️ Quick Start

### Prerequisites
- Ubuntu 22.04 LTS / 24.04 LTS with ROS 2 (Humble/Jazzy) installed.
- Movensys WMX3 Core Engine & WMX R2 packages configured.
- Jupyter Notebook / JupyterLab environment.

### Getting Started
1. Clone this repository into your workspace:
   ```bash
   git clone https://github.com/your-username/wmx-r2-guidance.git
   cd wmx-r2-guidance
   ```
2. Start JupyterLab:
   ```bash
   jupyter lab
   ```
3. Open `01_wmx_system_startup.ipynb` and begin running cells sequentially!

---

## ⚠️ Safe Shutdown & Resource Management
Because Jupyter Notebook holds the Python kernel memory continuously, a **Safe Shutdown** section is included at the end of the initialization flow. 

To prevent **Process Lock Errors (`StartProcessLockError`)** when restarting your notebooks, always run the final cleanup cell to release the WMX3 core lock:
```python
# Un-comment and run at the end of your session
req.data = False  # Reuses existing request instance to trigger close
res = wmx.call(SetEngine, '/wmx/engine/set_device', req)
```

---

## 🛡️ License
The ROS 2 interface components of this guidance are licensed under the **MIT License**. The underlying WMX3 Motion Engine remains the proprietary intellectual property of **Movensys**.
