# 설계 파일 목록

[전체 모습](../README.md) · [English](parts.en.md) · [치수·체결 규격](design.ko.md) · [출력 방향](printing.ko.md)

부품별 다운로드와 원본 파일 구성을 안내합니다. 치수와 체결부는 [출력 부품 설계 규격](design.ko.md), 출력·인쇄 설정은 [출력·인쇄 방법](printing.ko.md)에 있습니다.

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

<a id="file-formats"></a>

## 파일 형식과 선택

| 형식 | 내용 |
| --- | --- |
| `.sc` | 편집 가능한 SolidCraft 원본 |
| `.step` | CAD 프로그램 간 교환용 솔리드 형상 |
| `.stl` | 개별 부품의 출력 메시 |
| `.pdf` | 부품·배치 도면 |

출력 대상은 각 부품의 `print/` 폴더에 있는 STL입니다. CAD 원본의 숨겨진 참고 기판·프로파일은 출력 대상이 아닙니다. 전체 외형과 응용 모델은 SolidCraft와 STEP으로 제공합니다. 단위·배율은 [출력·인쇄 방법](printing.ko.md)에 있습니다.
