# Purchased component specifications

[English README](../README.en.md) · [한국어](components.ko.md) · [Design references](references.md) · [ROS models](ros.en.md)

This document covers purchased component models, quantities, and product specifications. Dimensions are in mm. Frame mounting positions are in the [complete model layout](full-model.en.md#layout); board mounting holes and tray placement are in [printed part design specifications](design.en.md#electronics-trays).

<a id="drivetrain"></a>

## Drivetrain — DFRobot KIT0085

The drivetrain uses two motors and two wheels from the DFRobot Rubber Wheel & Motor Kit.

| Item | Product specification |
| --- | --- |
| Motor | 28PA51G, 12 V |
| Motor envelope | 123 × 36 × 36 |
| Wheel | Ø136 × 24 wide |

<a id="motor-brackets"></a>

## Motor mounts — two universal metal brackets

The brackets are marketed for 750/755/775/795/895 DC motors and 28/35/42 stepper motors.

| Item | Supplied product drawing value |
| --- | --- |
| Width | 50 ±0.1 |
| Formed vertical leg | 51–51.5 |
| Formed base leg | 53–53.5 |
| Flat-pattern length | 100 ±0.1 |
| Motor center opening | Ø22.1 |
| Motor-side adjustment holes | Drawing labels 4×Ø3.5, adjustment range 20–31 |
| Base slots | Width 4.2, end radius R2.1, drawing length dimension 30 |
| Base slot row spacing | 30 ±0.1 |

<a id="rear-casters"></a>

## Casters — two 3-inch units

| Item | Supplied product drawing value |
| --- | --- |
| Wheel diameter | Ø76 |
| Overall installation height | 101 |
| Labeled width | 33 |
| Mounting plate envelope | 95 × 64 |
| Vertical slot-row pitch | 44.5 |
| Labeled horizontal pitch | Reference 72.3; adjustment range 68.3–76.3 |
| Slot width | 8.5, with R4.3 ends labeled |
| Additional round holes | Labeled Ø9 |
| Swivel-center to wheel-axle offset | Labeled 34 |
| Mounting plate top to wheel axle | Labeled 63 |

<a id="controls-sensors"></a>

## Computing, control, and sensors

| Component | Quantity | Role and product information |
| --- | --- | --- |
| NVIDIA Jetson Orin Nano Super | 1 | Main computer |
| Arduino Mega 2560 | 1 | Microcontroller |
| NT-S-DCDM1210 | 1 | Motor driver |
| RPLIDAR A2M12 | 1 | LiDAR; Ø76 × 41 high envelope |
| RealSense D435i | 1 | Depth camera |
| HFI-A9 | 1 | IMU |

<a id="power-conversion"></a>

## DC-DC converters

| Component | Quantity | Product information |
| --- | --- | --- |
| SZH-EKBD-058 | 2 | Buck module; 60 × 51 × 22 body |
| LTC3780 SZH-EK334 | 1 | Buck-boost module |

<a id="frame-extrusions"></a>

## Frame members — 2020 aluminum extrusions

CAD reference member counts for the base platform (`440 × 400 × 140`) and shared third-level extension platform. Placement coordinates are in [complete model structure and layout](full-model.en.md).

| Group | Specification | Quantity | Placement and role |
| --- | --- | --- | --- |
| Base transverse rails | 2020 extrusion, 400 long | 6 | Four upper/lower front and rear rails, one upper center LiDAR rail, one lower rear caster rail |
| Base longitudinal rails | 2020 extrusion, 360 long | 4 | Four upper/lower left and right side rails |
| Base vertical posts | 2020 extrusion, 140 long | 4 | Four outer corner vertical members |
| Third-level extension posts | 2020 extrusion, 200 long | 4 | Shared corner posts for extension concepts (with four lower angle brackets and four upper triangular gussets) |
| Third-level upper frame and sheet | 2020 × 400 (3), 2020 × 360 (2), 440 × 400 × 3 aluminum sheet (1) | 1 set | Upper module support platform (the robot arm variant adds two extra cross rails) |

<a id="fasteners-standoffs"></a>

## Fasteners and standoffs

Fastener and standoff quantities for the printed covers, sensor bracket, and electronics trays. Interface dimensions are in [printed part design specifications](design.en.md).

| Component | Specification | Quantity | Application |
| --- | --- | --- | --- |
| Extrusion bolts and T-nuts | M4 × 8 bolt + M4 hammer T-nut (10 × 6 × 3.5) | 50 sets | Top deck (16 sets), eight front/side/rear split covers (32 sets, 4 per panel), D435i bracket (2 sets) |
| Sensor mounting screws | M3 × 6 screw | 6 | RPLIDAR A2M12 mount (4, flat underhead), RealSense D435i mount (2) |
| Board standoffs | M3 metal PCB standoff, 10 body (5 male thread) | 26 | Lower tray (14 pilot bosses) and upper tray (12 pilot bosses) |
| Inter-deck standoffs | M3 metal PCB standoff, 40 body | 4 | Two-level electronics tray corner columns (150 × 150 pitch) |
