# Design file index

[Overall view](../README.en.md) · [한국어](parts.ko.md) · [Dimensions and fasteners](design.en.md) · [Print orientations](printing.en.md)

This index covers downloads and source file contents. See [printed part design specifications](design.en.md) for dimensions and mounting interfaces, and [printing instructions](printing.en.md) for output settings.

<a id="printed-parts"></a>

## Printed part files

| Part | Included files | Downloads |
| --- | --- | --- |
| [Top deck](design.en.md#top-deck) | Front left/right and rear left/right panels | [STL](../hardware/top-deck/print) · [CAD](../hardware/top-deck/cad) · [1:1 drawing](../hardware/top-deck/drawings/top-deck-1to1.pdf) |
| [Side covers](design.en.md#side-panels) | 200 / 220 / 180 mm panels | [STL](../hardware/side-panels/print) · [CAD](../hardware/side-panels/cad) · [180 mm panel 1:1 drawing](../hardware/side-panels/drawings/side-panel-180-1to1.pdf) |
| [D435i mount](design.en.md#camera-mount) | Left/right front covers and V2 bracket | [STL](../hardware/camera-mount/print) · [CAD](../hardware/camera-mount/cad) · [1:1 drawing](../hardware/camera-mount/drawings/d435i-bracket-v2-1to1.pdf) |
| [Electronics trays](design.en.md#electronics-trays) | Lower and upper trays | [STL](../hardware/electronics-tray/print) · [CAD](../hardware/electronics-tray/cad) |

<a id="fit-coupon"></a>

M3 fit coupon: [download STL](../hardware/electronics-tray/print/m3-pilot-fit-coupon.stl) · [usage](printing.en.md#fit-check)

### Camera source file contents

- [camera-panels.sc](../hardware/camera-mount/cad/camera-panels.sc): contains the left/right cover history and a hidden earlier bracket; only the two covers are displayed.
- [d435i-bracket-v2.sc](../hardware/camera-mount/cad/d435i-bracket-v2.sc): the current V2 bracket source. Its printable counterpart is [d435i-bracket-v2.stl](../hardware/camera-mount/print/d435i-bracket-v2.stl).

<a id="assembly-models"></a>

## Complete model and application concepts

See [complete model and application concepts](full-model.en.md) for each model's exterior and layout dimensions.

| Model | CAD source and STEP |
| --- | --- |
| Base platform | <sub>[SolidCraft](../hardware/assembly/full-robot-reference.sc) · [STEP](../hardware/assembly/full-robot-reference.step)</sub> |
| Cargo carrier concept | <sub>[SolidCraft](../hardware/application-examples/cargo-concept.sc) · [STEP](../hardware/application-examples/cargo-concept.step)</sub> |
| Six-axis robot arm concept | <sub>[SolidCraft](../hardware/application-examples/arm-concept.sc) · [STEP](../hardware/application-examples/arm-concept.step)</sub> |
| Information display concept | <sub>[SolidCraft](../hardware/application-examples/display-concept.sc) · [STEP](../hardware/application-examples/display-concept.step)</sub> |

<a id="file-formats"></a>

## File formats and selection

| Format | Contents |
| --- | --- |
| `.sc` | Editable SolidCraft source |
| `.step` | Solid geometry for exchange between CAD programs |
| `.stl` | Individual part print mesh |
| `.pdf` | Part and layout drawings |

Use the STLs in each part's `print/` folder for printing. Hidden reference boards and extrusions in CAD sources are not printable parts. Complete exterior and application models are available as SolidCraft and STEP files. Units and scale are covered in [printing instructions](printing.en.md).
