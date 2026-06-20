import streamlit as st
import plotly.graph_objects as go
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from utils.styles import inject

st.set_page_config(page_title="P3 vs P4 — Comparison", page_icon="⚖️", layout="wide")
inject()

# ── Header ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero" style="border-top: 3px solid #FFB347;">
  <p class="hero-meta">CROSS-PROJECT COMPARISON</p>
  <h1 class="hero-title" style="background: linear-gradient(90deg,#00E676,#FFB347,#7B61FF);
     -webkit-background-clip:text;-webkit-text-fill-color:transparent;">
    P3 vs P4 — Same Problem, Two Philosophies
  </h1>
  <p class="hero-sub">
    Projects 3 and 4 solve the <strong>identical structural problem</strong> —
    same steel component, same 4 × 1000 N in-plane load, same fixed bore constraints —
    using opposite design strategies. The results tell a striking story about the
    limits of topology optimization vs the power of generative design.
  </p>
  <span class="tag tag-green">P3: Topology Optimization</span>
  <span class="tag tag-purple">P4: Generative Design</span>
  <span class="tag tag-gray">Same load · Same part · Different outcome</span>
</div>
""", unsafe_allow_html=True)

# ── Side-by-side philosophy ──────────────────────────────────────────────────
st.markdown('<div class="section-hdr">🧠 Philosophy Comparison</div>', unsafe_allow_html=True)

ph_col1, ph_col2 = st.columns(2, gap="large")

with ph_col1:
    st.markdown("""
    <div class="pcard" style="border-top: 3px solid #00E676;">
      <p style="color:#00E676;font-size:0.75rem;font-weight:700;text-transform:uppercase;">PROJECT 3 — TOPOLOGY OPTIMIZATION</p>
      <h3 style="color:#00E676;margin:0 0 0.8rem 0;">Start with everything, remove what isn't needed</h3>
      <div style="font-size:0.88rem;color:#C0D0E0;line-height:1.7;">
        <p>1. Begin with the full solid steel plate as the <em>design space</em></p>
        <p>2. Apply loads and constraints to the finite element model</p>
        <p>3. Algorithm iteratively removes material from low-stress regions</p>
        <p>4. Stop when target mass (50%) is reached and stiffness is maximized</p>
        <p>5. Result: one geometry in the chosen material (steel)</p>
      </div>
      <hr style="border-color:#1E3A5F;margin:0.8rem 0;">
      <div>
        <span class="tag tag-green">Deterministic</span>
        <span class="tag tag-green">Single material</span>
        <span class="tag tag-green">One result</span>
        <span class="tag tag-gray">Engineer sets target</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

