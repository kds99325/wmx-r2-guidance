# [Blueprint] WMX R2 ROS2 EtherCAT & Motor Control Jupyter Notebook Guidance

본 가이드는 모벤시스(Movensys)의 WMX3 실시간 모션 제어 엔진을 ROS2 환경에서 제어하는 **WMX R2** 패키지를 기반으로, 사용자가 대화식(Interactive) 주피터 노트북 환경에서 하드웨어 모터를 시동하고 기본 제어를 수행할 수 있도록 구성한 통합 교안 아키텍처입니다.

노트북 셀 단위로 **Markdown(이론 및 절차 설명)**과 **Code(Python `rclpy` 및 Bash 셸 명령)**를 유기적으로 배치하여 실습 편의성을 극대화했습니다.

---

## 📌 노트북 설계 요약 및 핵심 목표
1. **점진적 제어 접근법:** 복잡한 로봇 제어(MoveIt2/Nav2) 이전에, 독자적인 WMX3 라이브러리 및 ROS2 기본 통신 아키텍처를 이해합니다.
2. **실시간 시동 흐름 마스터:** WMX 특유의 장치 초기화, 네트워크 상태 제어, 알람 관리 및 서보 제어 흐름(Typical Startup Sequence)을 직접 코드로 실행하며 검증합니다.
3. **대화식 제어 환경 활용:** Python 셸(`rclpy`)을 통해 주피터 환경 내에서 실시간 피드백을 수신하고 동적으로 축을 제어합니다.

---

# 📚 주피터 노트북 전체 목차 (TOC)

- **Chapter 1: 실시간 제어 환경 준비 및 패키지 빌드**
  - 1.1. WMX Linux 실시간 환경 및 의존성 개요 (Markdown)
  - 1.2. CycloneDDS 및 환경 변수 등록 (Bash)
  - 1.3. 작업 공간(Workspace) 빌드 및 검증 (Bash)
- **Chapter 2: WMX R2 일반 하드웨어 제어 노드 기동**
  - 2.1. 실시간 로우레벨 제어 런치(General Nodes Launch) 실행 (Bash)
  - 2.2. 제어 인터페이스 노드 상태 모니터링 (Bash/Python)
- **Chapter 3: 하드웨어 초기화 및 실시간 시동 시퀀스 실습 (핵심 실습)**
  - 3.1. [STEP 1] WMX3 가상/물리 디바이스 인터페이스 생성 (Python)
  - 3.2. [STEP 2] EtherCAT 실시간 네트워크 통신 개시 (Python)
  - 3.3. [STEP 3] 하드웨어 파라미터 XML 로딩 (Python)
  - 3.4. [STEP 4] 축별 오류 상황 초기화 및 알람 클리어 (Python)
  - 3.5. [STEP 5] 서보 활성화 (Servo On) 제어 (Python)
- **Chapter 4: 기본 모터 축 위치 및 속도 제어 실습**
  - 4.1. 동적 축 속도(AxisVelocity) 지령 전송 (Python/Bash)
  - 4.2. 키보드 및 타임 아웃 기반 조깅(Jogging) 운전 실습 (Python)
- **Chapter 5: EtherCAT 원격 디지털 I/O 상태 모니터링 및 제어**
  - 5.1. I/O 입력 비트 상태 조회 (Python)
  - 5.2. I/O 출력 제어 및 비트 조작 (Python)
- **Chapter 6: 네트워크 상태 진단 및 문제 해결 (Diagnostics)**
  - 6.1. EtherCAT 토폴로지 분석 및 네트워크 무결성 진단 (Python)

---

# ✏️ 각 단원별 상세 구성 및 수록 내용 (Cell-by-Cell Blueprint)

## Chapter 1: 실시간 제어 환경 준비 및 패키지 빌드

