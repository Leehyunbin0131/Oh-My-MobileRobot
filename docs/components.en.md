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
