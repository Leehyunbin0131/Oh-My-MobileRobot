# Printing instructions

[English README](../README.en.md) · [한국어](printing.ko.md) · [File index](parts.en.md)

This document covers STL orientations, slicer settings, and PDF drawing print settings. STL units are mm and the intended scale is 100%. File formats and downloads are in the [design file index](parts.en.md#file-formats).

<a id="orientation"></a>

## Print orientation

| Part | STL orientation and maximum height |
| --- | --- |
| Top deck | Flat outer face on the bed, underside ribs upward; maximum height 7 |
| Plain, 180 mm, and camera side panels | Flat outer face on the bed, inner ribs upward; maximum height 3 |
| D435i V2 bracket | Flat camera-contact face on the bed; maximum height 6.5 |
| Electronics trays | Flat underside on the bed, bosses upward; maximum height 6 |

Some STLs are centered around XY zero or offset sideways. Center them on the bed in the slicer. Minimum Z is aligned with the print face. The largest XY footprint is a 220 × 200 top panel, designed for a 250 × 250 bed.

<a id="fit-check"></a>

## Using the fit coupon

The [M3 fit coupon](parts.en.md#fit-coupon) compares standoff engagement at the tray interface. Print it with the same material, orientation, and settings as the final part. Interface dimensions are in [electronics tray specifications](design.en.md#electronics-trays).

<a id="slicer-settings"></a>

## Slicer settings

Choose filament, nozzle, layer height, wall count, and shrinkage compensation to suit the printer and material. Inspect the slicer preview to confirm that the thin 1 mm skin is retained.

<a id="drawing-printing"></a>

## Printing drawings

PDF drawings use **actual size / 100%** printing at 1:1 scale. Fit-to-page changes the dimensions. Measure the 50 mm scale bars on the deck and camera drawings to verify printing scale.

| Drawing | Pages and paper sizes |
| --- | --- |
| Top deck | 1 overall layout page on A1 + 4 individual panel pages on A3 |
| D435i bracket | 2 pages of part and mounting-space views on A4 |
| 180 mm side panel | 1 page on A4 |

Printing the overall deck and individual panel drawings at their original scale requires A1 and A3 paper, respectively. Drawing downloads are in the [printed part file index](parts.en.md#printed-parts).
