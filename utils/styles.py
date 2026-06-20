GLOBAL_CSS = """
<style>
/* ── Layout ── */
.block-container { padding-top: 1.5rem !important; padding-bottom: 2rem !important; }
#MainMenu { visibility: hidden; }
footer    { visibility: hidden; }

/* ── Hero ── */
.hero {
    background: linear-gradient(135deg, #0D1B2A 0%, #1B2A3B 60%, #0F3460 100%);
    border: 1px solid #2E4A6B;
    border-radius: 16px;
    padding: 2.5rem 2rem 2rem 2rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: "";
    position: absolute; top: -40px; right: -40px;
    width: 250px; height: 250px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(0,212,255,0.07) 0%, transparent 70%);
}
.hero-title {
    font-size: 2.4rem; font-weight: 900; margin: 0 0 0.3rem 0;
    background: linear-gradient(90deg, #00D4FF 0%, #7B61FF 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    line-height: 1.15;
}
.hero-sub { font-size: 1rem; color: #9E9E9E; margin: 0 0 1rem 0; }
.hero-meta { font-size: 0.85rem; color: #7A8FA6; }

/* ── Tags ── */
.tag {
    display: inline-block; padding: 3px 10px; border-radius: 20px;
    font-size: 0.75rem; font-weight: 600; margin: 2px;
}
.tag-orange { background: rgba(255,107,53,0.15); color: #FF6B35; border: 1px solid rgba(255,107,53,0.4); }
.tag-cyan   { background: rgba(0,212,255,0.15);  color: #00D4FF; border: 1px solid rgba(0,212,255,0.4); }
.tag-green  { background: rgba(0,230,118,0.15);  color: #00E676; border: 1px solid rgba(0,230,118,0.4); }
.tag-purple { background: rgba(123,97,255,0.15); color: #7B61FF; border: 1px solid rgba(123,97,255,0.4); }
.tag-gray   { background: rgba(150,150,150,0.15);color: #B0B0B0; border: 1px solid rgba(150,150,150,0.4); }

/* ── Project cards (home) ── */
.pcard {
    background: linear-gradient(135deg, #141E2E 0%, #0D1520 100%);
    border-radius: 14px; padding: 1.6rem 1.4rem;
    border: 1px solid #1E3A5F; height: 100%;
    transition: border-color 0.2s, transform 0.2s;
    position: relative; overflow: hidden;
}
.pcard:hover { border-color: #00D4FF; transform: translateY(-2px); }
.pcard-num {
    font-size: 3.5rem; font-weight: 900; opacity: 0.07;
    position: absolute; top: 8px; right: 16px; line-height: 1;
}
.pcard-title { font-size: 1.15rem; font-weight: 700; margin: 0 0 0.3rem 0; }
.pcard-desc  { font-size: 0.82rem; color: #9E9E9E; margin: 0 0 1rem 0; line-height: 1.5; }
.pcard-stat  { font-size: 1.6rem; font-weight: 800; }
.pcard-stat-label { font-size: 0.72rem; color: #7A8FA6; letter-spacing: 0.05em; text-transform: uppercase; }

/* ── Section header ── */
.section-hdr {
    border-left: 4px solid #00D4FF;
    padding-left: 0.75rem;
    margin: 2rem 0 1rem 0;
    font-size: 1.2rem; font-weight: 700;
}
.section-hdr-orange { border-left-color: #FF6B35; }
.section-hdr-green  { border-left-color: #00E676; }
.section-hdr-purple { border-left-color: #7B61FF; }

/* ── Metric tile ── */
.mtile {
    background: #141E2E; border-radius: 10px;
    padding: 1rem 1.2rem;
    border: 1px solid #1E3A5F;
}
.mtile-val   { font-size: 1.6rem; font-weight: 800; }
.mtile-label { font-size: 0.72rem; color: #7A8FA6; text-transform: uppercase; letter-spacing: 0.06em; }

/* ── Comparison table ── */
.cmp-table { width: 100%; border-collapse: collapse; font-size: 0.88rem; }
.cmp-table th { background: #1B2A3B; color: #7A8FA6; padding: 8px 14px; text-align: left;
                text-transform: uppercase; letter-spacing: 0.06em; font-size: 0.72rem;
                border-bottom: 2px solid #2E4A6B; }
.cmp-table td { padding: 8px 14px; border-bottom: 1px solid #1E3A5F; vertical-align: middle; }
.cmp-table tr:hover td { background: rgba(0,212,255,0.04); }

/* ── Best badge ── */
.best-badge {
    display: inline-block; padding: 2px 8px; border-radius: 12px;
    font-size: 0.68rem; font-weight: 700; background: rgba(0,230,118,0.15);
    color: #00E676; border: 1px solid rgba(0,230,118,0.4);
}

/* ── Info callout ── */
.callout {
    border-left: 3px solid #00D4FF;
    background: rgba(0,212,255,0.06);
    border-radius: 0 8px 8px 0;
    padding: 0.8rem 1rem;
    margin: 1rem 0;
    font-size: 0.88rem;
    color: #C0D0E0;
}
.callout-orange { border-left-color: #FF6B35; background: rgba(255,107,53,0.06); }
.callout-green  { border-left-color: #00E676; background: rgba(0,230,118,0.06); }
.callout-purple { border-left-color: #7B61FF; background: rgba(123,97,255,0.06); }
</style>
"""

def inject(extra=""):
    import streamlit as st
    st.markdown(GLOBAL_CSS + extra, unsafe_allow_html=True)
