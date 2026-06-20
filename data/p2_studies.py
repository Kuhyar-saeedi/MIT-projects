import pandas as pd

STUDIES = [
    {"Study": 1,  "Geometry": "Original", "Gates": 1, "Melt_C": 220, "Mold_C": 50,  "Fill_s": 0.42, "Pressure_MPa": 16.167, "Deflection_mm": 0.266, "Shrinkage_pct": 1.500, "Weld_Faces": 60, "Sink_Faces": None, "Material": "PP",  "Phase": 1, "Label": "Baseline 1G"},
    {"Study": 2,  "Geometry": "Original", "Gates": 1, "Melt_C": 220, "Mold_C": 50,  "Fill_s": 0.42, "Pressure_MPa": 16.167, "Deflection_mm": 0.266, "Shrinkage_pct": 1.500, "Weld_Faces": 60, "Sink_Faces": None, "Material": "PP",  "Phase": 1, "Label": "Baseline 1G repeat"},
    {"Study": 3,  "Geometry": "Original", "Gates": 2, "Melt_C": 220, "Mold_C": 50,  "Fill_s": 0.42, "Pressure_MPa": 13.229, "Deflection_mm": 0.161, "Shrinkage_pct": 1.769, "Weld_Faces": 52, "Sink_Faces": None, "Material": "PP",  "Phase": 2, "Label": "2G original geom"},
    {"Study": 4,  "Geometry": "Modified", "Gates": 2, "Melt_C": 220, "Mold_C": 50,  "Fill_s": 0.42, "Pressure_MPa": 13.229, "Deflection_mm": 0.161, "Shrinkage_pct": 1.769, "Weld_Faces": 34, "Sink_Faces": 7,    "Material": "PP",  "Phase": 2, "Label": "2G modified geom"},
    {"Study": 5,  "Geometry": "Modified", "Gates": 2, "Melt_C": 240, "Mold_C": 50,  "Fill_s": 0.31, "Pressure_MPa": 12.234, "Deflection_mm": 0.178, "Shrinkage_pct": 1.734, "Weld_Faces": 37, "Sink_Faces": 7,    "Material": "PP",  "Phase": 3, "Label": "Melt +20 °C"},
    {"Study": 6,  "Geometry": "Modified", "Gates": 2, "Melt_C": 260, "Mold_C": 50,  "Fill_s": 0.21, "Pressure_MPa": 11.987, "Deflection_mm": 0.212, "Shrinkage_pct": 1.701, "Weld_Faces": 34, "Sink_Faces": 7,    "Material": "PP",  "Phase": 3, "Label": "Melt +40 °C"},
    {"Study": 7,  "Geometry": "Modified", "Gates": 2, "Melt_C": 200, "Mold_C": 50,  "Fill_s": 0.42, "Pressure_MPa": 15.552, "Deflection_mm": 0.083, "Shrinkage_pct": 1.763, "Weld_Faces": 32, "Sink_Faces": 7,    "Material": "PP",  "Phase": 3, "Label": "Melt −20 °C ★"},
    {"Study": 8,  "Geometry": "Modified", "Gates": 2, "Melt_C": 220, "Mold_C": 70,  "Fill_s": 0.42, "Pressure_MPa": 12.761, "Deflection_mm": 0.254, "Shrinkage_pct": 1.776, "Weld_Faces": 37, "Sink_Faces": 7,    "Material": "PP",  "Phase": 4, "Label": "Warm mold 70 °C"},
    {"Study": 9,  "Geometry": "Modified", "Gates": 2, "Melt_C": 220, "Mold_C": 30,  "Fill_s": 0.31, "Pressure_MPa": 14.537, "Deflection_mm": 0.062, "Shrinkage_pct": 1.734, "Weld_Faces": 34, "Sink_Faces": 7,    "Material": "PP",  "Phase": 4, "Label": "Cold mold 30 °C ★★"},
    {"Study": 10, "Geometry": "Modified", "Gates": 4, "Melt_C": 220, "Mold_C": 50,  "Fill_s": 0.31, "Pressure_MPa":  6.652, "Deflection_mm": 0.831, "Shrinkage_pct": 1.870, "Weld_Faces": 42, "Sink_Faces": 5,    "Material": "PP",  "Phase": 5, "Label": "4 gates"},
    {"Study": 11, "Geometry": "Modified", "Gates": 3, "Melt_C": 220, "Mold_C": 50,  "Fill_s": 0.31, "Pressure_MPa":  8.455, "Deflection_mm": 0.229, "Shrinkage_pct": 1.869, "Weld_Faces": 37, "Sink_Faces": 8,    "Material": "PP",  "Phase": 5, "Label": "3 gates"},
    {"Study": 12, "Geometry": "Modified", "Gates": 1, "Melt_C": 220, "Mold_C": 50,  "Fill_s": 0.42, "Pressure_MPa": 16.189, "Deflection_mm": 0.269, "Shrinkage_pct": 1.509, "Weld_Faces": 35, "Sink_Faces": 7,    "Material": "PP",  "Phase": 6, "Label": "1G verification"},
    {"Study": 13, "Geometry": "Modified", "Gates": 2, "Melt_C": 220, "Mold_C": 70,  "Fill_s": 0.42, "Pressure_MPa": 11.082, "Deflection_mm": 0.496, "Shrinkage_pct": 1.735, "Weld_Faces": 40, "Sink_Faces": 5,    "Material": "PP",  "Phase": 6, "Label": "Alt gate pos."},
    {"Study": 14, "Geometry": "Modified", "Gates": 3, "Melt_C": 220, "Mold_C": 70,  "Fill_s": 0.31, "Pressure_MPa":  6.650, "Deflection_mm": 0.443, "Shrinkage_pct": 2.035, "Weld_Faces": 39, "Sink_Faces": 8,    "Material": "PP",  "Phase": 7, "Label": "3G warm mold"},
    {"Study": 15, "Geometry": "Modified", "Gates": 3, "Melt_C": 227, "Mold_C": 70,  "Fill_s": 0.31, "Pressure_MPa":  6.299, "Deflection_mm": 0.443, "Shrinkage_pct": 2.034, "Weld_Faces": 38, "Sink_Faces": 8,    "Material": "PP",  "Phase": 7, "Label": "3G warm +7 °C"},
    {"Study": 16, "Geometry": "Modified", "Gates": 3, "Melt_C": 232, "Mold_C": 70,  "Fill_s": 0.31, "Pressure_MPa":  6.096, "Deflection_mm": 0.464, "Shrinkage_pct": 2.051, "Weld_Faces": 41, "Sink_Faces": 8,    "Material": "PP",  "Phase": 7, "Label": "3G warm +12 °C"},
    {"Study": 17, "Geometry": "Modified", "Gates": 2, "Melt_C": 220, "Mold_C": 30,  "Fill_s": 0.31, "Pressure_MPa": 14.537, "Deflection_mm": 0.062, "Shrinkage_pct": 1.734, "Weld_Faces": 34, "Sink_Faces": 7,    "Material": "PP",  "Phase": 8, "Label": "Repeat S9 ✓"},
    {"Study": 18, "Geometry": "Modified", "Gates": 2, "Melt_C": 220, "Mold_C": 30,  "Fill_s": 0.63, "Pressure_MPa": 42.972, "Deflection_mm": 0.123, "Shrinkage_pct": 0.437, "Weld_Faces": 34, "Sink_Faces": 5,    "Material": "ABS", "Phase": 9, "Label": "ABS material"},
]

PHASE_LABELS = {
    1: "Phase 1 — Single-Gate Baseline",
    2: "Phase 2 — Dual-Gate & Geometry Change",
    3: "Phase 3 — Melt Temperature Sweep",
    4: "Phase 4 — Mold Temperature Sweep",
    5: "Phase 5 — Gate Count Exploration",
    6: "Phase 6 — Verification & Alt. Config",
    7: "Phase 7 — Three-Gate Thermal Opt.",
    8: "Phase 8 — Verification Repeat",
    9: "ABS Material Comparison",
}

def get_df():
    return pd.DataFrame(STUDIES)