with ph_col2:
    st.markdown("""
    <div class="pcard" style="border-top: 3px solid #7B61FF;">
      <p style="color:#7B61FF;font-size:0.75rem;font-weight:700;text-transform:uppercase;">PROJECT 4 — GENERATIVE DESIGN</p>
      <h3 style="color:#7B61FF;margin:0 0 0.8rem 0;">Start with nothing, generate what is needed</h3>
      <div style="font-size:0.88rem;color:#C0D0E0;line-height:1.7;">
        <p>1. Define only the <em>boundary conditions</em>: preserved zones, obstacles, loads, constraints</p>
        <p>2. Specify candidate materials and manufacturing methods</p>
        <p>3. Algorithm generates valid geometry for every material–method combination</p>
        <p>4. All results satisfy SF ≥ 2 by construction</p>
        <p>5. Engineer selects from 20 generated candidates</p>
      </div>
      <hr style="border-color:#1E3A5F;margin:0.8rem 0;">
      <div>
        <span class="tag tag-purple">Exploratory</span>
        <span class="tag tag-purple">Multi-material</span>
        <span class="tag tag-purple">20 results</span>
        <span class="tag tag-gray">AI-driven</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# ── Results comparison chart ──────────────────────────────────────────────────
st.markdown('<div class="section-hdr">📊 Mass Results — The Same Load, Very Different Weights</div>', unsafe_allow_html=True)

scenarios = [
    "Original<br>Steel Plate",
    "P3: Topology<br>Steel (−49.6%)",
    "P4: Gen. Design<br>Steel (Outcome 6)",
    "P4: Gen. Design<br>Al 6061 Milling",
    "P4: Gen. Design<br>Aluminium Unres.",
    "P4: Gen. Design<br>AlSi10Mg ★",
    "P4: Gen. Design<br>ABS Plastic",
]
masses = [8.94, 4.51, 2.903, 2.982, 0.998, 0.987, 0.392]
colors = ["#8B949E", "#00E676", "#A0C0D0", "#90A0C0", "#00B4D8", "#7B61FF", "#FF6B35"]
labels = ["8.94 kg\n(baseline)", "4.51 kg\n(−49.6%)", "2.90 kg\n(−67.5%)",
          "2.98 kg\n(−66.7%)", "1.00 kg\n(−88.8%)", "0.99 kg ★\n(−88.9%)", "0.39 kg\n(−95.6%)"]

fig = go.Figure(go.Bar(
    x=scenarios,
    y=masses,
    marker_color=colors,
    text=[f"{m:.2f} kg" for m in masses],
    textposition="outside",
    textfont=dict(color="#E0E0E0", size=11),
    width=0.65,
))

# Reference lines
fig.add_hline(y=8.94, line_dash="solid", line_color="#8B949E", line_width=0.8,
              annotation_text="Original (8.94 kg)", annotation_font_color="#8B949E",
              annotation_position="top right")
fig.add_hline(y=4.51, line_dash="dot", line_color="#00E676", line_width=1.5,
              annotation_text="P3 target (4.51 kg)", annotation_font_color="#00E676",
              annotation_position="bottom right")

# Arrow annotation for best
fig.add_annotation(
    x="P4: Gen. Design<br>AlSi10Mg ★", y=0.987,
    text="★ SELECTED<br>89% reduction", showarrow=True,
    arrowhead=2, arrowcolor="#7B61FF",
    font=dict(color="#7B61FF", size=11),
    ax=80, ay=-50,
)

fig.update_layout(
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(20,30,46,0.6)",
    title=dict(text="Component mass across approaches — same load case, different strategies", font=dict(size=14)),
    yaxis=dict(title="Mass (kg)", gridcolor="#1E3A5F"),
    height=460, margin=dict(t=60, b=40, l=60, r=20),
    showlegend=False,
)
st.plotly_chart(fig, use_container_width=True)

# ── Head-to-head table ────────────────────────────────────────────────────────
st.markdown('<div class="section-hdr">⚖️ Head-to-Head: P3 (Steel) vs P4 (Best Metallic)</div>', unsafe_allow_html=True)

st.markdown("""
<table class="cmp-table">
  <tr>
    <th>Property</th>
    <th>Original Part</th>
    <th style="color:#00E676;">P3 — Topology (Steel)</th>
    <th style="color:#00D4FF;">P4 — Gen. Design (Steel)</th>
    <th style="color:#7B61FF;">P4 — Gen. Design (AlSi10Mg) ★</th>
  </tr>
  <tr>
    <td>Method</td>
    <td>—</td>
    <td>Remove from solid</td>
    <td>Generate from scratch</td>
    <td>Generate from scratch</td>
  </tr>
  <tr>
    <td>Material</td>
    <td>Steel</td>
    <td>Steel</td>
    <td>Steel</td>
    <td>Aluminium AlSi10Mg</td>
  </tr>
  <tr>
    <td>Mass</td>
    <td>8.94 kg</td>
    <td><strong>4.51 kg</strong></td>
    <td><strong>2.90 kg</strong></td>
    <td><strong>0.987 kg</strong></td>
  </tr>
  <tr>
    <td>Mass reduction</td>
    <td>—</td>
    <td><span class="best-badge">−49.6 %</span></td>
    <td><span class="best-badge">−67.5 %</span></td>
    <td><span class="best-badge">−89.0 %</span></td>
  </tr>
  <tr>
    <td>Safety Factor</td>
    <td>—</td>
    <td>≥ 4 (well above target)</td>
    <td>112.6 (massively over-designed)</td>
    <td>131.3 (massively over-designed)</td>
  </tr>
  <tr>
    <td>Max displacement</td>
    <td>—</td>
    <td>7.08 × 10⁻⁴ mm</td>
    <td>0.0007 mm</td>
    <td>0.00205 mm</td>
  </tr>
  <tr>
    <td>Max von Mises</td>
    <td>—</td>
    <td>6.587 MPa</td>
    <td>1.84 MPa</td>
    <td>1.83 MPa</td>
  </tr>
  <tr>
    <td>Starting geometry required?</td>
    <td>—</td>
    <td>Yes — full solid</td>
    <td>No</td>
    <td>No</td>
  </tr>
  <tr>
    <td>Materials explored</td>
    <td>—</td>
    <td>1 (steel only)</td>
    <td>6 simultaneously</td>
    <td>6 simultaneously</td>
  </tr>
  <tr>
    <td>Outputs generated</td>
    <td>—</td>
    <td>1 geometry</td>
    <td colspan="2">20 geometries (one per method/material combo)</td>
  </tr>
</table>
""", unsafe_allow_html=True)

st.markdown("""
<div class="callout callout-purple" style="margin-top:1rem;">
  <strong>Key insight from comparing P3 and P4 steel results:</strong> Generative design found a
  2.90 kg steel solution while topology optimization produced a 4.51 kg steel structure.
  Both satisfy the same load case with comfortable safety margins — but the generative algorithm
  explored the design space more freely and found a lighter topology.
  The massive safety factors (~100×) in P4 reveal that the 1000 N load is very light relative
  to the material's capacity — the binding constraint was geometry feasibility, not stress.
</div>
""", unsafe_allow_html=True)

# ── Radar chart top 3 scenarios ───────────────────────────────────────────────
st.markdown('<div class="section-hdr">🕸️ Multi-Metric Radar — Best Metallic Outcomes</div>', unsafe_allow_html=True)

# Normalise metrics (lower mass = better, higher SF = better, lower disp = better)
# Normalize to 0-10 scale where 10 = best
scenarios_radar = ["P3 Steel", "P4 Steel (O.6)", "P4 AlSi10Mg (O.19) ★"]
categories = ["Mass (lighter)", "Safety Factor", "Stiffness (1/disp)", "von Mises (lower)", "Recommendation"]

def norm(val, min_v, max_v, invert=False):
    if max_v == min_v:
        return 5.0
    n = (val - min_v) / (max_v - min_v) * 10
    return (10 - n) if invert else n

mass_vals  = [4.51,   2.903,  0.987]
sf_vals    = [4.0,    112.6,  131.3]
disp_vals  = [7.08e-4, 0.0007, 0.00205]
vm_vals    = [6.587,  1.84,   1.83]
rec_vals   = [80,     68.2,   89.9]  # estimated score for P3

radar_data = []
for i, name in enumerate(scenarios_radar):
    radar_data.append([
        norm(mass_vals[i],  min(mass_vals), max(mass_vals), invert=True),
        norm(sf_vals[i],    min(sf_vals),   max(sf_vals)),
        norm(1/disp_vals[i],1/max(disp_vals),1/min(disp_vals)),
        norm(vm_vals[i],    min(vm_vals),   max(vm_vals), invert=True),
        norm(rec_vals[i],   min(rec_vals),  max(rec_vals)),
    ])

radar_colors      = ["#00E676",              "#00D4FF",              "#7B61FF"]
radar_fillcolors  = ["rgba(0,230,118,0.15)", "rgba(0,212,255,0.15)", "rgba(123,97,255,0.15)"]
fig_radar = go.Figure()
for name, vals, color, fill in zip(scenarios_radar, radar_data, radar_colors, radar_fillcolors):
    fig_radar.add_trace(go.Scatterpolar(
        r=vals + [vals[0]],
        theta=categories + [categories[0]],
        fill="toself",
        name=name,
        line_color=color,
        fillcolor=fill,
        opacity=0.85,
    ))

fig_radar.update_layout(
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    polar=dict(
        bgcolor="rgba(20,30,46,0.6)",
        radialaxis=dict(visible=True, range=[0,10], gridcolor="#2E4A6B", color="#7A8FA6"),
        angularaxis=dict(gridcolor="#2E4A6B", color="#E0E0E0"),
    ),
    title=dict(text="Normalised performance (outer = better)", font=dict(size=13)),
    legend=dict(orientation="h", y=-0.15),
    height=440, margin=dict(t=60, b=60, l=60, r=60),
)
st.plotly_chart(fig_radar, use_container_width=True)

# ── Conclusion ────────────────────────────────────────────────────────────────
st.divider()
st.markdown('<div class="section-hdr">💡 Engineering Takeaways</div>', unsafe_allow_html=True)

t1, t2, t3 = st.columns(3)
with t1:
    st.markdown("""
    <div class="mtile" style="border-top: 3px solid #00E676;">
      <div style="color:#00E676;font-weight:700;margin-bottom:0.5rem;">Topology Optimization</div>
      <div style="font-size:0.85rem;color:#C0D0E0;line-height:1.6;">
        Fast and deterministic. Works with whatever material you start with.
        Best when the material is fixed and you need to reduce weight efficiently.
        Cannot explore material alternatives — that's a separate decision.
      </div>
    </div>
    """, unsafe_allow_html=True)
with t2:
    st.markdown("""
    <div class="mtile" style="border-top: 3px solid #7B61FF;">
      <div style="color:#7B61FF;font-weight:700;margin-bottom:0.5rem;">Generative Design</div>
      <div style="font-size:0.85rem;color:#C0D0E0;line-height:1.6;">
        Explores the full material and process space in one run.
        Produces candidates a human wouldn't consider. Reveals that switching
        from steel to aluminium achieves the same structural performance
        at a fraction of the weight.
      </div>
    </div>
    """, unsafe_allow_html=True)
with t3:
    st.markdown("""
    <div class="mtile" style="border-top: 3px solid #FFB347;">
      <div style="color:#FFB347;font-weight:700;margin-bottom:0.5rem;">The Real Lesson</div>
      <div style="font-size:0.85rem;color:#C0D0E0;line-height:1.6;">
        The 1000 N load under study is very light relative to either steel or aluminium.
        The dominant design driver is minimum material to connect the holes — not stress.
        Generative design found this faster because it had no starting geometry to "defend".
      </div>
    </div>
    """, unsafe_allow_html=True)

st.caption("M.Sc. Management Engineering · Fusion 360 Projects · University of Rome Tor Vergata · 2025/2026")
