# WMX R2 Jupyter 가이드 — 전체 계획

## 노트북 구성 (Step 번호는 노트북 전체에 걸쳐 이어짐)

| # | 파일 | 범위 | Step |
|---|---|---|---|
| 01 | `01_wmx_system_startup.ipynb` | WMX 시스템 시작: 백엔드 노드 기동, 엔진 생성, EtherCAT 통신 개시, XML 파라미터 로드 | 1~4 |
| 02 | `02_Axis_Activation&Coordinate_Alignment.ipynb` | 축 설정 및 모터 준비: 알람 클리어, Servo On, Homing, 제어 모드 설정 | 5~8 |
| 03 | `03_Motion_for_py.ipynb` | 간단한 모터 제어: Velocity Mode 조깅(HMI/E-Stop) + Position Mode 이동 | 9~12 |
| 04 | `04_Manipulator.ipynb` | 매니퓰레이터 응용: Proprietary Trajectory Control vs 표준 ros2_control | 13~15 |
| 05 | `05_Visualization_and_Data_Logging.ipynb` | 시각화 및 데이터 로깅: 자동 궤적 구동, 실시간 차트, CSV 저장/불러오기 | 16~20 |
| 06+ | *(미착수)* | `wmx-intelligent` + AI API 연동: 자연어 명령 → 모션 실행 | TBD |

01, 02, 03은 **셀 바이 셀**로 "모터가 실제로 구동하기까지 필요한 사전 단계"를 하나씩 학습하는 것이 목적이라 Step 구조를 해치지 않는다. 04부터는 이미 익힌 Step들의 조합(예: Step 1~8을 담은 launch 파일 하나)을 가져와 응용 실습에 집중하고, 07 이후에는 사용자가 자신의 로봇/축 구성에 맞게 커스텀 코드를 짤 수 있도록 템플릿 형태의 셀을 남겨둘 예정이다.

---

## 확정된 배경 지식

### 1. `set_mode`의 3가지 모드 (`02` Step 8 / `03`에서 실습)

`SetAxis` 서비스의 `data` 필드는 축마다 아래 정수 코드를 받는다.

| 코드 | 모드 | 설명 | 지원 상태 |
|---|---|---|---|
| `0` | **Position Mode** | 목표 절대/상대 위치로 이동. 02의 기본값이며 04의 궤적 제어(MoveIt2 C-Spline)도 이 모드를 사용. | ✅ 지원 |
| `1` | **Velocity Mode** | 목표 속도로 연속 회전(조깅/속도 제어). 03의 위젯 대시보드가 이 모드로 전환한 뒤 동작. | ✅ 지원 |
| `2` | **Torque Mode** | 목표 토크(전류) 지령으로 구동. | 🚧 열거값만 존재, 현재 설치된 `wmx_r2_message` 패키지에는 이를 위한 커맨드 토픽/서비스가 아직 없음 — SDK가 인터페이스를 노출하면 03에 Part C로 추가 예정. |

> 02는 Step 8에서 기본적으로 `0`(Position)으로 설정한다. 03에서 속도 조깅을 하려면 그 전에 `1`로 재전환해야 하고, 이어서 위치 이동을 실습하려면 다시 `0`으로 되돌려야 한다 — 이 전환 자체를 03의 Step 9 / Step 11로 명시했다.

### 2. `c-spline`, `joint_state_broadcaster` 등 — 기존 설명 유지

- **C-Spline**: MoveIt2가 만든 이산 waypoint를 WMX3 엔진 내부에서 3차 곡선으로 보간. 상위 ROS 2 제어기의 CPU 부하 없이 마이크로초 단위 하드웨어 클럭으로 동기화된다.
- **joint_state_broadcaster**: EtherCAT로 읽은 실제 인코더 값(Position/Velocity/Effort)을 표준 `sensor_msgs/msg/JointState`로 `/joint_states`에 지속 publish하는 중계 노드.

### 3. 01/02 client 셀 마크다운

01, 02, 03, 05 각 노트북 앞부분에 있는 `WmxClient` 생성 코드 셀 위에, Step 번호를 새로 매기지 않는 짧은 비고(`####` 레벨) 마크다운을 추가해 그 셀이 무엇을 하는지 설명한다. 01에는 상세 설명을, 02/03/05에는 "01 참고"로 축약한 설명을 넣어 Step 1~20 흐름을 끊지 않는다.

### 4. 하드웨어 유무에 따른 순서 배치

**하드웨어 기본 + 시뮬레이션 콜아웃** 방식으로 확정.