### Cell 1.1 (Markdown) : WMX Linux 실시간 환경 및 의존성 개요
*   **목적:** 사용자가 하드웨어 실습을 진행하기 전 필수적인 전제 조건을 확실하게 인지하도록 돕습니다.
*   **설명할 핵심 내용:**
    *   **실시간(Real-time) 제어의 필수성:** 모터 제어 주기(예: 1ms 또는 250us) 내에 패킷 송수신이 지연 없이 확정적(Deterministic)으로 이루어져야 함을 서술합니다. 이를 위해 **WMX Linux (RT-Preempt 패치 커널)** 및 WMX3 SDK 라이브러리(`libimdll.so` 등)가 설치되어 있는 경로(`/opt/wmx3/`)를 확인합니다.
    *   **RMW (ROS Middleware) CycloneDDS 권장 이유:** 기본 DDS들의 실시간성 한계를 극복하기 위해 타이밍 안정성이 검증된 `rmw_cyclonedds`를 필수 탑재하는 아키텍처적 배경을 설명합니다.

### Cell 1.2 (Bash Code) : CycloneDDS 및 환경 변수 등록
*   **목적:** 주피터 노트북 안에서 터미널 환경 설정을 일괄 업데이트하고 검증합니다.
*   **코드 예시:**
    ```bash
    # CycloneDDS 및 ROS2 개발 경로 변수 점검
    echo "=== Current ROS2 & DDS Settings ==="
    export RMW_IMPLEMENTATION=rmw_cyclonedds
    echo "RMW_IMPLEMENTATION: $RMW_IMPLEMENTATION"
    
    # WMX3 SDK 공유 라이브러리 탐색 경로 체크
    ls -l /opt/wmx3/lib/libimdll.so || echo "[Warning] WMX3 SDK is not detected in /opt/wmx3!"
    ```

### Cell 1.3 (Bash Code) : 작업 공간(Workspace) 빌드 및 검증
*   **목적:** WMX R2 인터페이스 빌드를 수행합니다.
*   **코드 예시:**
    ```bash
    # ROS2 패키지 빌드 명령어 실행 (사용자 ROS 2 작업 공간에서 실행 가정)
    cd ~/workspaces/movensys_ws
    source /opt/ros/$ROS_DISTRO/setup.bash
    colcon build --packages-up-to wmx_r2_package
    ```

---

## Chapter 2: WMX R2 일반 하드웨어 제어 노드 기동

### Cell 2.1 (Bash Code) : 실시간 로우레벨 제어 런치(General Nodes Launch) 실행
*   **목적:** 백그라운드에서 하드웨어와 연결을 대기하는 ROS2 드라이버 노드를 기동합니다.
*   **핵심 설명:**
    *   실시간 우선순위 스케줄링(FIFO, Priority 99 등)을 얻기 위해, ROS2 런치 구동 시 반드시 **root 권한(sudo)**이 필요합니다. 
    *   사용자의 주요 환경 변수들을 훼손하지 않는 `--preserve-env` 파라미터를 활용해 런치를 백그라운드로 실행합니다.
*   **코드 예시:**
    ```bash
    # 백그라운드로 로우 레벨 드라이버 4대 엔진 구동
    sudo --preserve-env=PATH \
         --preserve-env=LD_LIBRARY_PATH \
         --preserve-env=ROS_DISTRO \
         --preserve-env=RMW_IMPLEMENTATION \
         ros2 launch wmx_r2_package wmx_r2_general_nodes.launch.py &
    ```

### Cell 2.2 (Bash / Python Code) : 제어 인터페이스 노드 상태 모니터링
*   **목적:** 실행된 4대 핵심 노드(`wmx_engine_node`, `wmx_core_motion_node`, `wmx_io_node`, `wmx_ethercat_node`)와 토픽 리스트가 정상적으로 감지되는지 확인합니다.
*   **코드 예시:**
    ```python
    import subprocess
    # 활성화된 ROS2 노드 리스트 확인
    nodes = subprocess.check_output("ros2 node list", shell=True).decode('utf-8')
    print("--- Active ROS2 Nodes ---")
    print(nodes)
    
    # wmx_engine_node 등의 생존 여부 및 준비 시그널 확인
    # /wmx/engine/ready 토픽은 WMX 엔진 연결이 활성화될 때까지 False를 발행합니다.
    ```

