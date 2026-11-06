# 설계 파일 목록

[한국어 README](../README.md) · [English](parts.en.md) · [치수·체결 규격](design.ko.md) · [출력 방향](printing.ko.md)

CAD·출력·ROS 파일의 다운로드와 원본 구성을 안내합니다. 치수와 체결부는 [출력 부품 설계 규격](design.ko.md), 출력·인쇄 설정은 [출력·인쇄 방법](printing.ko.md), 모델 실행은 [ROS·ROS 2 모델 사용](ros.ko.md)에 있습니다.

<a id="printed-parts"></a>

## 출력 부품 파일

| 부품 | 파일 구성 | 다운로드 |
| --- | --- | --- |
| [상판](design.ko.md#top-deck) | 전면 좌·우판, 후면 좌·우판 | [STL](../hardware/top-deck/print) · [CAD](../hardware/top-deck/cad) · [1:1 도면](../hardware/top-deck/drawings/top-deck-1to1.pdf) |
| [측면 커버](design.ko.md#side-panels) | 200 / 220 / 180 mm 판 | [STL](../hardware/side-panels/print) · [CAD](../hardware/side-panels/cad) · [180 mm 판 1:1 도면](../hardware/side-panels/drawings/side-panel-180-1to1.pdf) |
| [D435i 고정부](design.ko.md#camera-mount) | 전면 좌·우 커버, V2 브라켓 | [STL](../hardware/camera-mount/print) · [CAD](../hardware/camera-mount/cad) · [1:1 도면](../hardware/camera-mount/drawings/d435i-bracket-v2-1to1.pdf) |
| [전장판](design.ko.md#electronics-trays) | 아래판, 위판 | [STL](../hardware/electronics-tray/print) · [CAD](../hardware/electronics-tray/cad) |

<a id="fit-coupon"></a>

M3 체결 시험편: [STL 다운로드](../hardware/electronics-tray/print/m3-pilot-fit-coupon.stl) · [사용 방법](printing.ko.md#fit-check)

### 카메라 원본 파일 구성

- [camera-panels.sc](../hardware/camera-mount/cad/camera-panels.sc): 좌·우 커버의 편집 이력과 숨겨진 초기 브라켓 형상이 포함되어 있으며, 두 커버만 표시됩니다.
- [d435i-bracket-v2.sc](../hardware/camera-mount/cad/d435i-bracket-v2.sc): 현재 V2 브라켓 원본입니다. 대응하는 출력 파일은 [d435i-bracket-v2.stl](../hardware/camera-mount/print/d435i-bracket-v2.stl)입니다.

<a id="assembly-models"></a>

## 전체 모델과 확장 예시

각 모델의 외형과 배치 치수는 [전체 모델과 확장 예시](full-model.ko.md)에 있습니다.

| 모델 | CAD 원본 및 STEP |
| --- | --- |
| 기본 베이스 | <sub>[SolidCraft](../hardware/assembly/full-robot-reference.sc) · [STEP](../hardware/assembly/full-robot-reference.step)</sub> |
| 적재함형 개념 모델 | <sub>[SolidCraft](../hardware/application-examples/cargo-concept.sc) · [STEP](../hardware/application-examples/cargo-concept.step)</sub> |
| 6축 로봇암형 개념 모델 | <sub>[SolidCraft](../hardware/application-examples/arm-concept.sc) · [STEP](../hardware/application-examples/arm-concept.step)</sub> |
| 안내 디스플레이형 개념 모델 | <sub>[SolidCraft](../hardware/application-examples/display-concept.sc) · [STEP](../hardware/application-examples/display-concept.step)</sub> |

<a id="ros-models"></a>

## ROS 모델 파일

[oh_my_mobilerobot_description 패키지](../ros/oh_my_mobilerobot_description)를 전체 다운로드해 사용합니다. URDF는 패키지 안의 메시를 참조합니다.

| 파일 | 내용 |
| --- | --- |
| [기본 베이스](../ros/oh_my_mobilerobot_description/urdf/base.urdf) | `base` URDF |
| [적재함형](../ros/oh_my_mobilerobot_description/urdf/cargo.urdf) | `cargo` URDF |
| [로봇암형](../ros/oh_my_mobilerobot_description/urdf/arm.urdf) | `arm` URDF |
| [디스플레이형](../ros/oh_my_mobilerobot_description/urdf/display.urdf) | `display` URDF |
| [공통 Xacro](../ros/oh_my_mobilerobot_description/urdf/oh_my_mobilerobot.urdf.xacro) | 모델 선택과 링크·관절 이름 접두사 |
| [시각화 메시](../ros/oh_my_mobilerobot_description/meshes/visual) | 링크 좌표에 맞춘 m 단위 STL |
| [실행 파일](../ros/oh_my_mobilerobot_description/launch) · [RViz 설정](../ros/oh_my_mobilerobot_description/rviz) | ROS 1·ROS 2용 표시 설정 |
| [CAD 매핑](../ros/oh_my_mobilerobot_description/config/cad_mapping.json) · [메시 명세](../ros/oh_my_mobilerobot_description/config/mesh_manifest.json) | 원본 연결·좌표·색상·SHA-256·경계 |
| [변환 도구](../tools/generate_ros_description.py) · [검사](../tests/test_ros_description.py) | CAD 기반 재생성과 모델 검사 |

빌드·실행·좌표계·수정 방법은 [ROS 문서](ros.ko.md)에 있습니다.

<a id="file-formats"></a>

## 파일 형식과 선택

| 형식 | 내용 |
| --- | --- |
| `.sc` | 편집 가능한 SolidCraft 원본 |
| `.step` | CAD 프로그램 간 교환용 솔리드 형상 |
| `.stl` | `hardware/**/print/`: 출력 메시(mm), `ros/**/meshes/visual/`: 시각화 메시(m) |
| `.pdf` | 부품·배치 도면 |
| `.urdf` | ROS 링크·관절·시각화·충돌 형상 정의 |
| `.xacro` | 모델 선택·이름 접두사가 있는 공통 URDF 원본 |

출력 대상은 각 부품의 `print/` 폴더에 있는 STL입니다. CAD 원본의 숨겨진 참고 기판·프로파일은 출력 대상이 아닙니다. 전체 외형과 응용 모델은 CAD 편집·교환용 SolidCraft·STEP과 ROS용 URDF·Xacro로 제공합니다. 출력 단위·배율은 [출력·인쇄 방법](printing.ko.md), ROS 단위·좌표는 [ROS 문서](ros.ko.md#frames)에 있습니다.
