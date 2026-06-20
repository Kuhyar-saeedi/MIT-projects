import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import sys
from pathlib import Path
import base64
from PIL import Image

sys.path.insert(0, str(Path(__file__).parent.parent))
from utils.styles import inject
from data.p2_studies import get_df, PHASE_LABELS

st.set_page_config(page_title="P2 — Injection Molding", page_icon="💉", layout="wide")
inject()

ROOT = Path(__file__).parent.parent
PDF_PATH = ROOT / "pdfs" / "project2_injection_molding.pdf"
ASSETS   = ROOT / "assets"

df_all = get_df()
df_pp  = df_all[df_all["Material"] == "PP"].copy()
df_mod = df_all[(df_all["Geometry"] == "Modified") & (df_all["Material"] == "PP")].copy()

PHASE_COLORS = {1:"#FF6B35",2:"#FFB347",3:"#00D4FF",4:"#00E676",
                5:"#7B61FF",6:"#FF61AB",7:"#FF9F1C",8:"#2EC4B6",9:"#FF6B35"}

# ── Header ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero" style="border-top: 3px solid #00D4FF;">
  <p class="hero-meta">PROJECT 2 · INJECTION MOLDING SIMULATION</p>
  <h1 class="hero-title">18 Parametric Studies</h1>
  <p class="hero-sub">
    Remote Control Housing — PP (Studies 1–17) and ABS (Study 18) —
    8 experimental phases optimising gate count, melt temperature and mold temperature.
  </p>
  <span class="tag tag-cyan">Generic PP</span>
  <span class="tag tag-cyan">Generic ABS</span>
  <span class="tag tag-cyan">18 Studies</span>
  <span class="tag tag-gray">Autodesk Fusion Cloud Solver</span>