---

## Chapter 3: 하드웨어 초기화 및 실시간 시동 시퀀스 실습 (핵심 실습)

### Cell 3.0 (Markdown) : 시동 시퀀스(Startup Sequence)의 중요성
*   **목적:** 하드웨어를 파손하지 않고 부드럽게 기동하는 고유의 순서를 가이드합니다.
*   **설명할 핵심 내용:**
    *   모터를 켜는 과정은 단순히 스위치를 올리는 것과 다릅니다. 통신망 상태가 정합성을 잃은 상황에서 구동 명령이 전송되는 것을 원천 차단하기 위해 WMX 엔진은 엄격한 단계별 시퀀스를 준수합니다.

### Cell 3.1 (Python Code) : [STEP 1] WMX3 가상/물리 디바이스 인터페이스 생성
*   **목적:** `SetEngine` 서비스를 호출하여 WMX3 디바이스를 생성합니다.
*   **코드 구성:** Python `rclpy` 모듈을 사용해 비동기적으로 서비스를 호출하는 주피터 특화 코드를 제시합니다.
*   **코드 예시:**
    ```python
    import rclpy
    from wmx_r2_message.srv import SetEngine

    if not rclpy.ok(): rclpy.init()
    node = rclpy.create_node('jupyter_wmx_startup_client')
    client = node.create_client(SetEngine, '/wmx/engine/set_device')

    while not client.wait_for_service(timeout_sec=2.0):
        print("Waiting for /wmx/engine/set_device service...")

    req = SetEngine.Request()
    req.data = True  # 디바이스 열기
    req.path = '/opt/wmx3/'
    req.name = 'my_device'

    future = client.call_async(req)
    rclpy.spin_until_future_complete(node, future)
    print(f"Device Init Response: {future.result()}")
    ```

### Cell 3.2 (Python Code) : [STEP 2] EtherCAT 실시간 네트워크 통신 개시
*   **목적:** EtherCAT 마스터 통신을 활성화합니다.
*   **설명:** 이 단계가 성공하면 물리적인 EtherCAT 버스 상의 모든 슬레이브 모터 드라이브와 I/O 카드가 마스터와 정밀 동기화(OP State 진입)됩니다.
*   **코드 예시:**
    ```python
    from std_srvs.srv import SetBool
    comm_client = node.create_client(SetBool, '/wmx/engine/set_comm')
    
    req_comm = SetBool.Request()
    req_comm.data = True # 통신 활성화
    
    future_comm = comm_client.call_async(req_comm)
    rclpy.spin_until_future_complete(node, future_comm)
    print(f"EtherCAT Communication Start Response: {future_comm.result()}")
    ```

### Cell 3.3 (Python Code) : [STEP 3] 하드웨어 파라미터 XML 로딩
*   **목적:** 각 제어할 로봇/하드웨어(예: Diffbot, Dobot 등)에 맞는 기어비, 엔코더 해상도 분해능 및 소프트웨어 안전 한계(Soft limits)를 칩셋에 업로드합니다.
*   **코드 예시:**
    ```python
    from wmx_r2_message.srv import LoadWmxParams
    param_client = node.create_client(LoadWmxParams, '/wmx/params/load')
    
    req_param = LoadWmxParams.Request()
    # 예시: Diffbot 파라미터 로드
    req_param.file_path = '/opt/ros/humble/share/wmx_r2_package/config/diffbot_wmx_parameters.xml'
    
    future_param = param_client.call_async(req_param)
    rclpy.spin_until_future_complete(node, future_param)
    print(f"Load Parameters Response: {future_param.result()}")
    ```

