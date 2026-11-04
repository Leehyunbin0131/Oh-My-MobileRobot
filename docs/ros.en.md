# ROS and ROS 2 model usage

[English README](../README.en.md) · [한국어](ros.ko.md) · [File index](parts.en.md#ros-models) · [CAD layout](full-model.en.md)

`oh_my_mobilerobot_description` provides URDFs, visual meshes, coordinate frames, and RViz launch configurations for the base and three application concepts. The same package builds with ROS 1 catkin or ROS 2 ament_cmake, selected by `ROS_VERSION` in the active environment.

<a id="models"></a>

## Model contents

| `variant` | Geometry | Links / joints |
| --- | --- | --- |
| `base` | Base without raised deck-corner posts | 12 / 11 |
| `cargo` | Shared third-level platform and cargo carrier | 13 / 12 |
| `arm` | Shared third-level platform and industrial-style six-axis arm | 13 / 12 |
| `display` | Shared third-level platform and information display | 13 / 12 |

All four models share the base links and meshes. There are six continuous joints: two drive wheels, two caster swivels, and two caster wheels. Extensions attach to a fixed `module_link`; the arm retains its static CAD pose.

Visual meshes include the covers, extrusions, motors, wheels, casters, and sensor envelopes. Collision geometry uses boxes for the base, sensors, and caster supports, and cylinders for the wheels. Extension modules provide visual geometry. Mass, inertia, contact properties, and control settings for dynamics simulation belong to the chosen hardware configuration.

<a id="installation"></a>

## Prerequisites

The commands below use Linux Bash with the ROS environment already sourced. ROS 1 uses a Python 3 catkin environment; ROS 2 uses ament_cmake and colcon. Initialize `rosdep` for the installed ROS distribution before running these commands.

```bash
git clone https://github.com/Leehyunbin0131/Oh-My-MobileRobot.git ~/Oh-My-MobileRobot
```

For an existing checkout, substitute its path in the copy command below. Put the **complete package directory** in the workspace so that `package://` mesh references resolve.

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

## Display and integration

The default launch loads `robot_description` and starts `robot_state_publisher`, the joint adjustment GUI, and RViz. The RViz fixed frame is `base_footprint`. Select another model with `variant:=cargo`, `variant:=arm`, or `variant:=display`.

| Argument | Default | Function |
| --- | --- | --- |
| `variant` | `base` | Select one of the four models |
| `model` | URDF for the selected variant | Supply a separate URDF path |
| `gui` | `true` | Use the joint adjustment GUI; `false` publishes joint states without a GUI |
| `publish_joint_states` | `true` | Start the display joint-state publisher |
| `rviz` | `true` | Start RViz |
| `use_sim_time` | `false` | Use time from `/clock` |

Example displaying only the model data and TF without a window:

```bash
ros2 launch oh_my_mobilerobot_description display.launch.py variant:=base gui:=false rviz:=false
```

In ROS 1, pass the same arguments to `display.launch`. To connect real joint states, set `publish_joint_states:=false` and use `/joint_states` from the drive system. The drive node supplies the pose from `odom` to `base_footprint`, while sensor drivers supply measurement data.

<a id="frames"></a>

## Units and frames

URDFs and `meshes/visual/` use **metres and radians** with mesh scale `1 1 1`. ROS axes are **X forward, Y left, Z up**. Left and right are viewed from the robot facing forward. The CAD's millimetre coordinates are documented in the [complete model layout](full-model.en.md#base-platform).

| Frame | Reference |
| --- | --- |
| `base_footprint` | Ground projection of the drive-axle midpoint; model root |
| `base_link` | Frame underside directly above the drive-axle midpoint, 0.101 m above ground |
| `left_wheel_link`, `right_wheel_link` | Drive-wheel centers |
| `left_caster_swivel_link`, `right_caster_swivel_link` | Swivel centers at the caster mounting plates |
| `left_caster_wheel_link`, `right_caster_wheel_link` | Caster-wheel centers |
| `lidar_link` | Center of the A2M12 mounting plane |
| `laser_frame` | Center height of the CAD optical envelope |
| `camera_link` | Front center of the D435i reference envelope |
| `camera_optical_frame` | Same position, with Z forward, X right, Y down |
| `module_link` | Extension reference point, present only in extension models |

Convert CAD coordinates `(X, Y, Z)` to coordinates relative to `base_link` as follows:

```text
x = (60 - Y) / 1000
y = (X - 220) / 1000
z = Z / 1000
```

Add 0.101 m to `z` for coordinates relative to `base_footprint`. Drive-wheel center spacing is 0.480 m and radius is 0.068 m. Caster wheels trail the swivel axes by 0.034 m and have a radius of 0.038 m. Wheel joint axes are +Y; swivel axes are +Z.

Sensor frames describe CAD mounting positions and directions. Match their names and extrinsic transforms to the sensor drivers when connecting hardware. Axis and unit conventions follow [REP-103](references.md#ros-references).

<a id="customization"></a>

## Customization and regeneration

The common Xacro accepts `variant` and `prefix` arguments. For example, run this from the repository root to generate a prefixed URDF:

```bash
xacro ros/oh_my_mobilerobot_description/urdf/oh_my_mobilerobot.urdf.xacro variant:=base prefix:=robot1_ > /tmp/robot1.urdf
```

When launching this file with `model:=/tmp/robot1.urdf`, change the RViz fixed frame to `robot1_base_footprint` as well.

[`cad_mapping.json`](../ros/oh_my_mobilerobot_description/config/cad_mapping.json) defines source paths, body colors, and reference coordinates. [`mesh_manifest.json`](../ros/oh_my_mobilerobot_description/config/mesh_manifest.json) records source SHA-256 hashes, mesh bounds, and units.

With SolidCraft CLI and Python 3.9 or later available, regenerate from the source CAD at the repository root:

```bash
python -m pip install -r tools/requirements-ros.txt
python tools/generate_ros_description.py
python -m unittest discover -s tests -v
```

If `solidcraft-cli` is not on PATH, add `--solidcraft "path to executable"` to the generation command. The generator extracts visible bodies through a SolidCraft MCP read/export session, checks source integrity and bounds, and produces the meshes, common Xacro, and four URDFs. Checks cover source correspondence, mesh integrity, link trees, left/right placement, ground height, sensor axes, caster rotation, and Xacro variants.

After changing geometry or joints, update the workspace package and rebuild. Use the [individual printable STLs](parts.en.md#printed-parts) for 3D printing.