</div>
""", unsafe_allow_html=True)

# ── Top KPIs ─────────────────────────────────────────────────────────────────
k1,k2,k3,k4,k5 = st.columns(5)
with k1: st.metric("Total Studies", "18")
with k2: st.metric("Best Deflection", "0.062 mm", "-77 % vs baseline", help="Study 9: 2G, cold mold 30 °C")
with k3: st.metric("Min Weld Faces", "32", "-47% vs 1-gate", help="Study 7: cooler melt 200 °C")
with k4: st.metric("Geometry Improvement", "52 → 34", "weld faces after modification")
with k5: st.metric("ABS Shrinkage", "0.437 %", "vs 1.734% PP (−75%)")

st.divider()

# ── Tabs ─────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📈 Interactive Charts",
    "📋 All 18 Studies",
    "🔬 Phase Analysis",
    "🧪 PP vs ABS",
    "📸 Before / After & Steps",
])

# ════════════════════════════════════════════════════════════════════════
with tab1:
    st.markdown('<div class="section-hdr">Deflection vs Study — All 18 Runs</div>', unsafe_allow_html=True)

    # Main scatter: deflection across all studies
    fig = go.Figure()
    for phase_id, phase_name in PHASE_LABELS.items():
        sub = df_all[df_all["Phase"] == phase_id]
        if sub.empty:
            continue
        fig.add_trace(go.Scatter(
            x=sub["Study"], y=sub["Deflection_mm"],
            mode="markers+lines" if phase_id <= 8 else "markers",
            name=f"Ph {phase_id}",
            marker=dict(size=sub["Gates"]*5+6, color=PHASE_COLORS[phase_id],
                        line=dict(width=1, color="white"), opacity=0.85),
            line=dict(color=PHASE_COLORS[phase_id], width=1.5, dash="dot"),
            text=sub["Label"], hovertemplate=(
                "<b>Study %{x}</b><br>Deflection: %{y:.3f} mm<br>%{text}<extra></extra>"
            ),
        ))
    # Best marker
    best = df_all[df_all["Study"] == 9].iloc[0]
    fig.add_annotation(x=9, y=0.062, text="★ BEST<br>Study 9", showarrow=True,
                       arrowhead=2, arrowcolor="#00E676", font=dict(color="#00E676", size=11),
                       ax=30, ay=-40)
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(20,30,46,0.6)",
        title=dict(text="Out-of-Plane Deflection per Study (marker size = gate count)", font=dict(size=14)),
        xaxis=dict(title="Study #", dtick=1, gridcolor="#1E3A5F"),
        yaxis=dict(title="Deflection (mm)", gridcolor="#1E3A5F"),
        legend=dict(orientation="h", y=-0.18, font=dict(size=10)),
        height=420, margin=dict(t=50, b=80, l=60, r=20),
    )
    st.plotly_chart(fig, use_container_width=True)

    # ── Weld faces vs Deflection scatter ─────────────────────────────────
    st.markdown('<div class="section-hdr">Weld Faces vs Deflection — Quality Map (Studies 4–18)</div>', unsafe_allow_html=True)
    df_qual = df_all[df_all["Study"] >= 4].dropna(subset=["Sink_Faces"])

    fig2 = px.scatter(
        df_qual, x="Weld_Faces", y="Deflection_mm",
        color="Gates", color_continuous_scale=["#FF6B35","#00D4FF","#7B61FF","#00E676"],
        size=[8]*len(df_qual),
        text="Study",
        hover_data={"Label": True, "Material": True, "Mold_C": True},
        labels={"Weld_Faces": "Weld-Line Faces (aesthetic)", "Deflection_mm": "Deflection (mm)"},
    )
    fig2.add_annotation(x=34, y=0.062, text="Study 9 ★<br>Best overall",
                        showarrow=True, arrowhead=2, arrowcolor="#00E676",
                        font=dict(color="#00E676", size=11), ax=-60, ay=-30)
    fig2.add_annotation(x=32, y=0.083, text="Study 7<br>Fewest welds",
                        showarrow=True, arrowhead=2, arrowcolor="#00D4FF",
                        font=dict(color="#00D4FF", size=11), ax=-60, ay=30)
    fig2.update_traces(textposition="top center", textfont=dict(size=9))
    fig2.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(20,30,46,0.6)",
        height=420, margin=dict(t=40, b=40, l=60, r=20),
        title=dict(text="Lower-left = fewer defects. Color = gate count.", font=dict(size=13)),
    )
    st.plotly_chart(fig2, use_container_width=True)

    st.markdown("""
    <div class="callout">
      <strong>Reading the chart:</strong> The ideal study sits in the <em>bottom-left corner</em> —
      fewest weld faces AND lowest deflection. Study 9 and Study 7 are closest to that ideal.
      Studies with 4 gates (Study 10) move catastrophically to the top-right.
    </div>
    """, unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown('<div class="section-hdr">Complete Study Table</div>', unsafe_allow_html=True)

    display_df = df_all[["Study","Geometry","Gates","Melt_C","Mold_C",
                          "Fill_s","Pressure_MPa","Deflection_mm","Shrinkage_pct",
                          "Weld_Faces","Sink_Faces","Material","Label"]].copy()
    display_df.columns = ["Study","Geometry","Gates","Melt °C","Mold °C",
                           "Fill (s)","Pressure (MPa)","Deflect (mm)","Shrink (%)","Weld ✦","Sink ✦","Mat","Notes"]

    def color_row(row):
        styles = [""] * len(row)
        if row["Study"] in [9, 17]:
            return ["background-color:rgba(0,230,118,0.12)"] * len(row)
        if row["Study"] == 7:
            return ["background-color:rgba(0,212,255,0.10)"] * len(row)
        if row["Mat"] == "ABS":
            return ["background-color:rgba(255,107,53,0.10)"] * len(row)
        return styles

    styled = display_df.style.apply(color_row, axis=1).format({
        "Deflect (mm)": "{:.3f}",
        "Shrink (%)":   "{:.3f}",
        "Pressure (MPa)": "{:.3f}",
        "Fill (s)":     "{:.2f}",
    }, na_rep="—")
    st.dataframe(styled, use_container_width=True, height=560)

    st.markdown("""
    <div class="callout">
      🟢 <strong>Green</strong>: Study 9/17 — best deflection &nbsp;·&nbsp;
      🔵 <strong>Blue</strong>: Study 7 — fewest weld faces &nbsp;·&nbsp;
      🟠 <strong>Orange</strong>: Study 18 — ABS material &nbsp;·&nbsp;
      ✦ counts on 146 aesthetic faces (Studies 4–18 only)
    </div>
    """, unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown('<div class="section-hdr">Phase-by-Phase Results</div>', unsafe_allow_html=True)

    phase_summaries = {
        1: ("Studies 1–2", "Single-gate baseline on original geometry. 60 weld-line faces across all model faces. Deflection 0.266 mm. No aesthetic faces designated yet."),
        2: ("Studies 3–4", "Added a second gate (Study 3: −18% pressure), then introduced the geometry modification (Study 4: boss cluster simplified). Weld faces on aesthetic surfaces dropped from 52 → 34, establishing the comparable baseline."),
        3: ("Studies 5–7", "Melt temperature sweep (200–260 °C), 2 gates. Study 7 at 200 °C achieved the fewest weld faces of the campaign (32) and deflection of only 0.083 mm. Higher melt → lower pressure but more welds."),
        4: ("Studies 8–9", "Mold temperature sweep: 70 °C (warm) vs 30 °C (cold). Study 9 cold mold: deflection 0.062 mm — a 77% reduction vs the 2-gate baseline. Selected as the best PP configuration."),
        5: ("Studies 10–11", "Gate count increased to 3 and 4. Paradoxically worsened results: 4 gates produced the highest weld count (42) and worst deflection (0.831 mm). More gates ≠ better quality for this geometry."),
        6: ("Studies 12–13", "Verification runs. Study 12 confirmed 1-gate baseline with aesthetic faces. Study 13 showed gate position matters — same settings as Study 8 but different position → 40 weld faces vs 37."),
        7: ("Studies 14–16", "Three gates + warm mold + melt sweep (220–232 °C). Consistently underperformed: deflection 0.443–0.464 mm, weld faces 38–41, shrinkage peaked at ~2.05%."),
        8: ("Study 17", "Independent verification repeat of Study 9. Identical results confirmed — deflection 0.062 mm, 34 weld faces. Reproducibility validated."),
    }

    for ph_id in range(1, 9):
        title, summary = phase_summaries[ph_id]
        color = PHASE_COLORS[ph_id]
        sub = df_all[df_all["Phase"] == ph_id]
        with st.expander(f"**Phase {ph_id} — {title}** ({PHASE_LABELS[ph_id]})", expanded=(ph_id == 4)):
            st.markdown(f'<div class="callout" style="border-left-color:{color};">{summary}</div>', unsafe_allow_html=True)
            if not sub.empty:
                cols_show = ["Study","Gates","Melt_C","Mold_C","Fill_s","Pressure_MPa","Deflection_mm","Weld_Faces","Sink_Faces","Label"]
                cols_show = [c for c in cols_show if c in sub.columns]
                st.dataframe(sub[cols_show].rename(columns={
                    "Melt_C":"Melt °C","Mold_C":"Mold °C","Fill_s":"Fill (s)",
                    "Pressure_MPa":"Pressure (MPa)","Deflection_mm":"Deflect (mm)",
                    "Weld_Faces":"Weld ✦","Sink_Faces":"Sink ✦","Label":"Notes"
                }).style.format({"Deflect (mm)":"{:.3f}","Pressure (MPa)":"{:.3f}","Fill (s)":"{:.2f}"}, na_rep="—"),
                use_container_width=True)

# ════════════════════════════════════════════════════════════════════════
with tab4:
    st.markdown('<div class="section-hdr">PP vs ABS — Same Configuration, Different Materials</div>', unsafe_allow_html=True)
    st.markdown("""
    Study 18 cloned the best PP configuration (Study 9: 2 gates, melt 220 °C, mold 30 °C)
    and swapped **Generic PP (crystalline)** for **Generic ABS (amorphous)**.
    """)

    # Comparison bar charts
    metrics_labels = ["Fill Time (s)", "Pressure at Switch (MPa)", "Deflection (mm)", "Shrinkage (%)", "Weld Faces", "Sink Faces"]
    pp_vals  = [0.31, 14.537, 0.062, 1.734, 34, 7]
    abs_vals = [0.63, 42.972, 0.123, 0.437, 34, 5]
    delta    = ["+103%", "+195%", "+98%", "−75%", "=", "−29%"]
    better   = ["PP", "PP", "PP", "ABS", "Tie", "ABS"]

    fig_cmp = go.Figure()
    fig_cmp.add_trace(go.Bar(
        name="PP (Study 9)", x=metrics_labels, y=pp_vals,
        marker_color="#00D4FF", text=[f"{v}" for v in pp_vals], textposition="outside",
    ))
    fig_cmp.add_trace(go.Bar(
        name="ABS (Study 18)", x=metrics_labels, y=abs_vals,
        marker_color="#FF6B35", text=[f"{v}" for v in abs_vals], textposition="outside",
    ))
    fig_cmp.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(20,30,46,0.6)",
        barmode="group",
        title=dict(text="PP vs ABS — Identical Gate/Temperature Setup", font=dict(size=14)),
        yaxis=dict(gridcolor="#1E3A5F"),
        legend=dict(orientation="h", y=1.12),
        height=400, margin=dict(t=60, b=40, l=50, r=20),
    )
    st.plotly_chart(fig_cmp, use_container_width=True)

    # Key comparison table
    st.markdown("#### Metric-by-metric comparison")
    st.markdown("""
    <table class="cmp-table">
      <tr><th>Metric</th><th>PP — Study 9</th><th>ABS — Study 18</th><th>Δ</th><th>Winner</th></tr>
      <tr><td>Fill time</td><td>0.31 s</td><td>0.63 s</td><td>+103 %</td><td><span class="tag tag-cyan">PP</span></td></tr>
      <tr><td>Injection pressure</td><td>14.537 MPa</td><td>42.972 MPa</td><td>+195 %</td><td><span class="tag tag-cyan">PP</span></td></tr>
      <tr><td>Max packing pressure</td><td>37.045 MPa</td><td>56.948 MPa</td><td>+54 %</td><td><span class="tag tag-cyan">PP</span></td></tr>
      <tr><td>Out-of-plane deflection</td><td>0.062 mm</td><td>0.123 mm</td><td>+98 %</td><td><span class="tag tag-cyan">PP</span></td></tr>
      <tr><td>Mold shrinkage</td><td>1.734 %</td><td>0.437 %</td><td>−75 %</td><td><span class="tag tag-orange">ABS</span></td></tr>
      <tr><td>Weld-line faces</td><td>34</td><td>34</td><td>= same</td><td>Tie</td></tr>
      <tr><td>Sink-mark faces</td><td>7</td><td>5</td><td>−29 %</td><td><span class="tag tag-orange">ABS</span></td></tr>
    </table>
    """, unsafe_allow_html=True)
    st.markdown("""
    <div class="callout" style="margin-top:1rem;">
      <strong>Why the differences?</strong> PP is <em>semi-crystalline</em> — it undergoes a sharp
      volumetric shrinkage during crystallization, driving high mold shrinkage (~1.7%) and better
      dimensional response to cold-mold cooling. ABS is <em>amorphous</em> — no crystallization
      transition, so shrinkage is purely thermal (~0.4%) but higher flow-induced residual stresses
      cause worse deflection despite lower overall shrinkage.
    </div>
    """, unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════
with tab5:
    st.markdown('<div class="section-hdr">Geometry Modification — Before & After</div>', unsafe_allow_html=True)
    st.markdown("The central internal boss cluster was simplified between Studies 3 and 4, reducing weld-line faces on aesthetic surfaces from 52 → 34.")

    bef_images = sorted(ASSETS.glob("geo_before_photo_*.jpg"))
    aft_images = sorted(ASSETS.glob("geo_after_photo_*.jpg"))

    if bef_images and aft_images:
        ba_cols = st.columns(len(bef_images) + len(aft_images))
        for i, img_path in enumerate(bef_images):
            with ba_cols[i]:
                st.markdown(f'<div style="text-align:center;color:#FF6B35;font-size:0.75rem;font-weight:700;margin-bottom:4px;">BEFORE — View {i+1}</div>', unsafe_allow_html=True)
                st.image(str(img_path), use_container_width=True)
        for i, img_path in enumerate(aft_images):
            with ba_cols[len(bef_images) + i]:
                st.markdown(f'<div style="text-align:center;color:#00E676;font-size:0.75rem;font-weight:700;margin-bottom:4px;">AFTER — View {i+1}</div>', unsafe_allow_html=True)
                st.image(str(img_path), use_container_width=True)
    else:
        st.info("Images not found in assets/ directory.")

    st.divider()
    st.markdown('<div class="section-hdr">Simulation Setup — 8-Step Workflow</div>', unsafe_allow_html=True)
    step_labels = [
        "Target Body Selection",
        "Material Selection",
        "Injection Location",
        "Aesthetic Faces",
        "Process Settings",
        "Pre-Check",
        "Cloud Solve",
        "Job Status Monitor",
    ]
    step_images = sorted(ASSETS.glob("step_*.jpg"))
    if step_images:
        n_cols = 4
        rows = [step_images[i:i+n_cols] for i in range(0, len(step_images), n_cols)]
        for row_imgs in rows:
            cols = st.columns(n_cols)
            for j, img_path in enumerate(row_imgs):
                step_num = int(img_path.stem.split("_")[-1])
                with cols[j]:
                    label = step_labels[step_num - 1] if step_num <= len(step_labels) else f"Step {step_num}"
                    st.markdown(f'<div style="text-align:center;color:#00D4FF;font-size:0.72rem;font-weight:700;margin-bottom:4px;">Step {step_num}: {label}</div>', unsafe_allow_html=True)
                    st.image(str(img_path), use_container_width=True)
    else:
        st.info("Step images not found in assets/ directory.")

# ── PDF viewer ───────────────────────────────────────────────────────────────
st.divider()
st.markdown('<div class="section-hdr">📄 Full Report</div>', unsafe_allow_html=True)
with st.expander("Click to open / download the Project 2 PDF report", expanded=False):
    if PDF_PATH.exists():
        pdf_bytes = PDF_PATH.read_bytes()
        b64 = base64.b64encode(pdf_bytes).decode()
        st.markdown(
            f'<iframe src="data:application/pdf;base64,{b64}" width="100%" height="820px" style="border:none;border-radius:8px;"></iframe>',
            unsafe_allow_html=True
        )
        st.download_button("📥 Download PDF", data=pdf_bytes, file_name="Project2_InjectionMolding.pdf", mime="application/pdf")
    else:
        st.warning("PDF not found.")
