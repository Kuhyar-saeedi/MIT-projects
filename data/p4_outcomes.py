import pandas as pd

OUTCOMES = [
    {"Outcome": 11,   "Material": "ABS Plastic",   "Process": "Unrestricted",   "Mass_kg": 0.392,  "Min_SF": 10.95,  "VonMises_MPa": 1.83, "MaxDisp_mm": 0.0653, "Score": 75.5, "Selected": False, "Rejected": False},
    {"Outcome": 12,   "Material": "ABS Plastic",   "Process": "Additive",       "Mass_kg": 0.393,  "Min_SF": 10.58,  "VonMises_MPa": 1.89, "MaxDisp_mm": 0.0659, "Score": 55.2, "Selected": False, "Rejected": False},
    {"Outcome": 19,   "Material": "Al AlSi10Mg",   "Process": "Unrestricted",   "Mass_kg": 0.987,  "Min_SF": 131.30, "VonMises_MPa": 1.83, "MaxDisp_mm": 0.0021, "Score": 89.9, "Selected": True,  "Rejected": False},
    {"Outcome": 20,   "Material": "Al AlSi10Mg",   "Process": "Additive",       "Mass_kg": 0.989,  "Min_SF": 126.80, "VonMises_MPa": 1.89, "MaxDisp_mm": 0.0021, "Score": 69.9, "Selected": False, "Rejected": False},
    {"Outcome": 1,    "Material": "Aluminium",      "Process": "Unrestricted",   "Mass_kg": 0.998,  "Min_SF": 150.10, "VonMises_MPa": 1.83, "MaxDisp_mm": 0.0021, "Score": 89.8, "Selected": False, "Rejected": False},
    {"Outcome": 2,    "Material": "Aluminium",      "Process": "Additive",       "Mass_kg": 1.000,  "Min_SF": 145.10, "VonMises_MPa": 1.89, "MaxDisp_mm": 0.0021, "Score": 69.8, "Selected": False, "Rejected": False},
    {"Outcome": 14,   "Material": "ABS Plastic",   "Process": "3-axis Milling", "Mass_kg": 1.171,  "Min_SF": 5.87,   "VonMises_MPa": 3.41, "MaxDisp_mm": 0.2317, "Score": 46.8, "Selected": False, "Rejected": False},
    {"Outcome": 13,   "Material": "ABS Plastic",   "Process": "2-axis Cutting", "Mass_kg": 1.240,  "Min_SF": 21.48,  "VonMises_MPa": 0.93, "MaxDisp_mm": 0.0333, "Score": 90.0, "Selected": False, "Rejected": True},
    {"Outcome": 15,   "Material": "ABS Plastic",   "Process": "Casting",        "Mass_kg": 1.531,  "Min_SF": 21.68,  "VonMises_MPa": 0.92, "MaxDisp_mm": 0.0289, "Score": 85.3, "Selected": False, "Rejected": False},
    {"Outcome": 6,    "Material": "Steel",          "Process": "Unrestricted",   "Mass_kg": 2.903,  "Min_SF": 112.60, "VonMises_MPa": 1.84, "MaxDisp_mm": 0.0007, "Score": 68.2, "Selected": False, "Rejected": False},
    {"Outcome": 7,    "Material": "Steel",          "Process": "Additive",       "Mass_kg": 2.908,  "Min_SF": 109.10, "VonMises_MPa": 1.90, "MaxDisp_mm": 0.0007, "Score": 48.1, "Selected": False, "Rejected": False},
    {"Outcome": "4/17","Material": "Al 6061",       "Process": "3-axis Milling", "Mass_kg": 2.982,  "Min_SF": 80.40,  "VonMises_MPa": 3.42, "MaxDisp_mm": 0.0076, "Score": 68.5, "Selected": False, "Rejected": False},
    {"Outcome": "3/16","Material": "Al 6061",       "Process": "2-axis Cutting", "Mass_kg": 3.159,  "Min_SF": 294.90, "VonMises_MPa": 0.93, "MaxDisp_mm": 0.0011, "Score": 67.1, "Selected": False, "Rejected": False},
    {"Outcome": 18,   "Material": "Al A356-T6",    "Process": "Casting",        "Mass_kg": 3.854,  "Min_SF": 179.00, "VonMises_MPa": 0.92, "MaxDisp_mm": 0.0009, "Score": 43.2, "Selected": False, "Rejected": False},
    {"Outcome": 5,    "Material": "Aluminium",      "Process": "Casting",        "Mass_kg": 3.897,  "Min_SF": 298.30, "VonMises_MPa": 0.92, "MaxDisp_mm": 0.0009, "Score": 41.8, "Selected": False, "Rejected": False},
    {"Outcome": 9,    "Material": "Steel",          "Process": "3-axis Milling", "Mass_kg": 8.670,  "Min_SF": 60.40,  "VonMises_MPa": 3.43, "MaxDisp_mm": 0.0025, "Score": 0.0,  "Selected": False, "Rejected": False},
    {"Outcome": 8,    "Material": "Steel",          "Process": "2-axis Cutting", "Mass_kg": 9.170,  "Min_SF": 221.80, "VonMises_MPa": 0.93, "MaxDisp_mm": 0.0004, "Score": 0.0,  "Selected": False, "Rejected": False},
    {"Outcome": 10,   "Material": "Steel",          "Process": "Casting",        "Mass_kg": 11.330, "Min_SF": 225.20, "VonMises_MPa": 0.92, "MaxDisp_mm": 0.0003, "Score": 0.0,  "Selected": False, "Rejected": False},
]

MATERIAL_COLORS = {
    "ABS Plastic":  "#FF6B35",
    "Al AlSi10Mg":  "#00D4FF",
    "Aluminium":    "#00B4D8",
    "Al 6061":      "#0096C7",
    "Al A356-T6":   "#0077B6",
    "Steel":        "#8B949E",
}

def get_df():
    return pd.DataFrame(OUTCOMES)
