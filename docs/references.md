# 자료 출처 / Design references

[한국어](../README.md) · [English](../README.en.md)

제조사 자료·제품 도면·프로젝트 실측과 설계 기준의 출처입니다. 실제 규격은 [구매 부품 사양](components.ko.md), 체결부 치수는 [출력 부품 설계 규격](design.ko.md), 조립 모델 좌표는 [전체 모델](full-model.ko.md)에 있습니다.

This page identifies manufacturer data, product drawings, project measurements, and design references. Values are documented in [purchased component specifications](components.en.md), [printed part design specifications](design.en.md), and the [complete model layout](full-model.en.md).

| 대상 / Item | 출처 / Source | 적용 항목 / Scope |
| --- | --- | --- |
| 프레임 / Frame | 프로젝트 실측·요구사항 / Project measurements and requirements | 프레임 외곽·프로파일 구성 / Frame envelope and extrusion layout |
| RPLIDAR A2M12 | [SLAMTEC A2M12 datasheet v1.0](https://wiki.slamtec.com/download/attachments/83066883/LD310_SLAMTEC_rplidar_datasheet_A2M12_v1.0_en.pdf?api=v2&modificationDate=1677815058000&version=1) | 센서 외형·장착 패턴·나사 삽입 한도 / Sensor envelope, mounting pattern, screw insertion limit |
| RealSense D435i | [D400 datasheet, August 2025](https://www.realsenseai.com/wp-content/uploads/2025/08/Intel-RealSense-D400-Series-Datasheet-August-2025.pdf) | Figure 10-9: 후면 체결·외형 / Rear mounting and exterior envelope |
| XT60 / XT60H | [AMASS product catalog](https://www.china-amass.com/public/upload/20240723/c1ae9604bbe795ebfd366c9063019e3e.pdf) | Catalog page 13: 표준 단자 단면 / Standard connector cross sections |
| Arduino Mega 2560 | [Arduino hardware documentation](https://docs.arduino.cc/hardware/mega-2560/) | 기판 외곽·고정홀 / Board outline and mounting pattern |
| NT-S-DCDM1210 | 프로젝트에 제공된 제조사 매뉴얼 `NT-S-DCDM1210.pdf`, p.7 / Manufacturer manual supplied for the project, p.7 | 기판 외곽·고정홀, 매뉴얼 재배포 제외 / Board envelope and mounting pattern; manual not redistributed |
| SZH-EKBD-058 | [Product listing](https://www.devicemart.co.kr/goods/view?no=1342925), 프로젝트 실측 / project measurements | 본체 외형·사용자 정정 홀 간격·방열판 여유 / Body envelope, user-corrected hole pitch, heatsink clearance |
| SZH-EK334 | [Product listing](https://www.devicemart.co.kr/goods/view?no=10826138), 프로젝트 실측 / project measurements | 사용자 실측 고정홀 간격 / User-measured mounting-hole pitch |
| KIT0085 | [DFRobot official product](https://www.dfrobot.com/product-1203.html) | 모터·바퀴 제품 규격 / Motor and wheel specifications |
| Motor bracket | 사용자 제공 판매 도면 / User-supplied product drawing | 절곡 외형·중심 개구부·조정홀 / Formed envelope, center opening, adjustment holes |
| 3-inch casters | 사용자 제공 판매 도면 / User-supplied product drawing | 바퀴·장착판·회전축 치수 / Wheel, mounting plate, and swivel dimensions |
| Jetson Orin Nano Super / HFI-A9 | 사용자 지정 / User-specified components | 메인 PC·IMU 모델 / Main computer and IMU models |
| 해머형 T너트 / Hammer T-nut | 프로젝트 설계 참고 외형 / Project design reference envelope | 측면 판 키홀의 기준 외형 / Reference envelope for side-panel keyholes |

출력 부품의 치수에는 제품 규격, 사용자 실측, 설계 여유가 구분되어 있습니다. / Printed part dimensions distinguish product specifications, user measurements, and design clearances.