- 01~04는 실제 EtherCAT 하드웨어 흐름을 기본 서술로 유지한다.
- 하드웨어가 없는 사용자를 위해 04/05에 "🖥️ 시뮬레이션 환경이라면?" 콜아웃 박스를 넣어 Gazebo 트랙(`gazebo_trajectory_simulation.launch.py`, `sim_bridge.launch.py`)으로 바로 넘어갈 수 있게 안내한다.
- 05는 원래 Gazebo 기반으로 만들어져 있으므로 그대로 시뮬레이션 노트북으로 유지하되, 실기 하드웨어 사용자를 위한 "실기로 바꾸려면" 콜아웃을 추가한다.
- 별도 파일로 트랙을 완전히 분리하지는 않는다 (노트북 개수 증가로 유지보수 부담이 커짐).

---

## 03 노트북 보완 내용

1. 인트로에 Part A(Velocity)/Part B(Position) 구성과 Torque 미지원 안내 추가.
2. **Step 9**: 축을 Velocity Mode(`1`)로 전환.
3. **Step 10**: 기존 HMI 조깅 대시보드 + **E-Stop 버튼** 신설 (`/wmx/axis/stop` 서비스 호출 — 기존 "STOP" 버튼은 속도 0 publish, "E-STOP"은 별도 서비스 콜로 구분).
4. **Step 11**: 축을 다시 Position Mode(`0`)로 전환.
5. **Step 12**: 목표 위치로 이동하는 서비스 호출 실습. ⚠️ 정확한 서비스 이름(`move`/`move_abs` 등)은 설치된 `wmx_r2_message` 패키지 버전에 따라 다를 수 있어 `ros2 service list | grep /wmx/axis`로 확인 후 코드의 서비스 이름을 맞추도록 TODO 콜아웃으로 표시.
6. Torque Mode는 "추후 SDK 업데이트 대기" 안내만 추가하고 실습 셀은 만들지 않음 (사용자 확인: 현재 인터페이스 없음).

## 04 노트북 보완 내용

1. 인트로 중간에 잘려 있던 "Zero-Gap Digital Twin" 설명 문장 완성, 남아있던 `[cite: ...]` 잔재 제거.
2. **Step 13**: `references/launch_dobot_cr3a_manipulator.md`의 터미널 명령을 그대로 가져와 드라이버/컨트롤러, MoveIt2 플래너, Trajectory API 브리지 3개 터미널 기동 절차를 명시.
3. **Step 14**: 기존 `MoveJoints` 서비스 호출(Proprietary Trajectory Control) 실습 유지.
4. **Step 15**: 표준 `ros2_control` 트랙 비교 실습 — `wmx_r2_control_cr3a_manipulator.launch.py`로 전환 후 표준 `control_msgs/action/FollowJointTrajectory` 액션으로 동일한 목표 자세를 실행. (표준 ROS 2 인터페이스라 이름이 안정적으로 확정되어 있음.)
5. 시뮬레이션 콜아웃 박스 추가.

## 05 노트북 보완 내용 (`05_.ipynb` → `05_Visualization_and_Data_Logging.ipynb`로 이름 변경)

1. **Step 16~17**: 기존 Half-Sine 자동 구동 + 트윈 축 차트 유지, 단 플로팅 셀 안에 있던 `wmx.destroy_node()` 중복 호출 버그 제거(같은 노드를 두 번 destroy하려던 부분을 마지막 정리 셀 하나로 통합).
2. **Step 18**: 캡처한 telemetry를 CSV로 저장 (`~/workspaces/movensys_ws/wmx_logs/telemetry_*.csv`).
3. **Step 19**: 저장된 CSV를 다시 불러와(=데이터 불러오기) ROS 2/로봇 연결 없이도 이어서 분석할 수 있음을 실습.
4. **Step 20**: ROS 2 노드 정리(기존 마지막 셀, 라벨만 추가).
5. 빈 코드 셀 제거.

## 다음 로드맵 (06+) — 아직 미착수

- **06 (가칭) `wmx-intelligent` AI API 연동**: 자연어 지시("팔을 안전 자세로 옮겨줘")를 Claude API 등으로 파싱해 04의 `MoveJoints`/`FollowJointTrajectory` 호출로 변환하는 노트북. 03~05가 정리된 뒤 별도 세션에서 착수.
- **07 사용자 커스텀 템플릿**: 지금까지의 Step들을 재사용 가능한 함수/셀 스니펫으로 정리해, 사용자가 자신의 축 구성으로 갈아끼울 수 있는 뼈대 노트북 제공.
