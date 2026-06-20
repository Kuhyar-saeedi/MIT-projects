import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import sys
from pathlib import Path
import base64

sys.path.insert(0, str(Path(__file__).parent.parent))
from utils.styles import inject
from data.p4_outcomes import get_df, MATERIAL_COLORS

st.set_page_config(page_title="P4 — Generative Design", page_icon="🤖", layout="wide")
inject()

ROOT = Path(__file__).parent.parent
PDF_PATH = ROOT / "pdfs" / "project4_generative_design.pdf"

df = get_df()
df_num = df[pd.to_numeric(df["Outcome"], errors="coerce").notna()].copy()
df_num["Outcome"] = df_num["Outcome"].astype(int)

# ── Header ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero" style="border-top: 3px solid #7B61FF;">
  <p class="hero-meta">PROJECT 4 · GENERATIVE DESIGN</p>
  <h1 class="hero-title" style="background: linear-gradient(90deg,#7B61FF,#00D4FF);
     -webkit-background-clip:text;-webkit-text-fill-color:transparent;">
    AI-Generated Structural Geometries
  </h1>
  <p class="hero-sub">
    Same load case as Project 3 — but inverted philosophy. No starting solid:
    the software autonomously generates 20 valid designs across 6 materials and
    5 manufacturing methods from boundary conditions alone.
  </p>
  <span class="tag tag-purple">20 Outcomes</span>
  <span class="tag tag-purple">6 Materials</span>
  <span class="tag tag-purple">5 Manufacturing Methods</span>
  <span class="tag tag-gray">SF ≥ 2 guaranteed</span>
</div>
""", unsafe_allow_html=True)

# ── KPIs ────────────────────────────────────────────────────────────────────
k1,k2,k3,k4 = st.columns(4)
with k1: st.metric("Outcomes Generated", "20", "16 converged + 4 completed")
with k2: st.metric("Selected (Outcome 19)", "0.987 kg", "AlSi10Mg — Unrestricted")
with k3: st.metric("Min Safety Factor", "131.3×", "Outcome 19 — massively over-designed")
with k4: st.metric("Max Displacement", "0.00205 mm", "Outcome 19 — extremely stiff")

st.divider()

# ── Main scatter ──────────────────────────────────────────────────────────────
st.markdown('<div class="section-hdr section-hdr-purple">🗺️ All 20 Outcomes — Mass vs Safety Factor</div>', unsafe_allow_html=True)

fig = go.Figure()

for mat, color in MATERIAL_COLORS.items():
    sub = df[df["Material"] == mat]
    if sub.empty:
        continue
    sel = sub[sub["Selected"] == True]
    rej = sub[sub["Rejected"] == True]
    norm = sub[(sub["Selected"] == False) & (sub["Rejected"] == False)]

    for grp, marker_sym, size, opacity, label_sfx in [
        (norm, "circle",   10, 0.85, ""),
        (sel,  "star",     20, 1.0,  " ★ SELECTED"),
        (rej,  "x",        12, 0.6,  " ✕ rejected"),
    ]:
        if grp.empty:
            continue
        fig.add_trace(go.Scatter(
            x=grp["Mass_kg"], y=grp["Min_SF"],
            mode="markers",
            name=f"{mat}{label_sfx}",
            marker=dict(symbol=marker_sym, size=size, color=color,
                        line=dict(width=1.5 if label_sfx else 0.5, color="white"),
                        opacity=opacity),
            text=grp["Outcome"].astype(str),
            hovertemplate=(
                "<b>Outcome %{text}</b><br>"
                f"Material: {mat}<br>"
                "Mass: %{x:.3f} kg<br>"
                "Min SF: %{y:.1f}<br>"
                "<extra></extra>"
            ),
            customdata=grp[["Process","Score"]].values,
        ))

fig.add_vline(x=4.51, line_dash="dot", line_color="#00E676",
              annotation_text="P3 steel result (4.51 kg)", annotation_font_color="#00E676",
              annotation_position="top right")
fig.add_vrect(x0=0, x1=2.0, fillcolor="rgba(123,97,255,0.06)",
              layer="below", line_width=0,
              annotation_text="Better than P3 steel", annotation_position="top left",
              annotation_font_color="#7B61FF")

fig.update_layout(
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(20,30,46,0.6)",
    title=dict(text="Outcome Map: Mass (kg) vs Minimum Safety Factor — colored by material",
               font=dict(size=14, color="#E0E0E0")),
    xaxis=dict(title="Mass (kg)", gridcolor="#1E3A5F", type="log"),
    yaxis=dict(title="Min Safety Factor", gridcolor="#1E3A5F", type="log"),
    legend=dict(orientation="v", x=1.02, font=dict(size=10)),
    height=520, margin=dict(t=60, b=40, l=60, r=180),
)
st.plotly_chart(fig, use_container_width=True)
st.markdown("""
<div class="callout callout-purple">
  <strong>Reading the chart:</strong> Both axes use log scale. The ideal outcome sits in the
  <em>bottom-right</em> (light + strong). Dashed green line = Project 3's steel reference (4.51 kg).
  All outcomes to its left beat P3 at the same load. ★ = selected Outcome 19.