### Cell 3.4 (Python Code) : [STEP 4] 축별 오류 상황 초기화 및 알람 클리어
*   **목적:** 전원이 인가될 때 발생해 있는 구동 서보 드라이브의 알람(Alarm) 상태를 리셋하여 동작 가능 상태로 해제합니다.
*   **코드 예시:**
    ```python
    from wmx_r2_message.srv import SetAxis
    alarm_client = node.create_client(SetAxis, '/wmx/axis/clear_alarm')
    
    req_alarm = SetAxis.Request()
    # 0번 및 1번 모터 축 동시 알람 해제
    req_alarm.index = [0, 1]
    req_alarm.data = [0, 0] # 가드 데이터
    
    future_alarm = alarm_client.call_async(req_alarm)
    rclpy.spin_until_future_complete(node, future_alarm)
    print(f"Alarm Clear Response: {future_alarm.result()}")
    ```

### Cell 3.5 (Python Code) : [STEP 5] 서보 활성화 (Servo On) 제어
*   **목적:** 모터 드라이브에 실제 전력을 흘려(Servo On) 축이 사용자의 운전 명령을 따르도록 강력하게 고정시킵니다.
*   **주의:** 이 단계가 완료되면 모터 브레이크가 해제되고 기구부가 고정되므로 주위에 간섭 물체가 없는지 엄격히 점검해야 합니다.
*   **코드 예시:**
    ```python
    servo_client = node.create_client(SetAxis, '/wmx/axis/set_on')
    
    req_servo = SetAxis.Request()
    req_servo.index = [0, 1]
    req_servo.data = [1, 1]  # 1 = Servo On 활성화
    
    future_servo = servo_client.call_async(req_servo)
    rclpy.spin_until_future_complete(node, future_servo)
    print(f"Servo On Command Sent. Response: {future_servo.result()}")
    ```

---

## Chapter 4: 기본 모터 축 위치 및 속도 제어 실습

### Cell 4.1 (Python / Bash Code) : 동적 축 속도(AxisVelocity) 지령 전송
*   **목적:** 서보 온이 정상적으로 수립되었다면, 주피터 노트북에서 토픽을 한 번만 퍼블리시하여 모터를 실제 회전시켜 봅니다.
*   **코드 예시 (Python 퍼블리셔):**
    ```python
    from wmx_r2_message.msg import AxisVelocity
    import time
    
    # 토픽 퍼블리셔 노드 생성
    vel_pub = node.create_publisher(AxisVelocity, '/wmx/axis/velocity', 10)
    
    # 0번 축을 1000 user-unit/s 의 속도로 회전 명령 (가속 10000, 감속 10000)
    msg = AxisVelocity()
    msg.index = [0]
    msg.velocity = [1000.0]
    msg.acc = [10000.0]
    msg.dec = [10000.0]
    
    print("Sending velocity command for 2 seconds...")
    vel_pub.publish(msg)
    time.sleep(2.0)
    
    # 정지 명령 전송
    msg.velocity = [0.0]
    vel_pub.publish(msg)
    print("Stopped.")
    ```

### Cell 4.2 (Markdown & Code) : 안전 장치 - 타임아웃 조깅 (Jogging) 실습
*   **목적:** 실무 하드웨어 테스트 시 가장 안전한 제어 조작인 'Hold-to-move' Jogging에 대해 실습합니다.
*   **설명할 핵심 내용:**
    *   **안전 타임아웃의 원리:** 명령 주기 동안 토픽이 지속적으로 유입되지 않으면 드라이버 단에서 강제로 휠 속도를 `0`으로 감속시켜 폭주를 막는 `cmd_vel_timeout` 메커니즘을 배웁니다.
