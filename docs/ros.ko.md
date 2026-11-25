# ROS·ROS 2 모델 사용

[한국어 README](../README.md) · [English](ros.en.md) · [파일 목록](parts.ko.md#ros-models) · [CAD 배치](full-model.ko.md)

`oh_my_mobilerobot_description`은 기본 베이스와 세 확장 예시의 URDF, 시각화 메시, 좌표계와 RViz 실행 설정을 제공하는 로봇 모델 패키지입니다. 같은 패키지를 ROS 1에서는 catkin으로, ROS 2에서는 ament_cmake로 빌드합니다. 어느 방식을 쓸지는 활성화된 환경의 `ROS_VERSION`에 따라 정해집니다.

<a id="models"></a>

## 모델 구성

| `variant` | 형상 | 링크 / 관절 |
| --- | --- | --- |
| `base` | 상판 위 모서리 기둥이 없는 기본 베이스 | 12 / 11 |
| `cargo` | 공통 3층 플랫폼과 적재함 | 13 / 12 |
| `arm` | 공통 3층 플랫폼과 산업용 6축암 형태 | 13 / 12 |
| `display` | 공통 3층 플랫폼과 안내 디스플레이 | 13 / 12 |

네 모델은 같은 베이스 링크와 메시를 공유합니다. 연속 회전 관절은 구동 바퀴 두 개, 캐스터 회전축 두 개, 캐스터 바퀴 축 두 개로 총 6개입니다. 확장부는 `module_link`에 고정되어 있고 로봇암도 CAD의 정적 자세를 그대로 유지합니다.

시각화 메시에는 외장, 프로파일, 모터, 바퀴, 캐스터, 센서의 외형이 들어 있습니다. 충돌 형상은 베이스와 센서, 캐스터 지지부가 박스이고 바퀴가 원통입니다. 확장 모듈에는 시각화 형상을 제공합니다. 동역학 시뮬레이션에 필요한 질량, 관성, 접촉 특성과 제어 설정은 사용하는 하드웨어 구성에 맞춰 추가합니다.

<a id="installation"></a>

## 준비

아래 명령은 ROS 환경을 활성화한 Linux Bash 셸을 기준으로 합니다. ROS 1은 Python 3 기반 catkin 환경, ROS 2는 ament_cmake·colcon 환경을 사용합니다. `rosdep`은 해당 ROS 배포판에 맞게 초기화되어 있어야 합니다.

```bash
git clone https://github.com/Leehyunbin0131/Oh-My-MobileRobot.git ~/Oh-My-MobileRobot
```

저장소를 이미 받아 두었다면 아래 복사 명령의 저장소 경로를 그 위치로 바꿉니다. `package://` 메시 경로를 해석할 수 있도록 **패키지 폴더 전체**를 워크스페이스에 넣습니다.

### ROS 2

```bash
mkdir -p ~/robot_ros2_ws/src
cp -R ~/Oh-My-MobileRobot/ros/oh_my_mobilerobot_description ~/robot_ros2_ws/src/
cd ~/robot_ros2_ws
rosdep install --from-paths src --ignore-src -r -y --rosdistro "$ROS_DISTRO"
colcon build --symlink-install --packages-select oh_my_mobilerobot_description
source install/setup.bash
ros2 launch oh_my_mobilerobot_description display.launch.py variant:=base
```

### ROS 1

```bash
mkdir -p ~/robot_ros1_ws/src
cp -R ~/Oh-My-MobileRobot/ros/oh_my_mobilerobot_description ~/robot_ros1_ws/src/
cd ~/robot_ros1_ws
rosdep install --from-paths src --ignore-src -r -y --rosdistro "$ROS_DISTRO"
catkin_make
source devel/setup.bash
roslaunch oh_my_mobilerobot_description display.launch variant:=base
```

<a id="display"></a>

## 표시와 연결

기본 실행은 `robot_description`을 불러온 뒤 `robot_state_publisher`와 관절 조정 GUI, RViz를 시작합니다. RViz의 고정 프레임은 `base_footprint`입니다. 다른 모델은 `variant:=cargo`, `variant:=arm`, `variant:=display`로 선택합니다.

| 인수 | 기본값 | 기능 |
| --- | --- | --- |
| `variant` | `base` | 네 모델 중 선택 |
| `model` | 선택한 모델의 URDF | 별도 URDF 파일 경로 지정 |
| `gui` | `true` | 관절 조정 GUI 사용. `false`면 GUI 없이 관절 상태 발행 |
| `publish_joint_states` | `true` | 표시용 `joint_state_publisher` 실행 |
| `rviz` | `true` | RViz 실행 |
| `use_sim_time` | `false` | `/clock` 기반 시간 사용 |

화면 없이 모델과 TF만 확인할 때는 다음 명령을 씁니다.

```bash
ros2 launch oh_my_mobilerobot_description display.launch.py variant:=base gui:=false rviz:=false
```

ROS 1에서는 같은 인수를 `display.launch`에 전달합니다. 실제 로봇의 관절 상태를 연결할 때는 `publish_joint_states:=false`로 표시용 발행을 끄고 주행 노드의 `/joint_states`를 사용합니다. 이때 주행 노드는 `odom`에서 `base_footprint`까지의 위치를, 센서 드라이버는 측정 데이터를 공급하도록 연결합니다.

<a id="frames"></a>

## 단위와 좌표계

URDF와 `meshes/visual/`은 **m·rad** 단위를 쓰고 메시 배율은 `1 1 1`입니다. ROS 축은 **X 전방, Y 좌측, Z 상방**이며 좌우는 로봇이 전방을 바라볼 때를 기준으로 합니다. CAD의 mm 좌표는 [전체 모델 배치](full-model.ko.md#base-platform)에 있습니다.

| 프레임 | 기준 |
| --- | --- |
| `base_footprint` | 구동축 중점의 지면 투영점, 모델 루트 |
| `base_link` | 구동축 중점 바로 위의 프레임 아랫면, 지면에서 0.101 m |
| `left_wheel_link`, `right_wheel_link` | 구동 바퀴 중심 |
| `left_caster_swivel_link`, `right_caster_swivel_link` | 캐스터 장착판의 회전 중심 |
| `left_caster_wheel_link`, `right_caster_wheel_link` | 캐스터 바퀴 중심 |
| `lidar_link` | A2M12 장착면 중심 |
| `laser_frame` | CAD 광학부 외형의 중심 높이 |
| `camera_link` | D435i 참고 외형의 전면 중심 |
| `camera_optical_frame` | 같은 위치, Z 전방·X 우측·Y 하방 |
| `module_link` | 확장부 기준점, 확장 모델에만 포함 |

CAD 좌표 `(X, Y, Z)`는 다음 식으로 `base_link` 기준 좌표로 바꿉니다.

```text
x = (60 - Y) / 1000
y = (X - 220) / 1000
z = Z / 1000
```

`base_footprint` 기준 높이는 위의 `z`에 0.101 m를 더합니다. 구동축 중심 간격은 0.480 m, 구동 바퀴 반경은 0.068 m입니다. 캐스터 바퀴는 회전축보다 뒤로 0.034 m 떨어져 있으며 반경은 0.038 m입니다. 바퀴 관절축은 +Y, 캐스터 회전축은 +Z입니다.

센서 프레임은 CAD상의 장착 위치와 방향을 나타내는 참조값입니다. 실제 센서를 연결할 때는 드라이버의 프레임 이름과 외부 보정값에 맞춰 조정합니다. 축과 단위는 [REP-103](references.md#ros-references)의 규칙을 따릅니다.

<a id="customization"></a>

## 수정과 재생성

모델 선택과 이름 접두사는 공통 Xacro의 `variant`, `prefix` 인수로 지정할 수 있습니다. 예를 들어 저장소 루트에서 다음 명령을 실행하면 접두사가 붙은 URDF가 생성됩니다.

```bash
xacro ros/oh_my_mobilerobot_description/urdf/oh_my_mobilerobot.urdf.xacro variant:=base prefix:=robot1_ > /tmp/robot1.urdf
```

이 파일을 `model:=/tmp/robot1.urdf`로 실행할 때는 RViz의 고정 프레임도 `robot1_base_footprint`로 바꿉니다.

CAD와의 연결 정보는 [`cad_mapping.json`](../ros/oh_my_mobilerobot_description/config/cad_mapping.json)에 있습니다. 이 파일은 원본 경로, 부품별 색상, 좌표 기준을 정의합니다. [`mesh_manifest.json`](../ros/oh_my_mobilerobot_description/config/mesh_manifest.json)에는 원본 SHA-256과 메시 경계, 단위 정보가 기록됩니다.

원본 CAD를 다시 변환하려면 SolidCraft CLI와 Python 3.9 이상 환경이 있는 저장소 루트에서 다음 명령을 실행합니다.

```bash
python -m pip install -r tools/requirements-ros.txt
python tools/generate_ros_description.py
python -m unittest discover -s tests -v
```

`solidcraft-cli`가 PATH에 없다면 생성 명령에 `--solidcraft "실행 파일 경로"`를 추가합니다. 변환기는 SolidCraft의 MCP 읽기·내보내기 세션에서 표시된 바디를 추출합니다. 이어서 원본 변경 여부와 경계 치수를 확인한 뒤 메시와 공통 Xacro, 네 URDF를 생성합니다. 검사 항목은 원본 일치, 메시 무결성, 링크 트리, 좌우·접지 높이, 센서 축, 캐스터 회전과 Xacro 변형입니다.

형상이나 관절을 수정했다면 워크스페이스의 패키지를 갱신하고 다시 빌드합니다. 3D 프린팅에는 [각 부품의 출력용 STL](parts.ko.md#printed-parts)을 사용합니다.