</div>
""", unsafe_allow_html=True)

# ── Full outcomes table ───────────────────────────────────────────────────────
st.markdown('<div class="section-hdr section-hdr-purple">📋 All Outcomes — Sorted by Mass</div>', unsafe_allow_html=True)

display_df = df[["Outcome","Material","Process","Mass_kg","Min_SF","VonMises_MPa","MaxDisp_mm","Score","Selected","Rejected"]].copy()
display_df.columns = ["Outcome","Material","Process","Mass (kg)","Min SF","σ_vM (MPa)","Max Disp (mm)","Score (%)","Selected","Rejected"]
display_df = display_df.sort_values("Mass (kg)")

def style_outcome(row):
    if row["Selected"]:
        return ["background-color:rgba(123,97,255,0.20)"] * len(row)
    if row["Rejected"]:
        return ["background-color:rgba(255,107,53,0.10)"] * len(row)
    return [""] * len(row)

styled = display_df.drop(columns=["Selected","Rejected"]).style.apply(
    style_outcome, axis=1, subset=pd.IndexSlice[:, :]
).format({"Mass (kg)":"{:.3f}","Min SF":"{:.1f}","σ_vM (MPa)":"{:.2f}","Max Disp (mm)":"{:.4f}","Score (%)":"{:.1f}"}, na_rep="—")
# Re-apply without the boolean cols
display_for_style = df[["Outcome","Material","Process","Mass_kg","Min_SF","VonMises_MPa","MaxDisp_mm","Score","Selected","Rejected"]].sort_values("Mass_kg").copy()

def row_bg(row):
    if row["Selected"]:
        return ["background-color:rgba(123,97,255,0.20)"] * 9
    if row["Rejected"]:
        return ["background-color:rgba(255,107,53,0.10)"] * 9
    return [""] * 9

view_df = display_for_style[["Outcome","Material","Process","Mass_kg","Min_SF","VonMises_MPa","MaxDisp_mm","Score"]].copy()
view_df.columns = ["Outcome","Material","Process","Mass (kg)","Min SF","σ_vM (MPa)","Max Disp (mm)","Score (%)"]
styled2 = view_df.style.apply(
    lambda row: (["background-color:rgba(123,97,255,0.20)"] * 8
                 if display_for_style.loc[row.name, "Selected"]
                 else (["background-color:rgba(255,107,53,0.10)"] * 8
                       if display_for_style.loc[row.name, "Rejected"]
                       else [""] * 8)),
    axis=1
).format({"Mass (kg)":"{:.3f}","Min SF":"{:.1f}","σ_vM (MPa)":"{:.2f}","Max Disp (mm)":"{:.4f}","Score (%)":"{:.1f}"}, na_rep="—")
st.dataframe(styled2, use_container_width=True, height=520)

st.markdown("""
<div class="callout callout-purple">
  🟣 <strong>Purple</strong>: Outcome 19 — selected final design &nbsp;·&nbsp;
  🟠 <strong>Orange</strong>: Outcome 13 — rejected (ABS plastic, inappropriate for structural part)
