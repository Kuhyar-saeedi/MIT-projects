import streamlit as st
import plotly.graph_objects as go
import sys
from pathlib import Path
import base64

sys.path.insert(0, str(Path(__file__).parent.parent))
from utils.styles import inject

st.set_page_config(page_title="P1 — Sand Casting", page_icon="🏭", layout="wide")
inject()

ROOT = Path(__file__).parent.parent
PDF_PATH = ROOT / "pdfs" / "project1_sand_casting.pdf"

# ── Header ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero" style="border-top: 3px solid #FF6B35;">
  <p class="hero-meta">PROJECT 1 · SAND CASTING</p>
  <h1 class="hero-title" style="background: linear-gradient(90deg,#FF6B35,#FFB347);
     -webkit-background-clip:text;-webkit-text-fill-color:transparent;">
    Foundry Design
  </h1>
  <p class="hero-sub">
    Complete sand-casting cycle for a three-port steel junction housing —
    from machined geometry to mould-ready casting blank.
  </p>
  <span class="tag tag-orange">FeG 520 Cast Steel</span>
  <span class="tag tag-orange">Sand Casting</span>
  <span class="tag tag-gray">31 pages</span>
</div>
""", unsafe_allow_html=True)

# ── Key metrics ──────────────────────────────────────────────────────────────
st.markdown('<div class="section-hdr section-hdr-orange">📊 Key Numbers</div>', unsafe_allow_html=True)

m1,m2,m3,m4,m5,m6 = st.columns(6)
with m1:
    st.markdown('<div class="mtile"><div class="mtile-val" style="color:#FF6B35;">1.20 kg</div><div class="mtile-label">Part Mass</div></div>', unsafe_allow_html=True)
with m2:
    st.markdown('<div class="mtile"><div class="mtile-val" style="color:#FF6B35;">4.06 s</div><div class="mtile-label">Pouring Time</div></div>', unsafe_allow_html=True)
with m3:
    st.markdown('<div class="mtile"><div class="mtile-val" style="color:#FF6B35;">4.117 kg</div><div class="mtile-label">Poured Weight</div></div>', unsafe_allow_html=True)
with m4:
    st.markdown('<div class="mtile"><div class="mtile-val" style="color:#FF6B35;">3°</div><div class="mtile-label">Draft Angle</div></div>', unsafe_allow_html=True)
with m5:
    st.markdown('<div class="mtile"><div class="mtile-val" style="color:#FF6B35;">4 mm</div><div class="mtile-label">Machining Allowance</div></div>', unsafe_allow_html=True)
with m6:
    st.markdown('<div class="mtile"><div class="mtile-val" style="color:#FF6B35;">500 pcs</div><div class="mtile-label">Production Batch</div></div>', unsafe_allow_html=True)

st.markdown("")

# ── Thermal moduli chart ─────────────────────────────────────────────────────
st.markdown('<div class="section-hdr section-hdr-orange">🌡️ Thermal Analysis — Directional Solidification</div>', unsafe_allow_html=True)

col_chart, col_info = st.columns([3, 2], gap="large")

with col_chart:
    zones   = ["Zone A<br>(Horizontal arm)", "Zone D<br>(Left arm)", "Zone B<br>(Central hub)", "Zone C<br>(Upper branch)", "Riser<br>(MM = 1.0 cm)"]
    moduli  = [5.4, 6.8, 8.5, 8.5, 10.0]
    colors  = ["#FF8C42", "#FFB347", "#FF6B35", "#E05320", "#00D4FF"]
    annots  = ["M = 5.4 mm", "M = 6.8 mm", "M = 8.5 mm", "M = 8.5 mm", "M_M = 10 mm (sleeve)"]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=zones, y=moduli,
        marker_color=colors,
        text=annots,
        textposition="outside",
        textfont=dict(size=12, color="#E0E0E0"),
        width=0.55,
    ))
    fig.add_shape(
        type="line", x0=-0.5, x1=4.5, y0=10.0, y1=10.0,
        line=dict(color="#00D4FF", width=1.5, dash="dot"),
    )
    fig.add_annotation(x=4.4, y=10.3, text="Riser solidifies last", showarrow=False,
                       font=dict(color="#00D4FF", size=11))
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(20,30,46,0.6)",
        title=dict(text="Thermal Moduli per Zone (M = V / S)", font=dict(size=14, color="#E0E0E0")),
        yaxis=dict(title="Thermal Modulus M (mm)", gridcolor="#1E3A5F"),
        xaxis=dict(gridcolor="#1E3A5F"),
        margin=dict(t=50, b=40, l=50, r=20),
        height=380,
        showlegend=False,
    )
    st.plotly_chart(fig, use_container_width=True)

with col_info:
    st.markdown("""
    <div class="callout callout-orange">
      <strong>Solidification Order</strong><br>
      For sound directional solidification the modulus must <em>increase</em>
      by ~10–30 % toward the riser at each step.
    </div>
    """, unsafe_allow_html=True)
    st.markdown("""
    **Feed path analysis:**
    | Step | Δ Modulus | Status |
    |------|-----------|--------|
    | A → B | +58 % | ⚠️ Too steep → end chill on A |
    | D → B | +25 % | ✅ Within 10–30 % band |
    | B → C | +1 %  | ⚠️ Too flat → sleeve on C |
    | C → Riser | +18 % | ✅ Directional |

    **Corrective measures:**
    - Chills on Zone A and D extremities
    - Insulating/exothermic sleeve on Branch C
    - Fillet radii at the A→B junction
    """)

# ── Gating system ────────────────────────────────────────────────────────────
st.markdown('<div class="section-hdr section-hdr-orange">🔩 Gating System</div>', unsafe_allow_html=True)

gc1, gc2, gc3 = st.columns(3)
with gc1:
    st.markdown("""
    <div class="mtile">
      <div style="color:#FF6B35;font-size:0.75rem;font-weight:700;text-transform:uppercase;
                  letter-spacing:0.06em;margin-bottom:0.4rem;">Gating Ratio</div>
      <div style="font-size:2rem;font-weight:900;color:#FF6B35;">4 : 3 : 2</div>
      <div class="mtile-label">Sprue : Runner : Gate</div>
      <hr style="border-color:#1E3A5F;margin:0.6rem 0;">
      <div style="font-size:0.82rem;color:#9E9E9E;">
        Pressurised — gate is the choke<br>
        System stays back-filled
      </div>
    </div>
    """, unsafe_allow_html=True)
with gc2:
    sections = ["Sprue (SS)", "Runner (SR)", "Ingate (SG)"]
    areas    = [314, 240, 162]
    req      = [258.9, 194.1, 129.4]
    fig2 = go.Figure()
    fig2.add_trace(go.Bar(name="Required (mm²)", x=sections, y=req, marker_color="#2E4A6B", text=[f"{v:.0f}" for v in req], textposition="inside"))
    fig2.add_trace(go.Bar(name="Selected (mm²)", x=sections, y=areas, marker_color="#FF6B35", text=[f"{v:.0f}" for v in areas], textposition="inside"))
    fig2.update_layout(
        barmode="overlay", template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(20,30,46,0.6)",
        legend=dict(orientation="h", y=1.15, font=dict(size=10)),
        yaxis=dict(title="Area (mm²)", gridcolor="#1E3A5F"),
        margin=dict(t=30, b=20, l=40, r=10), height=240, showlegend=True,
    )
    st.plotly_chart(fig2, use_container_width=True)
with gc3:
    st.markdown("""
    | Section | Dimension | Area |
    |---------|-----------|------|
    | Sprue   | Ø 20 mm  | 314 mm² |
    | Runner  | 20 × 24 mm | 240 mm² |
    | Ingate  | 18 × 18 mm | 162 mm² |

    **Gate velocity:** 1.005 m/s
    **Effective head:** 121.8 mm
    **Choke area:** 129.4 mm²
    """)

# ── Riser & Flask ────────────────────────────────────────────────────────────
st.markdown('<div class="section-hdr section-hdr-orange">🏺 Riser & Metallostatic Verification</div>', unsafe_allow_html=True)

rc1, rc2, rc3 = st.columns(3)
with rc1:
    st.markdown("""
    <div class="mtile">
      <div style="color:#FF6B35;font-size:0.75rem;font-weight:700;
                  text-transform:uppercase;margin-bottom:0.4rem;">Riser</div>
      <div style="font-size:1.4rem;font-weight:800;color:#FF6B35;">Ø 54 × 81 mm</div>
      <div class="mtile-label">Single cylindrical riser + sleeve</div>
      <hr style="border-color:#1E3A5F;margin:0.6rem 0;">
      <div style="font-size:0.82rem;color:#9E9E9E;">
        M<sub>M</sub> = 1.0 cm &nbsp;·&nbsp; Vol = 180 cm³<br>
        Feeds up to 0.450 L / 3.52 kg<br>
        Casting needs 0.339 L / 2.64 kg ✅<br>
        <strong>43 % less metal vs modulus-only pick</strong>
      </div>
    </div>
    """, unsafe_allow_html=True)
with rc2:
    st.markdown("""
    <div class="mtile">
      <div style="color:#FF6B35;font-size:0.75rem;font-weight:700;
                  text-transform:uppercase;margin-bottom:0.4rem;">Flask</div>
      <div style="font-size:1.4rem;font-weight:800;color:#FF6B35;">315 × 400 × 250 mm</div>
      <div class="mtile-label">UNI 6765-70 standard</div>
      <hr style="border-color:#1E3A5F;margin:0.6rem 0;">
      <div style="font-size:0.82rem;color:#9E9E9E;">
        Sand: synthetic resin-bonded<br>
        Method: match-plate (single cavity)<br>
        Batch: 500 pieces
      </div>
    </div>
    """, unsafe_allow_html=True)
with rc3:
    # Metallostatic verification chart
    fig3 = go.Figure(go.Bar(
        x=["Lifting Force", "Cope Weight"],
        y=[22.1, 44.5],
        marker_color=["#FF6B35", "#00E676"],
        text=["22.1 kg", "44.5 kg (×2 margin)"],
        textposition="outside",
        textfont=dict(color="#E0E0E0"),
        width=0.4,
    ))
    fig3.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(20,30,46,0.6)",
        title=dict(text="Metallostatic Check", font=dict(size=13)),
        yaxis=dict(title="Force (kg)", gridcolor="#1E3A5F"),
        margin=dict(t=40, b=20, l=40, r=10), height=230,
    )
    st.plotly_chart(fig3, use_container_width=True)
    st.markdown('<div class="callout callout-green" style="margin-top:0;">Cope weight is <strong>2× the lifting force</strong> — no extra clamps needed ✅</div>', unsafe_allow_html=True)

# ── Component data ────────────────────────────────────────────────────────────
st.markdown('<div class="section-hdr section-hdr-orange">📐 Component Specifications</div>', unsafe_allow_html=True)
s1, s2 = st.columns(2)
with s1:
    st.markdown("""
    | Property | Finished Part | Casting Blank |
    |----------|--------------|---------------|
    | Material | FeG 520 cast steel | FeG 520 cast steel |
    | Length | 129 mm | 140.25 mm |
    | Mass | 1.20 kg | ~2.64 kg (excl. riser) |
    | Volume | 152 800 mm³ | 338 900 mm³ |
    | Draft angle | — | 3° uniform |
    | Fillet radii | R6 mm | R0.5 mm internal / R7–28.5 blend |
    | Machining allowance | — | 4 mm (grade B, 80–180 mm class) |
    """)
with s2:
    st.markdown("""
    **Key design decisions:**
    - Small bolt holes (Ø14) → cast solid, drill later
    - Central passages → cast solid (D/L ratio fails Table 2)
    - Parting line: horizontal plane separating cope & drag
    - 3 sand cores: 2 side cores + 1 upper branch core
    - Heuver inscribed-circle method verified wall thickness ≤ 30% variation
    - Single riser on Branch C (highest thermal modulus, natural feed path)
    """)

# ── PDF viewer ───────────────────────────────────────────────────────────────
st.markdown('<div class="section-hdr section-hdr-orange">📄 Full Report</div>', unsafe_allow_html=True)
with st.expander("Click to open / download the Project 1 PDF report", expanded=False):
    if PDF_PATH.exists():
        pdf_bytes = PDF_PATH.read_bytes()
        b64 = base64.b64encode(pdf_bytes).decode()
        st.markdown(
            f'<iframe src="data:application/pdf;base64,{b64}" width="100%" height="820px" style="border:none;border-radius:8px;"></iframe>',
            unsafe_allow_html=True
        )
        st.download_button("📥 Download PDF", data=pdf_bytes, file_name="Project1_SandCasting.pdf", mime="application/pdf")
    else:
        st.warning("PDF not found. Please ensure pdfs/project1_sand_casting.pdf exists.")
