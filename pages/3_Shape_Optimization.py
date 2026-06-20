import streamlit as st
import plotly.graph_objects as go
import sys
from pathlib import Path
import base64

sys.path.insert(0, str(Path(__file__).parent.parent))
from utils.styles import inject

st.set_page_config(page_title="P3 — Shape Optimization", page_icon="⚡", layout="wide")
inject()

ROOT = Path(__file__).parent.parent
PDF_PATH = ROOT / "pdfs" / "project3_shape_optimization.pdf"

# ── Header ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero" style="border-top: 3px solid #00E676;">
  <p class="hero-meta">PROJECT 3 · TOPOLOGY OPTIMIZATION</p>
  <h1 class="hero-title" style="background: linear-gradient(90deg,#00E676,#00D4FF);
     -webkit-background-clip:text;-webkit-text-fill-color:transparent;">
    Shape Optimization & Additive Manufacturing
  </h1>
  <p class="hero-sub">
    A steel plate is cut in half — by algorithm. Topology optimization removes
    material from low-stress regions; the organic result is validated structurally
    and prepared for 3D printing.
  </p>
  <span class="tag tag-green">Steel → ABS 3D Print</span>
  <span class="tag tag-green">50% Mass Target</span>
  <span class="tag tag-gray">30 pages</span>
