import streamlit as st
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from utils.styles import inject

st.set_page_config(
    page_title="Fusion 360 Engineering Portfolio",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject()

# ── Hero ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <p class="hero-meta">⚙️ AUTODESK FUSION 360 · MANAGEMENT OF INNOVATION AND TECHNOLOGY</p>
  <h1 class="hero-title">Engineering Portfolio</h1>
  <p class="hero-sub">University of Rome "Tor Vergata" &nbsp;·&nbsp; Prof. Daniele Almonti &nbsp;·&nbsp; AY 2025/2026</p>
  <div>
    <span class="tag tag-cyan">Danial Mahmoody — 0384253</span>
    <span class="tag tag-cyan">Kuhyar Saeedi — 0384251</span>
    <span class="tag tag-cyan">Nima Shahrokhi — 0384377</span>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Global stats bar ─────────────────────────────────────────────────────────
st.markdown("### At a Glance")
c1, c2, c3, c4, c5 = st.columns(5)
with c1:
    st.metric("Projects", "4", help="Complete Fusion 360 projects")
with c2:
    st.metric("Simulations", "18", help="Injection molding parametric studies")
with c3:
    st.metric("Mass Reduction", "−49.6 %", help="Shape optimization result (Project 3)")
with c4:
    st.metric("Gen. Design Outcomes", "20", help="Outcomes generated in Project 4")
with c5:
    st.metric("Best Deflection", "0.062 mm", help="Lowest out-of-plane deflection (Study 9)")

st.divider()

# ── Project cards ────────────────────────────────────────────────────────────
st.markdown("### Projects — Select one to explore")

col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown("""
    <div class="pcard" style="border-top: 3px solid #FF6B35;">
      <div class="pcard-num" style="color:#FF6B35;">1</div>
      <div style="margin-bottom:0.5rem;">
        <span class="tag tag-orange">Sand Casting</span>
        <span class="tag tag-gray">FeG 520 Steel</span>
      </div>
      <p class="pcard-title" style="color:#FF6B35;">🏭 Foundry Design</p>
      <p class="pcard-desc">
        Complete sand-casting process design for a three-port junction housing —
        coring analysis, draft angles, thermal moduli, riser sizing, gating system,
        and metallostatic verification.
      </p>
      <div class="pcard-stat" style="color:#FF6B35;">4.06 s</div>
      <div class="pcard-stat-label">Pouring Time &nbsp;·&nbsp; 31 pages</div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Explore Project 1 →", key="p1", use_container_width=True):
        st.switch_page("pages/1_Sand_Casting.py")

with col2:
    st.markdown("""
    <div class="pcard" style="border-top: 3px solid #00D4FF;">
      <div class="pcard-num" style="color:#00D4FF;">2</div>
      <div style="margin-bottom:0.5rem;">
        <span class="tag tag-cyan">Injection Molding</span>
        <span class="tag tag-gray">PP · ABS</span>
        <span class="tag tag-cyan">★ Special</span>
      </div>
      <p class="pcard-title" style="color:#00D4FF;">💉 Simulation & Optimization</p>
      <p class="pcard-desc">
        18 parametric injection molding simulations on a Remote Control Housing —
        8 experimental phases exploring gate count, melt & mold temperature.
        PP vs ABS material comparison with interactive charts.
      </p>
      <div class="pcard-stat" style="color:#00D4FF;">18 studies</div>
      <div class="pcard-stat-label">Best deflection: 0.062 mm (Study 9) &nbsp;·&nbsp; 21 pages + data</div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Explore Project 2 → (Special)", key="p2", use_container_width=True):
        st.switch_page("pages/2_Injection_Molding.py")

col3, col4 = st.columns(2, gap="large")

with col3:
    st.markdown("""
    <div class="pcard" style="border-top: 3px solid #00E676;">
      <div class="pcard-num" style="color:#00E676;">3</div>
      <div style="margin-bottom:0.5rem;">
        <span class="tag tag-green">Shape Optimization</span>
        <span class="tag tag-gray">Steel → ABS Print</span>
      </div>
      <p class="pcard-title" style="color:#00E676;">⚡ Topology Optimization</p>
      <p class="pcard-desc">
        Topology-driven weight reduction of a steel plate: shape optimization,
        mesh reconstruction, static structural validation and additive
        manufacturing preparation on the Prusa XL.
      </p>
      <div class="pcard-stat" style="color:#00E676;">−49.6 %</div>
      <div class="pcard-stat-label">Mass reduction · 8.94 kg → 4.51 kg &nbsp;·&nbsp; 30 pages</div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Explore Project 3 →", key="p3", use_container_width=True):
        st.switch_page("pages/3_Shape_Optimization.py")

with col4:
    st.markdown("""
    <div class="pcard" style="border-top: 3px solid #7B61FF;">
      <div class="pcard-num" style="color:#7B61FF;">4</div>
      <div style="margin-bottom:0.5rem;">
        <span class="tag tag-purple">Generative Design</span>
        <span class="tag tag-gray">Al · Steel · ABS</span>
      </div>
      <p class="pcard-title" style="color:#7B61FF;">🤖 AI-Driven Generative Design</p>
      <p class="pcard-desc">
        Same load case as Project 3 — but inverted. 20 AI-generated outcomes
        across 5 manufacturing methods and 6 materials. Selected best:
        AlSi10Mg, unrestricted, 0.987 kg — a 89% reduction from original.
      </p>
      <div class="pcard-stat" style="color:#7B61FF;">20 outcomes</div>
      <div class="pcard-stat-label">Selected: 0.987 kg AlSi10Mg &nbsp;·&nbsp; 15 pages</div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Explore Project 4 →", key="p4", use_container_width=True):
        st.switch_page("pages/4_Generative_Design.py")

st.divider()

# ── Bonus comparison teaser ───────────────────────────────────────────────────
st.markdown("""
<div class="callout-green callout">
  <strong>🔥 Hidden insight:</strong> Projects 3 &amp; 4 solve the <em>exact same problem</em> —
  same component, same 4 × 1000 N load — using two different philosophies.
  Topology optimization (P3) kept steel and reduced mass by 49.6 %.
  Generative design (P4) explored materials and found an aluminium solution at 0.987 kg — <strong>89 % lighter than the original</strong>.
  See the head-to-head on the <b>⚖️ Comparison</b> page.
</div>
""", unsafe_allow_html=True)

if st.button("⚖️ Go to P3 vs P4 Comparison →", key="cmp", use_container_width=False):
    st.switch_page("pages/5_Comparison.py")

st.divider()
st.caption("M.Sc. Management Engineering · Fusion 360 Projects · University of Rome Tor Vergata · 2025/2026")