*   **코드 예시 (20Hz 주기적 발행):**
    ```python
    import threading
    
    jog_pub = node.create_publisher(AxisVelocity, '/wmx/axis/jog', 10)
    jog_msg = AxisVelocity()
    jog_msg.index = [0]
    jog_msg.velocity = [500.0] # 조그 운전 속도
    jog_msg.acc = [5000.0]
    jog_msg.dec = [5000.0]
    
    # 3초 동안만 주피터에서 주기적으로 조그 신호 모방 전송
    stop_event = threading.Event()
    def send_jog():
        while not stop_event.is_set():
            jog_pub.publish(jog_msg)
            time.sleep(0.05) # 20Hz 발행 (50ms 주기)
            
    thread = threading.Thread(target=send_jog)
    thread.start()
    time.sleep(3.0)
    stop_event.set()
    thread.join()
    print("Jog Test Ended. Motor automatically stops safely.")
    ```

---

## Chapter 5: EtherCAT 원격 디지털 I/O 상태 모니터링 및 제어

### Cell 5.1 (Python Code) : I/O 입력 비트 상태 조회
*   **목적:** 장치 센서나 안전 센서 등의 I/O 장비 입력 비트 상태를 불러옵니다.
*   **코드 예시:**
    ```python
    from wmx_r2_message.srv import GetIoBit
    io_client = node.create_client(GetIoBit, '/wmx/io/get_input_bit')
    
    req_io = GetIoBit.Request()
    req_io.byte = 0
    req_io.bit = 0 # 0번 바이트의 0번 비트 센서 상태 읽기
    
    future_io = io_client.call_async(req_io)
    rclpy.spin_until_future_complete(node, future_io)
    print(f"I/O State (Byte 0, Bit 0): {future_io.result().value}")
    ```

### Cell 5.2 (Python Code) : I/O 출력 제어 및 비트 조작
*   **목적:** 작업 끝단 지그 장치(Solenoid, Gripper 등)의 구동 명령을 위해 I/O 출력 포트에 쓰기 명령을 수행합니다.
*   **코드 예시:**
    ```python
    from wmx_r2_message.srv import SetIoBit
    set_io_client = node.create_client(SetIoBit, '/wmx/io/set_output_bit')
    
    req_set = SetIoBit.Request()
    req_set.byte = 0
    req_set.bit = 0
    req_set.value = 1 # 1로 켜기 (솔레노이드 등 활성화)
    
    future_set = set_io_client.call_async(req_set)
    rclpy.spin_until_future_complete(node, future_set)
    print(f"Set IO Output Response: {future_set.result()}")
    ```

---

## Chapter 6: 네트워크 상태 진단 및 문제 해결 (Diagnostics)

### Cell 6.1 (Python Code) : EtherCAT 토폴로지 분석 및 네트워크 무결성 진단
*   **목적:** 동작 도중 EtherCAT 디바이스 케이블 손상, 슬레이브 유실 상태 및 노이즈 등의 이유로 통신 품질이 떨어지는 경우 이를 실시간 진단합니다.
*   **코드 예시:**
    ```python
    from wmx_r2_message.srv import EcatGetNetworkState
    diag_client = node.create_client(EcatGetNetworkState, '/wmx/ecat/get_network_state')
    
    req_diag = EcatGetNetworkState.Request()
    req_diag.master_id = 0 # 0번 마스터 통신망 진단
    
    future_diag = diag_client.call_async(req_diag)
    rclpy.spin_until_future_complete(node, future_diag)
    print(f"EtherCAT Network State: {future_diag.result()}")
    ```

---

## 🚀 다음 단계로의 확장 방향 (Next Roadmap inside the Jupyter Notebook)
이번 '기본 뼈대 가이드'를 사용자가 성공적으로 이해하고 나면, 다음 주피터 세션에서 바로 연동할 수 있는 상위 응용 파트들은 다음과 같습니다.

1.  **Chapter 7: `differential_drive_controller` 통합 주행 실습**
    *   2륜 바퀴 역기하학(IK) 계수 검증 및 `/cmd_vel` 조종 인터페이스 연동.
2.  **Chapter 8: Joint Trajectory Controller 제어 및 매니퓰레이터 6축 동기화**
    *   Dobot CR3A / CR5A의 각 축 각도 데이터를 활용한 궤적 스플라인 플래닝 연계 실습.