</div>
""", unsafe_allow_html=True)

# ── Selected outcome detail ───────────────────────────────────────────────────
st.markdown('<div class="section-hdr section-hdr-purple">★ Selected: Outcome 19</div>', unsafe_allow_html=True)

s1, s2, s3 = st.columns(3)
with s1:
    st.markdown("""
    <div class="mtile" style="border: 2px solid #7B61FF;">
      <div style="color:#7B61FF;font-size:0.72rem;font-weight:700;text-transform:uppercase;margin-bottom:0.4rem;">OUTCOME 19 — SELECTED</div>
      <div class="mtile-val" style="color:#7B61FF;">0.987 kg</div>
      <div class="mtile-label">Final mass</div>
      <hr style="border-color:#2E4A6B;margin:0.5rem 0;">
      <div style="font-size:0.82rem;color:#9E9E9E;">
        Material: Aluminium AlSi10Mg<br>
        Process: Unrestricted<br>
        Min SF: 131.3 &nbsp;·&nbsp; Recommendation: 89.86%
      </div>
    </div>
    """, unsafe_allow_html=True)
with s2:
    st.markdown("""
    <div class="mtile">
      <div style="color:#00D4FF;font-size:0.72rem;font-weight:700;text-transform:uppercase;margin-bottom:0.4rem;">OUTCOME 1 — RUNNER-UP</div>
      <div class="mtile-val" style="color:#00D4FF;">0.998 kg</div>
      <div class="mtile-label">Marginal mass increase</div>
      <hr style="border-color:#2E4A6B;margin:0.5rem 0;">
      <div style="font-size:0.82rem;color:#9E9E9E;">
        Material: Aluminium (generic)<br>
        Process: Unrestricted<br>
        Min SF: 150.1 &nbsp;·&nbsp; Recommendation: 89.81%
      </div>
    </div>
    """, unsafe_allow_html=True)
with s3:
    st.markdown("""
    <div class="mtile">
      <div style="color:#00E676;font-size:0.72rem;font-weight:700;text-transform:uppercase;margin-bottom:0.4rem;">OUTCOME 20 — BEST ADDITIVE</div>
      <div class="mtile-val" style="color:#00E676;">0.989 kg</div>
      <div class="mtile-label">Best additive-optimized shape</div>
      <hr style="border-color:#2E4A6B;margin:0.5rem 0;">
      <div style="font-size:0.82rem;color:#9E9E9E;">
        Material: Aluminium AlSi10Mg<br>
        Process: Additive<br>
        Min SF: 126.8 &nbsp;·&nbsp; Recommendation: 69.85%
      </div>
    </div>
    """, unsafe_allow_html=True)

# ── Manufacturing methods ─────────────────────────────────────────────────────
st.markdown('<div class="section-hdr section-hdr-purple">🏭 Mass by Manufacturing Method</div>', unsafe_allow_html=True)

method_order = ["Unrestricted","Additive","2-axis Cutting","3-axis Milling","Casting"]
method_colors = {"Unrestricted":"#7B61FF","Additive":"#00E676","2-axis Cutting":"#00D4FF",
                 "3-axis Milling":"#FFB347","Casting":"#FF6B35"}

fig2 = go.Figure()
for proc in method_order:
    sub = df[df["Process"] == proc].sort_values("Mass_kg")
    if sub.empty:
        continue
    fig2.add_trace(go.Bar(
        x=sub["Material"], y=sub["Mass_kg"],
        name=proc,
        marker_color=method_colors.get(proc, "#9E9E9E"),
        text=[f"{m:.2f} kg" for m in sub["Mass_kg"]],
        textposition="outside",
        textfont=dict(size=10),
    ))
fig2.add_hline(y=4.51, line_dash="dot", line_color="#00E676",
               annotation_text="P3 topology ref. (4.51 kg)",
               annotation_font_color="#00E676")
fig2.update_layout(
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(20,30,46,0.6)",
    barmode="group",
    title=dict(text="Component mass by material and manufacturing process", font=dict(size=13)),
    yaxis=dict(title="Mass (kg)", gridcolor="#1E3A5F"),
    legend=dict(orientation="h", y=-0.20),
    height=420, margin=dict(t=50, b=80, l=60, r=20),
)
st.plotly_chart(fig2, use_container_width=True)

# ── PDF ───────────────────────────────────────────────────────────────────────
st.divider()
st.markdown('<div class="section-hdr section-hdr-purple">📄 Full Report</div>', unsafe_allow_html=True)
with st.expander("Click to open / download the Project 4 PDF report", expanded=False):
    if PDF_PATH.exists():
        pdf_bytes = PDF_PATH.read_bytes()
        b64 = base64.b64encode(pdf_bytes).decode()
        st.markdown(
            f'<iframe src="data:application/pdf;base64,{b64}" width="100%" height="820px" style="border:none;border-radius:8px;"></iframe>',
            unsafe_allow_html=True
        )
        st.download_button("📥 Download PDF", data=pdf_bytes, file_name="Project4_GenerativeDesign.pdf", mime="application/pdf")
    else:
        st.warning("PDF not found.")