</div>
""", unsafe_allow_html=True)

# ── Hero mass metric ──────────────────────────────────────────────────────────
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.metric("Original Mass", "8.94 kg", help="Steel plate before optimization")
with c2:
    st.metric("Optimized Mass", "4.51 kg", "−49.6 %", help="After topology optimization")
with c3:
    st.metric("Safety Factor", "≥ 4 everywhere", help="Well above yield threshold")
with c4:
    st.metric("Max von Mises", "6.6 MPa", help="Far below steel yield strength (~250 MPa)")

st.divider()

# ── Mass comparison ────────────────────────────────────────────────────────────
st.markdown('<div class="section-hdr section-hdr-green">⚖️ Mass Reduction</div>', unsafe_allow_html=True)

mass_col, info_col = st.columns([2, 3], gap="large")

with mass_col:
    fig_donut = go.Figure(go.Pie(
        labels=["Material Retained", "Material Removed"],
        values=[49.6, 50.4],
        hole=0.62,
        marker_colors=["#00E676", "#1E3A5F"],
        textinfo="label+percent",
        textfont=dict(size=13, color="white"),
        hovertemplate="%{label}: %{percent}<extra></extra>",
    ))
    fig_donut.add_annotation(
        text="−49.6%", showarrow=False,
        font=dict(size=26, color="#00E676", family="Arial Black"),
        x=0.5, y=0.5,
    )
    fig_donut.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        title=dict(text="Mass Ratio — Original vs Optimized", font=dict(size=13, color="#E0E0E0")),
        height=320, margin=dict(t=50, b=10, l=10, r=10),
        showlegend=True,
        legend=dict(orientation="h", y=-0.08),
    )
    st.plotly_chart(fig_donut, use_container_width=True)

with info_col:
    st.markdown("""
    <table class="cmp-table">
      <tr><th>Property</th><th>Original Plate</th><th>Optimized Body</th><th>Change</th></tr>
      <tr><td>Mass</td><td>8 935 g (8.94 kg)</td><td>4 507 g (4.51 kg)</td>
          <td><span class="best-badge">−49.6 %</span></td></tr>
      <tr><td>Volume</td><td>1.138 × 10⁶ mm³</td><td>5.741 × 10⁵ mm³</td><td>−49.6 %</td></tr>
      <tr><td>Material</td><td>Steel (0.008 g/mm³)</td><td>Steel → ABS print</td><td>—</td></tr>
      <tr><td>Bores</td><td>4 × circular</td><td>Preserved ✅</td><td>—</td></tr>
      <tr><td>Load capacity</td><td>4 × 1000 N</td><td>4 × 1000 N ✅</td><td>—</td></tr>
    </table>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="callout callout-green" style="margin-top:1rem;">
      <strong>Key insight:</strong> The optimizer retained mass ratio was 51.22% —
      essentially hitting the 50% target exactly. The organic skeleton connects
      the four bore hubs via curved, diagonal ribs following the true load paths.
      This shape <em>cannot</em> be machined conventionally — additive manufacturing
      is the only practical route.
    </div>
    """, unsafe_allow_html=True)

# ── Workflow timeline ─────────────────────────────────────────────────────────
st.markdown('<div class="section-hdr section-hdr-green">🔄 4-Phase Workflow</div>', unsafe_allow_html=True)

steps = [
    ("1. Shape Optimization", "#00E676",
     "Target body = original solid plate. Objective: minimize mass to ≤50% while maximizing stiffness. "
     "4 × 1000 N in-plane forces on bore faces. Fixed constraints on bore faces. Mesh: model-based, fine. "
     "3 cloud credits. Result: organic skeleton with mass ratio 51.22%."),
    ("2. Geometry Reconstruction", "#00D4FF",
     "Coarse optimization mesh → repair (Rebuild, adaptive, density 128) → remesh 9,506 → 102,546 facets "
     "while mass stays constant at ~4.57 kg → Organic solid conversion (NOT faceted — smooth free-form) "
     "→ re-cut 4 cylindrical bores with symmetric Extrude/Cut."),
    ("3. Static Structural Validation", "#7B61FF",
     "Same boundary conditions as optimization (4 × 1000 N, fixed bore faces). Cloud FEA result: "
     "max von Mises = 6.587 MPa (far below steel yield), max displacement = 7.08 × 10⁻⁴ mm (sub-micron), "
     "safety factor ≥ 4 everywhere. The lightened part is structurally safe."),
    ("4. Additive Manufacturing", "#FF6B35",
     "Prusa XL, ABS, 0.15 mm layers, 0.4 mm nozzle. PrusaSlicer reveals the real cost: 342 g total, "
     "of which 43.5% (150 g) is support material. Print time: 2 days 8 hours. Estimated cost: €9.51. "
     "Lesson: organic optimized shapes are expensive to print because of overhangs."),
]

for title, color, desc in steps:
    with st.expander(title, expanded=False):
        st.markdown(f'<div class="callout" style="border-left-color:{color};">{desc}</div>', unsafe_allow_html=True)

# ── Structural results ────────────────────────────────────────────────────────
st.markdown('<div class="section-hdr section-hdr-green">🔬 Static Structural Results</div>', unsafe_allow_html=True)

r1, r2, r3, r4 = st.columns(4)
with r1:
    st.markdown("""
    <div class="mtile">
      <div class="mtile-val" style="color:#00E676;">6.587 MPa</div>
      <div class="mtile-label">Max von Mises Stress</div>
      <div style="font-size:0.78rem;color:#7A8FA6;margin-top:4px;">Steel yield ~250 MPa<br>Safety margin: ×38</div>
    </div>""", unsafe_allow_html=True)
with r2:
    st.markdown("""
    <div class="mtile">
      <div class="mtile-val" style="color:#00E676;">7.08 × 10⁻⁴ mm</div>
      <div class="mtile-label">Max Total Displacement</div>
      <div style="font-size:0.78rem;color:#7A8FA6;margin-top:4px;">Sub-micron — effectively rigid</div>
    </div>""", unsafe_allow_html=True)
with r3:
    st.markdown("""
    <div class="mtile">
      <div class="mtile-val" style="color:#00E676;">≥ 4</div>
      <div class="mtile-label">Safety Factor</div>
      <div style="font-size:0.78rem;color:#7A8FA6;margin-top:4px;">Above target everywhere<br>(target band 2–4)</div>
    </div>""", unsafe_allow_html=True)
with r4:
    st.markdown("""
    <div class="mtile">
      <div class="mtile-val" style="color:#00E676;">3.71 × 10⁻⁵</div>
      <div class="mtile-label">Max Equivalent Strain</div>
      <div style="font-size:0.78rem;color:#7A8FA6;margin-top:4px;">Very small elastic strain</div>
    </div>""", unsafe_allow_html=True)

# ── 3D print breakdown ────────────────────────────────────────────────────────
st.markdown('<div class="section-hdr section-hdr-green">🖨️ 3D Print Breakdown (PrusaSlicer)</div>', unsafe_allow_html=True)

pc1, pc2 = st.columns([2, 3], gap="large")

with pc1:
    features = ["Support material", "Internal infill", "Solid infill", "Perimeter", "Support interface", "Ext. perimeter", "Other"]
    time_hrs  = [24.53, 9.18, 6.63, 3.60, 1.87, 1.82, 0.80]
    filament  = [149.78, 83.76, 42.48, 35.56, 6.16, 17.13, 7.13]
    colors_p  = ["#FF6B35","#00D4FF","#7B61FF","#00E676","#FFB347","#FF61AB","#8B949E"]

    fig_pie = go.Figure(go.Pie(
        labels=features, values=time_hrs,
        marker_colors=colors_p,
        hole=0.45,
        textinfo="label+percent",
        textfont=dict(size=11),
        hovertemplate="%{label}<br>Time: %{value:.1f} h<extra></extra>",
    ))
    fig_pie.add_annotation(text="342 g<br>total", showarrow=False,
                           font=dict(size=14, color="#E0E0E0"), x=0.5, y=0.5)
    fig_pie.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        title=dict(text="Print Time by Feature", font=dict(size=13)),
        height=350, margin=dict(t=50, b=10),
        legend=dict(orientation="v", font=dict(size=10)),
    )
    st.plotly_chart(fig_pie, use_container_width=True)

with pc2:
    st.markdown("""
    | Feature | Time | Share | Material |
    |---------|------|-------|----------|
    | **Support material** | 1 d 0 h 32 m | **43.5 %** | 149.78 g |
    | Internal infill | 9 h 11 m | 16.3 % | 83.76 g |
    | Solid infill | 6 h 38 m | 11.8 % | 42.48 g |
    | Perimeter | 3 h 36 m | 6.4 % | 35.56 g |
    | Support interface | 1 h 52 m | 3.3 % | 6.16 g |
    | External perimeter | 1 h 49 m | 3.2 % | 17.13 g |
    | **Total** | **2 d 8 h 20 m** | 100 % | **342 g** |

    **Machine:** Prusa XL, 0.25 mm nozzle, 0.12 mm layers
    **Filament:** Generic ABS
    **Part size:** 280.56 × 280.80 × 71.62 mm
    **Estimated cost:** € 9.51
    """)
    st.markdown("""
    <div class="callout callout-orange">
      <strong>The hidden cost of organic shapes:</strong> 43.5% of the entire print —
      a full day of machine time and 150 g of filament — is wasted as support material.
      This is the trade-off that only a dedicated slicer reveals: the algorithm makes
      the part light, but the overhanging ribs are expensive to manufacture additively.
    </div>
    """, unsafe_allow_html=True)

# ── Mesh reconstruction stats ─────────────────────────────────────────────────
st.markdown('<div class="section-hdr section-hdr-green">🔺 Mesh Reconstruction Stages</div>', unsafe_allow_html=True)

stages   = ["After Repair\n(coarse)", "Intermediate", "Refined", "Final (smooth)"]
facets   = [9506, 13204, 52820, 102546]
vertices = [4737, 6586, 26394, 51257]
masses   = [4563.8, 4568.6, 4567.3, 4570.5]

fig_mesh = go.Figure()
fig_mesh.add_trace(go.Bar(
    x=stages, y=facets, name="Facet count",
    marker_color="#00E676", yaxis="y",
))
fig_mesh.add_trace(go.Scatter(
    x=stages, y=masses, name="Mass (g)",
    marker=dict(color="#FF6B35", size=10), line=dict(color="#FF6B35", width=2),
    yaxis="y2", mode="lines+markers",
))
fig_mesh.update_layout(
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(20,30,46,0.6)",
    title=dict(text="Facet count rises 11×; mass stays constant — discretization only", font=dict(size=13)),
    yaxis=dict(title="Facet Count", gridcolor="#1E3A5F"),
    yaxis2=dict(title="Mass (g)", overlaying="y", side="right",
                range=[4550, 4580], showgrid=False),
    legend=dict(orientation="h", y=1.12),
    height=320, margin=dict(t=50, b=30, l=60, r=60),
)
st.plotly_chart(fig_mesh, use_container_width=True)

# ── PDF ───────────────────────────────────────────────────────────────────────
st.divider()
st.markdown('<div class="section-hdr section-hdr-green">📄 Full Report</div>', unsafe_allow_html=True)
with st.expander("Click to open / download the Project 3 PDF report", expanded=False):
    if PDF_PATH.exists():
        pdf_bytes = PDF_PATH.read_bytes()
        b64 = base64.b64encode(pdf_bytes).decode()
        st.markdown(
            f'<iframe src="data:application/pdf;base64,{b64}" width="100%" height="820px" style="border:none;border-radius:8px;"></iframe>',
            unsafe_allow_html=True
        )
        st.download_button("📥 Download PDF", data=pdf_bytes, file_name="Project3_ShapeOptimization.pdf", mime="application/pdf")
    else:
        st.warning("PDF not found.")
