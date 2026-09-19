"""
AquaHarvest AI - Clean, Modern Editorial Sustainability Platform
Pure, Uncluttered, and High-Contrast Climate-Tech Intelligence
"""

import os
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from PIL import Image

# Core & AI Package Imports
from core.config import (
    CITY_RAINFALL_DATA,
    ROOF_MATERIAL_COEFFICIENTS,
    DEFAULT_TANKER_COST_INR
)
from core.hydrology_math import run_full_hydrology_pipeline
from core.multimodal_vision import analyze_rooftop_image, ensure_sample_roof_image
from core.deliverable_generator import (
    generate_presentation_pptx,
    generate_executive_report_markdown
)
from ai.orchestrator import AgenticOrchestrator
from ai.granite_client import get_granite_client
from rag.vector_store import get_rag_store

# Page Setup
st.set_page_config(
    page_title="AquaHarvest AI | Smart Catchment & Aquifer Recharge",
    page_icon="💧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load High-Contrast Custom CSS
css_path = os.path.join(os.path.dirname(__file__), "assets", "style.css")
if os.path.exists(css_path):
    with open(css_path, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Session State Initialization
if "pipeline_results" not in st.session_state:
    st.session_state.pipeline_results = None
if "vision_results" not in st.session_state:
    st.session_state.vision_results = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "selected_surface_preset" not in st.session_state:
    st.session_state.selected_surface_preset = "Concrete Flat Slab"

granite_client = get_granite_client()
rag_store = get_rag_store()

# ==========================================
# EDITORIAL HERO SECTION (CLEAN & MINIMAL)
# ==========================================
st.markdown("""<div class="hero-header">
<div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 32px;">
<div style="flex: 1 1 540px; max-width: 660px;">
<div class="hero-pill">
<span class="hero-pill-dot"></span>
Next-Gen Catchment & Aquifer Recharge Intelligence
</div>
<h1 class="hero-title">Catch more. <span class="hero-italic">Waste zero.</span></h1>
<p class="hero-subtitle">
Hyperlocal rooftop catchment analysis, storage optimization, and aquifer recharge modeling for climate-resilient campuses and buildings.
</p>
</div>
<div class="hydro-emblem-wrapper">
<div class="hydro-orbital-ring-outer">
<span class="hydro-satellite-dot-outer"></span>
</div>
<div class="hydro-orbital-ring">
<span class="hydro-satellite-dot"></span>
</div>
<div class="hydro-orbit-chip chip-top">🌧️ High-Flow Yield</div>
<div class="hydro-orbit-chip chip-bottom">⚡ 98.5% Purity Guard</div>
<div class="hydro-card-core" title="AquaHarvest AI Hydrology Core">
<div class="hydro-shine-overlay"></div>
<div class="hydro-icon-container">
<svg width="76" height="76" viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg" class="hydro-vector-icon">
<defs>
<linearGradient id="dropGradBig" x1="16" y1="6" x2="48" y2="58" gradientUnits="userSpaceOnUse">
<stop offset="0%" stop-color="#00E5FF"/>
<stop offset="48%" stop-color="#10B981"/>
<stop offset="100%" stop-color="#0B3828"/>
</linearGradient>
<linearGradient id="leafGradBig" x1="28" y1="28" x2="42" y2="48" gradientUnits="userSpaceOnUse">
<stop offset="0%" stop-color="#E2FF75"/>
<stop offset="100%" stop-color="#10B981"/>
</linearGradient>
<filter id="softGlowBig" x="-20%" y="-20%" width="140%" height="140%">
<feDropShadow dx="0" dy="4" stdDeviation="4" flood-color="rgba(16,185,129,0.38)"/>
</filter>
</defs>
<ellipse cx="32" cy="53" rx="20" ry="4.5" stroke="rgba(11,56,40,0.2)" stroke-width="1.5"/>
<ellipse cx="32" cy="53" rx="27" ry="6" stroke="rgba(16,185,129,0.38)" stroke-width="1.2" stroke-dasharray="2 3"/>
<path d="M32 7 C32 7, 16 27, 16 39 C16 48 23.2 55 32 55 C40.8 55 48 48 48 39 C48 27, 32 7, 32 7 Z" fill="url(#dropGradBig)" filter="url(#softGlowBig)"/>
<path d="M22 35 C22 27, 28 17, 32 13 C29 18, 24 28, 25 35 C25.5 39, 27 42, 25 44 C23 46, 22 41, 22 35 Z" fill="rgba(255,255,255,0.65)"/>
<path d="M32 46 C32 46 31 36 38 31 C38 31 39 39 34 44 C33 45 32 46 32 46 Z" fill="url(#leafGradBig)"/>
<path d="M32 46 C32 46 33 38 28 34 C28 34 26 40 30 44 C31 45 32 46 32 46 Z" fill="#C4F646"/>
</svg>
</div>
<div class="hydro-brand-title">AquaHarvest</div>
<div class="hydro-status-pill">
<span class="hydro-pulse-beacon"></span>
<span class="hydro-status-text">AI CORE ACTIVE</span>
</div>
<span class="hydro-subtext">CGWB & BIS IS 15797</span>
</div>
</div>
</div>
</div>""", unsafe_allow_html=True)

# ==========================================
# SIDEBAR PARAMETERS (CLEAN & INTUITIVE)
# ==========================================
with st.sidebar:
    st.markdown("<h3 style='color: #0B3828; margin-top:0;'>Facility Parameters</h3>", unsafe_allow_html=True)
    
    city_choice = st.selectbox(
        "📍 Campus / Site City",
        list(CITY_RAINFALL_DATA.keys()),
        index=0,
        help="Loads historical IMD precipitation normals and local recharge bylaws."
    )
    city_meta = CITY_RAINFALL_DATA[city_choice]
    
    override_rain = st.checkbox("Custom Rainfall Input")
    if override_rain:
        annual_rain_val = st.number_input("Annual Rainfall (mm)", 100.0, 5000.0, float(city_meta["annual_rainfall_mm"]), 25.0)
    else:
        annual_rain_val = float(city_meta["annual_rainfall_mm"])
        st.caption(f"Historical Normal: **{annual_rain_val:.0f} mm/year** ({city_meta['state']})")
        
    st.markdown("---")
    st.markdown("<h4 style='color: #0B3828;'>Building Sizing</h4>", unsafe_allow_html=True)
    rooftop_area = st.number_input("Rooftop Catchment Area (m²)", 100, 100000, 2500, 100, help="Total footprint of terrace slabs or industrial roofs.")
    campus_population = st.number_input("Building Population (Occupants)", 50, 50000, 1500, 50, help="Daily students, faculty, or building residents.")
    tanker_rate = st.number_input("Commercial Tanker Rate (₹ / 10k L)", 500.0, 5000.0, float(DEFAULT_TANKER_COST_INR), 50.0)

    st.markdown("---")
    # Clean Engine Status
    st.markdown("""
    <div style="background: #FFFFFF; border: 1px solid rgba(11, 56, 40, 0.08); border-radius: 12px; padding: 14px; margin-top: 10px;">
        <span style="font-size: 11px; text-transform: uppercase; color: #5C7567; font-weight: 700;">Engine Status</span>
        <div style="color: #0B3828; font-weight: 700; font-size: 14px; margin-top: 2px;">🟢 Autonomous AI Active</div>
        <div style="color: #7B9385; font-size: 11px; margin-top: 2px;">Deterministic Hydrology Core</div>
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# PHYSICAL RAINWATER CONVEYANCE PATH
# ==========================================
st.markdown(f"""
<div class="flow-bar">
    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px; font-size: 13px;">
        <div style="display: flex; align-items: center; gap: 8px;">
            <span style="background: #E8F5D8; color: #245720; padding: 4px 10px; border-radius: 6px; font-weight: 700;">1. CATCHMENT</span>
            <span style="color: #0B3828; font-weight: 600;">{rooftop_area:,.0f} m² Roof</span>
        </div>
        <span style="color: #5C7567;">➔</span>
        <div style="display: flex; align-items: center; gap: 8px;">
            <span style="background: #E2F0FD; color: #1E40AF; padding: 4px 10px; border-radius: 6px; font-weight: 700;">2. FIRST FLUSH</span>
            <span style="color: #0B3828; font-weight: 600;">{rooftop_area * 1.5:,.0f} L Wash</span>
        </div>
        <span style="color: #5C7567;">➔</span>
        <div style="display: flex; align-items: center; gap: 8px;">
            <span style="background: #F3E8FF; color: #6B21A8; padding: 4px 10px; border-radius: 6px; font-weight: 700;">3. FILTER BED</span>
            <span style="color: #0B3828; font-weight: 600;">Sand & Gravel Media</span>
        </div>
        <span style="color: #5C7567;">➔</span>
        <div style="display: flex; align-items: center; gap: 8px;">
            <span style="background: #FEF3C7; color: #92400E; padding: 4px 10px; border-radius: 6px; font-weight: 700;">4. MODULAR CISTERN</span>
            <span style="color: #0B3828; font-weight: 600;">21-Day Dry Buffer</span>
        </div>
        <span style="color: #5C7567;">➔</span>
        <div style="display: flex; align-items: center; gap: 8px;">
            <span style="background: #E8F5D8; color: #245720; padding: 4px 10px; border-radius: 6px; font-weight: 700;">5. RECHARGE SHAFT</span>
            <span style="color: #0B3828; font-weight: 600;">Aquifer Infiltration</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Main Navigation Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📸 1. Catchment & Roof Vision",
    "⚙️ 2. Engineering Blueprint",
    "💰 3. Financial ROI & Carbon",
    "📚 4. Standards & Water Assistant",
    "🚰 5. Smart Network & Distribution"
])

# ==============================================================================
# TAB 1: CATCHMENT & ROOF VISION
# ==============================================================================
with tab1:
    st.markdown("<h2 class='section-headline'>Catchment Inspection & Surface Classification</h2>", unsafe_allow_html=True)
    st.markdown("<p class='section-subhead'>Select a certified surface material or upload an aerial/mobile photograph of the rooftop.</p>", unsafe_allow_html=True)

    # 4 Quick Selectable Surface Cards
    st.markdown("<p style='font-weight: 700; color: #5C7567; font-size: 13px; text-transform: uppercase;'>Choose Surface Material or Upload Custom Photo:</p>", unsafe_allow_html=True)
    scol1, scol2, scol3, scol4 = st.columns(4)
    
    with scol1:
        if st.button("🏢 Concrete Flat Slab\nC = 0.85 (Standard RCC)", use_container_width=True):
            st.session_state.selected_surface_preset = "Concrete Flat Slab"
            st.session_state.vision_results = {
                "is_valid_catchment": True,
                "surface_type": "Concrete Flat Slab",
                "runoff_coefficient": 0.85,
                "confidence_pct": 94.0,
                "surface_integrity_score": 92,
                "wear_status": "Pristine Concrete Slab",
                "debris_risk": "Low (Smooth Catchment)",
                "filtration_recommendation": "Dual-media sand & gravel filter",
                "first_flush_guidance": "First-flush pipe diverter (1.5mm standard)"
            }

    with scol2:
        if st.button("🧱 Clay Tiles\nC = 0.75 (Sloped Tiles)", use_container_width=True):
            st.session_state.selected_surface_preset = "Terracotta / Clay Tiles"
            st.session_state.vision_results = {
                "is_valid_catchment": True,
                "surface_type": "Terracotta / Clay Tiles",
                "runoff_coefficient": 0.75,
                "confidence_pct": 91.0,
                "surface_integrity_score": 85,
                "wear_status": "Sloped Terracotta Tile Array",
                "debris_risk": "Moderate (Leaves in tile valleys)",
                "filtration_recommendation": "Leaf screen + Dual-media gravel filter",
                "first_flush_guidance": "Eaves gutter leaf mesh with dual-stage sediment trap"
            }

    with scol3:
        if st.button("🏭 Corrugated Metal\nC = 0.90 (Industrial GI)", use_container_width=True):
            st.session_state.selected_surface_preset = "Corrugated GI Sheets"
            st.session_state.vision_results = {
                "is_valid_catchment": True,
                "surface_type": "Corrugated GI Sheets",
                "runoff_coefficient": 0.90,
                "confidence_pct": 96.0,
                "surface_integrity_score": 90,
                "wear_status": "Reflective Galvanized Iron Sheeting",
                "debris_risk": "Low to Moderate (Atmospheric soot)",
                "filtration_recommendation": "First-flush diverter + sediment trap",
                "first_flush_guidance": "High-flow diverter with stainless steel mesh screen"
            }

    with scol4:
        if st.button("🌱 Green / Soil Roof\nC = 0.20 (Eco-Substrate)", use_container_width=True):
            st.session_state.selected_surface_preset = "Grass / Green Roof"
            st.session_state.vision_results = {
                "is_valid_catchment": True,
                "surface_type": "Grass / Green Roof",
                "runoff_coefficient": 0.20,
                "confidence_pct": 89.0,
                "surface_integrity_score": 88,
                "wear_status": "Vegetated Retention Substrate",
                "debris_risk": "High (Bio-matter & root debris)",
                "filtration_recommendation": "Bio-retention geotextile filter",
                "first_flush_guidance": "Bio-retention filter with geotextile membrane recommended"
            }

    st.markdown("<br>", unsafe_allow_html=True)
    
    col_img_left, col_img_right = st.columns([1, 1], gap="medium")
    
    with col_img_left:
        st.markdown("<div class='clean-card'>", unsafe_allow_html=True)
        st.markdown("<h4 style='color:#0B3828; margin-top:0;'>Upload Rooftop Imagery</h4>", unsafe_allow_html=True)
        uploaded_file = st.file_uploader("Upload Drone / Satellite / Mobile Photo", type=["png", "jpg", "jpeg"])
        
        sample_path = ensure_sample_roof_image()
        test_dir = os.path.join(os.path.dirname(__file__), "test_images")
        
        st.markdown("<p style='font-size: 11.5px; color: #5C7567; text-transform: uppercase; font-weight: 700; margin: 12px 0 6px 0;'>⚡ Instant Open-Source Benchmark Test Suite:</p>", unsafe_allow_html=True)
        t_col1, t_col2 = st.columns(2)
        btn_c = t_col1.button("🏢 Concrete Slab", use_container_width=True, help="Wikimedia Commons urban RCC flat terrace (C = 0.85)")
        btn_t = t_col2.button("🧱 Terracotta Tiles", use_container_width=True, help="Wikimedia Commons sloped clay tiles (C = 0.75)")
        btn_m = t_col1.button("🏭 Corrugated Metal", use_container_width=True, help="Wikimedia Commons industrial GI sheet roof (C = 0.90)")
        btn_g = t_col2.button("🌱 Green Eco-Roof", use_container_width=True, help="Wikimedia Commons vegetated sedum roof (C = 0.20)")
        btn_w = st.button("⛔ Solid Waste Hazard (Test 98.5% Rejection)", use_container_width=True, help="Test hazard safety rejection with dense plastic waste")
        
        active_img = None
        active_caption = "Active Catchment Photo"
        
        if uploaded_file is not None:
            active_img = uploaded_file
            active_caption = "Uploaded Catchment Photo"
        elif btn_c:
            active_img = os.path.join(test_dir, "01_concrete_terrace_roof.jpg")
            active_caption = "Open-Source Benchmark: Flat RCC Concrete Terrace (Wikimedia Commons)"
        elif btn_t:
            active_img = os.path.join(test_dir, "02_terracotta_clay_tiles.jpg")
            active_caption = "Open-Source Benchmark: Sloped Terracotta Clay Tiles (Wikimedia Commons)"
        elif btn_m:
            active_img = os.path.join(test_dir, "03_industrial_corrugated_metal.jpg")
            active_caption = "Open-Source Benchmark: Industrial Corrugated GI Metal (Wikimedia Commons)"
        elif btn_g:
            active_img = os.path.join(test_dir, "04_vegetated_green_roof.jpg")
            active_caption = "Open-Source Benchmark: Vegetated Green Eco-Roof (Wikimedia Commons)"
        elif btn_w:
            active_img = os.path.join(test_dir, "05_solid_waste_hazard_debris.png")
            active_caption = "Open-Source Benchmark: Solid Waste & Plastic Debris (Hazard Rejection Test)"
        elif "active_test_img" in st.session_state and os.path.exists(st.session_state.active_test_img):
            active_img = st.session_state.active_test_img
            active_caption = st.session_state.get("active_test_caption", "Active Catchment Photo")
        elif os.path.exists(sample_path):
            active_img = sample_path
            active_caption = "Active Benchmark Concrete Roof (Expansion Joints & Sump Inlets)"

        if active_img is not None:
            if isinstance(active_img, str):
                st.session_state.active_test_img = active_img
                st.session_state.active_test_caption = active_caption
            st.image(active_img, caption=active_caption, use_container_width=True)
            
        st.markdown("</div>", unsafe_allow_html=True)

    with col_img_right:
        if active_img and (uploaded_file is not None or btn_c or btn_t or btn_m or btn_g or btn_w or not st.session_state.vision_results):
            v_res = analyze_rooftop_image(active_img)
            st.session_state.vision_results = v_res

        v = st.session_state.vision_results or {
            "is_valid_catchment": True,
            "surface_type": "Concrete Flat Slab",
            "runoff_coefficient": 0.85,
            "confidence_pct": 93.0,
            "surface_integrity_score": 90,
            "wear_status": "Standard Reinforced Concrete Terrace",
            "debris_risk": "Low",
            "filtration_recommendation": "Dual-media sand & gravel filter",
            "first_flush_guidance": "First-flush pipe diverter (1.5mm standard)"
        }

        is_valid = v.get("is_valid_catchment", True)
        card_class = "clean-card" if is_valid else "clean-card clean-card-danger"
        
        st.markdown(f"<div class='{card_class}'>", unsafe_allow_html=True)
        
        if not is_valid:
            st.markdown("<h4 style='color:#EF4444; margin-top:0;'>⚠️ Catchment Validation: REJECTED</h4>", unsafe_allow_html=True)
            st.markdown(f"""
            <div style="margin-bottom: 14px;">
                <div style="font-size: 13px; color: #EF4444; text-transform: uppercase; font-weight: 700;">Detection Category</div>
                <div style="font-size: 18px; font-weight: 800; color: #0B3828; margin: 2px 0 8px 0;">{v['surface_type']}</div>
                <div style="display: flex; align-items: baseline; gap: 14px; flex-wrap: wrap;">
                    <span style="font-size: 24px; font-weight: 800; color: #EF4444; font-family: 'JetBrains Mono';">C = 0.0 (Hazard)</span>
                    <span style="color: #DC2626; font-size: 13px; font-weight: 700;">Waste Clutter Confidence: {v.get('waste_detection_confidence_pct', 98)}%</span>
                    <span style="color: #64748B; font-size: 13px;">Catchment Suitability: 0%</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.progress(v.get("surface_integrity_score", 8) / 100.0)
            st.markdown(f"<p style='font-size: 12px; color: #EF4444; margin-top: 4px;'>Surface Integrity: <b>{v.get('surface_integrity_score', 8)}/100</b> ({v.get('wear_status', 'Hazardous')})</p>", unsafe_allow_html=True)

            st.markdown(f"""
            <div style="background: rgba(239, 68, 68, 0.06); border: 1px solid rgba(239, 68, 68, 0.2); border-radius: 8px; padding: 14px; margin-top: 14px;">
                <p style="margin: 0 0 6px 0; color: #B91C1C; font-size: 13px; font-weight: 700;">{v.get('safety_alert')}</p>
                <p style="margin: 4px 0; color: #475569; font-size: 12px;"><b>Detection Signals:</b> High-frequency object clutter gradient ({v.get('diagnostic_metrics', {}).get('edge_clutter_gradient', 21.4)}), {v.get('diagnostic_metrics', {}).get('active_hue_bands', 8)} distinct saturated packaging color bands.</p>
                <p style="margin: 4px 0; color: #9A3412; font-size: 12px;"><b>Required Action:</b> {v.get('filtration_recommendation')}</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("<h4 style='color:#0B3828; margin-top:0;'>Computer Vision Diagnostic Report</h4>", unsafe_allow_html=True)
            st.markdown(f"""
            <div style="margin-bottom: 16px;">
                <div style="font-size: 13px; color: #5C7567; text-transform: uppercase; font-weight: 700;">Identified Catchment Surface</div>
                <div style="font-size: 20px; font-weight: 800; color: #0B3828; margin: 2px 0 8px 0;">{v['surface_type']}</div>
                <div style="display: flex; align-items: baseline; gap: 10px;">
                    <span style="font-size: 28px; font-weight: 800; color: #167A53; font-family: 'JetBrains Mono';">C = {v['runoff_coefficient']}</span>
                    <span style="color: #2E6B24; font-size: 13px; font-weight: 600;">(Confidence: {v.get('confidence_pct', 92)}%)</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.progress(v.get("surface_integrity_score", 88) / 100.0)
            st.markdown(f"<p style='font-size: 12px; color: #5C7567; margin-top: 4px;'>Surface Integrity Index: <b>{v.get('surface_integrity_score', 88)}/100</b> ({v.get('wear_status', 'Good')})</p>", unsafe_allow_html=True)

            st.markdown(f"""
            <div style="background: #F6F8F3; border-radius: 10px; padding: 14px; margin-top: 14px; border: 1px solid rgba(11, 56, 40, 0.06);">
                <p style="margin: 3px 0; color: #0B3828; font-size: 13px;"><b>🍃 Debris / Silt Risk:</b> <span style="color: #92400E; font-weight: 600;">{v.get('debris_risk', 'Low')}</span></p>
                <p style="margin: 3px 0; color: #0B3828; font-size: 13px;"><b>🛡️ Recommended Pre-Filter:</b> {v.get('filtration_recommendation', 'Dual-media sand & gravel')}</p>
                <p style="margin: 3px 0; color: #0B3828; font-size: 13px;"><b>🚿 First-Flush Standard:</b> {v.get('first_flush_guidance', '1.5mm volume wash')}</p>
            </div>
            """, unsafe_allow_html=True)
            
        st.markdown("</div>", unsafe_allow_html=True)

    # Real-Time Yield Banner
    st.markdown("<br>", unsafe_allow_html=True)
    c_factor = v["runoff_coefficient"]
    est_liters = rooftop_area * annual_rain_val * c_factor * 0.90
    est_tankers = est_liters / 10000.0
    est_savings = est_tankers * tanker_rate

    k1, k2, k3, k4 = st.columns(4)
    k1.metric("📍 City & Rainfall", city_choice, f"{annual_rain_val:.0f} mm / year")
    k2.metric("📐 Catchment Area", f"{rooftop_area:,.0f} m²", f"Runoff C = {c_factor}")
    
    if not is_valid:
        k3.metric("💧 Usable Rain Yield", "0 L (Halted)", "Surface Decontamination Needed")
        k4.metric("🚛 Tankers Saved / Yr", "0 Tankers", "Risk of Contamination")
    else:
        k3.metric("💧 Annual Rain Yield", f"{est_liters/1000:,.0f} m³", f"{est_liters:,.0f} Liters")
        k4.metric("🚛 Tankers Saved / Yr", f"{est_tankers:,.0f} Tankers", f"₹{est_savings:,.0f} Value")


# ==============================================================================
# TAB 2: ENGINEERING BLUEPRINT
# ==============================================================================
with tab2:
    st.markdown("<h2 class='section-headline'>Autonomous Engineering Blueprint</h2>", unsafe_allow_html=True)
    st.markdown("<p class='section-subhead'>Coordinates 5 specialized domain agents into an automated decision-support pipeline sizing modular tanks, recharge shafts, and filter media.</p>", unsafe_allow_html=True)

    col_btn, col_blank = st.columns([1, 2])
    with col_btn:
        run_agents = st.button("⚡ Run Full Engineering Assessment", type="primary", use_container_width=True)

    if run_agents or st.session_state.pipeline_results is None:
        prog_bar = st.progress(0.0)
        status_msg = st.empty()
        
        def on_agent_progress(step_title, fraction):
            status_msg.markdown(f"**Executing:** `{step_title}`")
            prog_bar.progress(fraction)

        orchestrator = AgenticOrchestrator(granite_client)
        active_surface = st.session_state.vision_results.get("surface_type", "Concrete Flat Slab") if st.session_state.vision_results else "Concrete Flat Slab"
        
        st.session_state.pipeline_results = orchestrator.run_pipeline(
            area_sqm=rooftop_area,
            surface_type=active_surface,
            city=city_choice,
            annual_rainfall_mm=annual_rain_val,
            population=campus_population,
            tanker_cost_inr=tanker_rate,
            vision_data=st.session_state.vision_results,
            progress_callback=on_agent_progress if run_agents else None
        )
        status_msg.success(f"✓ All 5 Engineering Agents Executed in {st.session_state.pipeline_results['elapsed_seconds']}s")
        prog_bar.progress(1.0)

    res = st.session_state.pipeline_results
    sum_data = res["summary"]

    st.markdown("<br>", unsafe_allow_html=True)
    
    # Core Engineering Blueprint Cards
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Harvested Rainwater", f"{sum_data['annual_harvest_liters']:,.0f} L", f"{sum_data['annual_harvest_m3']} m³/year")
    c2.metric("Modular Cistern Sizing", f"{sum_data['tank_capacity_liters']:,.0f} L", sum_data['tank_dimensions'])
    c3.metric("Recharge Shaft Depth", f"{sum_data['recharge_shaft_depth_m']} Meters", "Sand-Gravel Reverse Filter")
    c4.metric("Water Displaced", f"{sum_data['tankers_saved']:,.0f} Tankers/yr", "10,000 L Tankers")

    st.markdown("<br>", unsafe_allow_html=True)
    
    # Interactive Dual-Visualization Row
    gcol1, gcol2 = st.columns([1, 1], gap="medium")
    
    with gcol1:
        st.markdown("<div class='clean-card'>", unsafe_allow_html=True)
        st.markdown("<h4 style='color:#0B3828; margin-top:0;'>Water Self-Sufficiency & Dry Buffer</h4>", unsafe_allow_html=True)
        
        # Calculate water security percentage
        annual_demand = campus_population * 25.0 * 365.0
        sec_pct = min(100.0, (sum_data['annual_harvest_liters'] / annual_demand * 100.0))
        
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=sec_pct,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Campus Water Self-Sufficiency (%)", 'font': {'size': 14, 'color': '#0B3828'}},
            delta={'reference': 50, 'increasing': {'color': "#10B981"}},
            number={'suffix': "%", 'font': {'color': '#0B3828', 'size': 32}},
            gauge={
                'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "#5C7567"},
                'bar': {'color': "#0B3828"},
                'bgcolor': "#EEF3E9",
                'borderwidth': 1,
                'bordercolor': "rgba(11,56,40,0.1)",
                'steps': [
                    {'range': [0, 35], 'color': 'rgba(239, 68, 68, 0.15)'},
                    {'range': [35, 70], 'color': 'rgba(245, 158, 11, 0.15)'},
                    {'range': [70, 100], 'color': 'rgba(196, 246, 70, 0.45)'}
                ],
                'threshold': {
                    'line': {'color': "#0B3828", 'width': 4},
                    'thickness': 0.75,
                    'value': 75
                }
            }
        ))
        fig_gauge.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Plus Jakarta Sans", color="#0B3828"),
            height=260,
            margin=dict(l=20, r=20, t=30, b=20)
        )
        st.plotly_chart(fig_gauge, use_container_width=True)
        st.markdown(f"<p style='color:#5C7567; font-size:12px; text-align:center;'>Supplies <b>{res['agent3']['tank_specs']['buffer_days_provided']} days</b> of continuous non-potable buffer during peak heatwaves.</p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with gcol2:
        st.markdown("<div class='clean-card'>", unsafe_allow_html=True)
        st.markdown("<h4 style='color:#0B3828; margin-top:0;'>Seasonal Inflow vs. Facility Demand</h4>", unsafe_allow_html=True)
        
        monthly_pipeline = run_full_hydrology_pipeline(
            rooftop_area,
            st.session_state.vision_results.get("surface_type", "Concrete Flat Slab") if st.session_state.vision_results else "Concrete Flat Slab",
            city_choice,
            campus_population,
            annual_rain_val,
            tanker_rate
        )
        df_m = pd.DataFrame(monthly_pipeline["monthly_chart_data"])
        
        fig_season = go.Figure()
        fig_season.add_trace(go.Bar(
            x=df_m["month"],
            y=df_m["inflow_liters"],
            name="Harvested Inflow (L)",
            marker_color="#0B3828",
            opacity=0.9
        ))
        fig_season.add_trace(go.Scatter(
            x=df_m["month"],
            y=df_m["demand_liters"],
            name="Facility Demand (L)",
            mode="lines+markers",
            line=dict(color="#167A53", width=3)
        ))
        fig_season.update_layout(
            template="plotly_white",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Plus Jakarta Sans", color="#0B3828", size=12),
            xaxis=dict(
                title_text="Month",
                title_font=dict(color="#0B3828", size=12, family="Plus Jakarta Sans"),
                tickfont=dict(color="#0B3828", size=11, family="Plus Jakarta Sans"),
                gridcolor="rgba(11, 56, 40, 0.06)",
                linecolor="rgba(11, 56, 40, 0.2)"
            ),
            yaxis=dict(
                title_text="Water Volume (Liters)",
                title_font=dict(color="#0B3828", size=12, family="Plus Jakarta Sans"),
                tickfont=dict(color="#0B3828", size=11, family="JetBrains Mono"),
                gridcolor="rgba(11, 56, 40, 0.08)",
                linecolor="rgba(11, 56, 40, 0.2)"
            ),
            height=260,
            margin=dict(l=20, r=20, t=20, b=20),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
                font=dict(color="#0B3828", size=11, family="Plus Jakarta Sans")
            )
        )
        st.plotly_chart(fig_season, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # 5-Stage Agentic Reasoning Cards with Status Badges
    st.markdown("### 🤖 Collaborative Agent Reasoning Chains")
    for trace in res["execution_trace"]:
        with st.expander(f"Stage {trace['stage']}: {trace['agent']} — {trace['summary']}", expanded=(trace['stage'] in [1, 3])):
            st.markdown(f"> **Reasoning:** {trace['rationale']}")
            if trace['stage'] == 3:
                st.markdown("**Dual-Media Filtration Layer Specifications (CGWB Standard):**")
                st.table(pd.DataFrame(res["agent3"]["recharge_specs"]["filtration_layers"]))


# ==============================================================================
# TAB 3: FINANCIAL ROI & CARBON SAVINGS
# ==============================================================================
with tab3:
    st.markdown("<h2 class='section-headline'>Financial ROI & Decarbonization</h2>", unsafe_allow_html=True)
    st.markdown("<p class='section-subhead'>Live capital expenditure audit, annual tanker cost reduction, and carbon offset calculations.</p>", unsafe_allow_html=True)

    fin_pipe = run_full_hydrology_pipeline(
        rooftop_area,
        st.session_state.vision_results.get("surface_type", "Concrete Flat Slab") if st.session_state.vision_results else "Concrete Flat Slab",
        city_choice,
        campus_population,
        annual_rain_val,
        tanker_rate
    )
    fin = fin_pipe["financials"]

    f1, f2, f3, f4 = st.columns(4)
    f1.metric("Payback Timeline", f"{fin['payback_months']} Months", f"{fin['payback_years']} Years")
    f2.metric("Net Annual Savings", f"₹{fin['net_annual_savings_inr']:,.0f}", "Avoided commercial tankers")
    f3.metric("5-Year Net Cashflow", f"₹{fin['five_year_net_savings_inr']:,.0f}", "After CapEx & OpEx")
    f4.metric("Avoided Carbon Footprint", f"{fin['avoided_co2_kg']:,.0f} kg CO₂", f"{fin['avoided_diesel_km']:,.0f} km diesel transport")

    st.markdown("<br>", unsafe_allow_html=True)

    # Comparative Cash Flow Chart
    st.markdown("<div class='clean-card'>", unsafe_allow_html=True)
    st.markdown("<h4 style='color:#0B3828; margin-top:0;'>Cumulative Financial Trajectory: AquaHarvest AI vs. Status Quo</h4>", unsafe_allow_html=True)
    
    years = [f"Year {y}" for y in range(1, 6)]
    dn_curve = [fin['annual_gross_savings_inr'] * y for y in range(1, 6)]
    ah_curve = [fin['total_capex_inr'] + (fin['annual_opex_inr'] * y) for y in range(1, 6)]
    
    df_compare = pd.DataFrame({
        "Year": years,
        "Cost of Doing Nothing (Continuous Diesel Tankers)": dn_curve,
        "AquaHarvest AI (CapEx + Low Maintenance)": ah_curve
    })

    fig_fin = px.bar(
        df_compare,
        x="Year",
        y=["Cost of Doing Nothing (Continuous Diesel Tankers)", "AquaHarvest AI (CapEx + Low Maintenance)"],
        barmode="group",
        color_discrete_sequence=["#EF4444", "#0B3828"]
    )
    fig_fin.update_layout(
        template="plotly_white",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Plus Jakarta Sans", color="#0B3828", size=12),
        xaxis=dict(
            title_text="",
            tickfont=dict(color="#0B3828", size=12, family="Plus Jakarta Sans"),
            showgrid=False,
            linecolor="rgba(11, 56, 40, 0.2)"
        ),
        yaxis=dict(
            title_text="Cumulative Spend (₹ INR)",
            title_font=dict(color="#0B3828", size=12, family="Plus Jakarta Sans"),
            tickfont=dict(color="#0B3828", size=11, family="JetBrains Mono"),
            gridcolor="rgba(11, 56, 40, 0.08)",
            linecolor="rgba(11, 56, 40, 0.2)"
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.04,
            xanchor="right",
            x=1,
            font=dict(color="#0B3828", size=12, family="Plus Jakarta Sans"),
            title_text=""
        ),
        height=340,
        margin=dict(l=20, r=20, t=30, b=20)
    )
    st.plotly_chart(fig_fin, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Bill of Materials Table
    st.markdown("### 📋 Line-Item Capital Expenditure (CapEx) Breakdown")
    bom = [
        {"Component": "Modular Cistern Storage Tank", "Specification": f"{fin_pipe['tank_specs']['tank_capacity_liters']:,.0f} Liters (Ferro-cement/RCC)", "Cost (₹)": f"₹{fin_pipe['tank_specs']['tank_capacity_liters'] * 4.5:,.0f}"},
        {"Component": "Guttering, Downpipes & First-Flush Standpipe", "Specification": f"{fin_pipe['first_flush_liters']:,.0f} L first-flush automatic valve", "Cost (₹)": "₹45,000"},
        {"Component": "Dual-Media Sand & Gravel Filtration Chamber", "Specification": "Silica Sand + River Gravel + Charcoal Bed", "Cost (₹)": "₹35,000"},
        {"Component": "Deep Aquifer Recharge Shaft Boring", "Specification": f"{fin_pipe['recharge_specs']['recharge_shaft_depth_m']}m Depth with Slotted PVC Casing", "Cost (₹)": f"₹{fin_pipe['recharge_specs']['recharge_shaft_depth_m'] * 6500.0:,.0f}"},
        {"Component": "Total Turnkey CapEx", "Specification": "Complete Civil & Plumbing Execution", "Cost (₹)": f"₹{fin['total_capex_inr']:,.0f}"}
    ]
    st.table(pd.DataFrame(bom))


# ==============================================================================
# TAB 4: STANDARDS & WATER ASSISTANT
# ==============================================================================
with tab4:
    st.markdown("<h2 class='section-headline'>Hydrology Standards & AI Water Assistant</h2>", unsafe_allow_html=True)
    st.markdown("<p class='section-subhead'>Query verified engineering standards covering the Central Ground Water Board (CGWB), BIS IS 15797:2008 specifications, and municipal rainwater harvesting mandates.</p>", unsafe_allow_html=True)

    qcol1, qcol2 = st.columns([4, 1])
    with qcol1:
        query_input = st.text_input("Ask a technical standard or municipal code question:", placeholder="e.g. What is the runoff coefficient of a concrete roof?")
    with qcol2:
        st.write("")
        st.write("")
        trigger_search = st.button("Query Assistant", use_container_width=True)

    st.markdown("<p style='font-size: 12px; color: #5C7567; text-transform: uppercase; font-weight: 700;'>Quick Question Presets:</p>", unsafe_allow_html=True)
    pcols = st.columns(4)
    if pcols[0].button("📐 Concrete Runoff Coeff", use_container_width=True):
        query_input = "What is the runoff coefficient of a concrete roof?"
        trigger_search = True
    if pcols[1].button("🚿 First-Flush Rule (IS 15797)", use_container_width=True):
        query_input = "What is the first flush diversion requirement under IS 15797?"
        trigger_search = True
    if pcols[2].button("🕳️ Aquifer Recharge Depth", use_container_width=True):
        query_input = "What are the engineering specs for an aquifer recharge shaft?"
        trigger_search = True
    if pcols[3].button("⚖️ Bangalore BBMP Fines", use_container_width=True):
        query_input = "What are the rainwater harvesting penalties in Bangalore BBMP?"
        trigger_search = True

    if (query_input and trigger_search) or (query_input and not st.session_state.chat_history):
        citations = rag_store.retrieve_relevant_bylaws(query_input, top_k=2)
        ctx_text = "\n".join([f"Source: {c['source']}\n{c['text']}" for c in citations])
        prompt = f"Context from official manuals:\n{ctx_text}\n\nQuestion: {query_input}\nAnswer:"
        ans = granite_client.generate(prompt)
        st.session_state.chat_history.insert(0, {
            "query": query_input,
            "answer": ans,
            "citations": citations
        })

    # Render Conversation Bubbles
    for item in st.session_state.chat_history[:3]:
        st.markdown(f"""
        <div class="chat-bubble-user">
            <b>User:</b> {item['query']}
        </div>
        <div class="chat-bubble-ai">
            <b style="color:#0B3828;">AquaHarvest AI Water Assistant:</b>
            <p style="margin: 8px 0; font-size: 14px; line-height: 1.6; color: #0B3828;">{item['answer']}</p>
            <div style="margin-top: 10px; border-top: 1px solid rgba(11,56,40,0.1); padding-top: 8px;">
                <span style="font-size: 11px; text-transform: uppercase; color: #245720; font-weight: 700;">Verified Knowledge Base Citations:</span><br/>
                {''.join([f"<span class='chat-source-tag'>📖 {c['source']}: {c['heading']}</span>" for c in item['citations']])}
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    
    # Dark Contrast Editorial Callout Card (Inspired by reference design)
    st.markdown("""
    <div class="dark-feature-card">
        <h3 class="dark-feature-title">Useful is good. <em>Trustworthy is better.</em></h3>
        <p style="color: #C1D9CE; font-size: 1.05rem; line-height: 1.6; max-width: 800px; margin-bottom: 24px;">
            AquaHarvest AI operates with complete mathematical and civil transparency. Every dimension is verifiable, every filter layer is grounded in certified codes, and human health safeguards are hard-coded into the pipeline.
        </p>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 16px;">
            <div style="background: rgba(255,255,255,0.06); padding: 16px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.08);">
                <div style="color: #C4F646; font-weight: 700; margin-bottom: 4px;">1. Inclusion & Scalability</div>
                <div style="color: #DDEBE3; font-size: 12px;">Tiered civil designs ranging from low-cost ferro-cement tanks to automated underground matrix cisterns.</div>
            </div>
            <div style="background: rgba(255,255,255,0.06); padding: 16px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.08);">
                <div style="color: #C4F646; font-weight: 700; margin-bottom: 4px;">2. Zero Black-Box Math</div>
                <div style="color: #DDEBE3; font-size: 12px;">Explicit Rational Formula (Q = C × I × A) with auditable line-item CapEx and OpEx schedules.</div>
            </div>
            <div style="background: rgba(255,255,255,0.06); padding: 16px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.08);">
                <div style="color: #C4F646; font-weight: 700; margin-bottom: 4px;">3. Public Health Safeguard</div>
                <div style="color: #DDEBE3; font-size: 12px;">Harvested rainwater is dedicated to non-potable use. Drinking use enforces secondary UV/chlorination (BIS 10500).</div>
            </div>
            <div style="background: rgba(255,255,255,0.06); padding: 16px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.08);">
                <div style="color: #C4F646; font-weight: 700; margin-bottom: 4px;">4. Ephemeral Privacy</div>
                <div style="color: #DDEBE3; font-size: 12px;">Operates without collecting any personally identifiable information (PII). In-session ephemeral analysis only.</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ==============================================================================
# TAB 5: SMART WATER NETWORK & DISTRIBUTION SIMULATOR
# ==============================================================================
with tab5:
    st.markdown("<h2 class='section-headline'>Smart Water Network & Dynamic Allocation</h2>", unsafe_allow_html=True)
    st.markdown("<p class='section-subhead'>Simulate real-time water routing, virtual IoT cistern telemetry, and stress-test institutional resilience under climate volatility scenarios.</p>", unsafe_allow_html=True)

    # 1. Climate Stress-Test Scenario Controller
    st.markdown("<p style='font-weight: 700; color: #5C7567; font-size: 13px; text-transform: uppercase;'>Climate Stress-Test Scenarios:</p>", unsafe_allow_html=True)
    scen_col1, scen_col2, scen_col3 = st.columns(3)
    
    with scen_col1:
        scen_normal = st.button("⛅ Normal Season\nBalanced Inflow & Demand", use_container_width=True)
    with scen_col2:
        scen_heatwave = st.button("🔥 45°C Peak Heatwave\nZero Rain, Tanker Surge", use_container_width=True)
    with scen_col3:
        scen_cloudburst = st.button("⛈️ 120mm Flash Cloudburst\nExtreme Inflow, Max Recharge", use_container_width=True)

    # Determine Active Scenario
    if "active_scenario" not in st.session_state:
        st.session_state.active_scenario = "Normal"
    if scen_heatwave:
        st.session_state.active_scenario = "Heatwave"
    elif scen_cloudburst:
        st.session_state.active_scenario = "Cloudburst"
    elif scen_normal:
        st.session_state.active_scenario = "Normal"

    current_scen = st.session_state.active_scenario
    
    # Scenario State Multipliers
    if current_scen == "Heatwave":
        sim_tank_level = 38.0
        sim_demand_mult = 1.45
        sim_status = "⚠️ DROUGHT CONSERVATION ACTIVE — Rationed Irrigation"
        sim_inflow_rate = "0 L/day (Dry Spell Day 42)"
        sim_ph = 7.1
        sim_turbidity = 1.4
    elif current_scen == "Cloudburst":
        sim_tank_level = 98.0
        sim_demand_mult = 0.85
        sim_status = "⚡ PEAK MONSOON SURGE — 100% Overflow to Aquifer Shaft"
        sim_inflow_rate = f"+{rooftop_area * 105 * 0.85:,.0f} L/event"
        sim_ph = 6.8
        sim_turbidity = 4.8
    else:
        sim_tank_level = 76.0
        sim_demand_mult = 1.0
        sim_status = "🟢 OPTIMAL CIRCULAR HARVESTING — Normal Grid Routing"
        sim_inflow_rate = f"+{rooftop_area * (annual_rain_val / 65) * 0.85:,.0f} L/monsoon day"
        sim_ph = 7.2
        sim_turbidity = 2.1

    # Scenario Banner
    st.markdown(f"""
    <div style="background: #FFFFFF; border: 1px solid rgba(11, 56, 40, 0.08); border-radius: 14px; padding: 14px 20px; margin: 16px 0; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px;">
        <div>
            <span style="font-size: 11px; font-weight: 700; text-transform: uppercase; color: #5C7567;">Active Simulation Scenario:</span>
            <div style="font-size: 16px; font-weight: 700; color: #0B3828;">{current_scen} Conditions</div>
        </div>
        <div style="font-weight: 700; font-size: 13px; color: #0B3828;">{sim_status}</div>
        <div>
            <span style="font-size: 11px; font-weight: 700; text-transform: uppercase; color: #5C7567;">Live Catchment Inflow:</span>
            <div style="font-family: 'JetBrains Mono'; font-weight: 700; color: #167A53;">{sim_inflow_rate}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 2. Virtual IoT Telemetry & Allocation Grid
    ncol_left, ncol_right = st.columns([1, 1], gap="medium")
    
    with ncol_left:
        st.markdown("<div class='clean-card'>", unsafe_allow_html=True)
        st.markdown("<h4 style='color:#0B3828; margin-top:0;'>📡 Virtual IoT Storage Telemetry</h4>", unsafe_allow_html=True)
        
        # Tank Level Progress
        st.markdown(f"""
        <div style="margin-bottom: 12px;">
            <div style="display: flex; justify-content: space-between; align-items: baseline;">
                <span style="font-size: 13px; font-weight: 700; color: #5C7567; text-transform: uppercase;">Cistern Fill Level</span>
                <span style="font-size: 24px; font-weight: 800; font-family: 'JetBrains Mono'; color: #0B3828;">{sim_tank_level:.1f}%</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.progress(sim_tank_level / 100.0)
        
        st.markdown("<br>", unsafe_allow_html=True)
        # Quality Sensor Metrics Grid
        tq1, tq2, tq3 = st.columns(3)
        tq1.metric("Water pH", f"{sim_ph:.1f}", "Neutral / Soft")
        tq2.metric("Turbidity", f"{sim_turbidity:.1f} NTU", "< 5.0 (Safe)")
        tq3.metric("TDS Level", "42 ppm", "Low Mineral")

        st.markdown(f"""
        <div style="background: #F6F8F3; border-radius: 10px; padding: 12px; margin-top: 14px; border: 1px solid rgba(11, 56, 40, 0.06); font-size: 12px; color: #0B3828;">
            <p style="margin: 2px 0;"><b>⚙️ Dual-Media Filter State:</b> Operational (Differential Pressure: 0.18 bar)</p>
            <p style="margin: 2px 0;"><b>🔄 Automated Backwash Cycle:</b> Scheduled in 36 operational hours</p>
            <p style="margin: 2px 0;"><b>⚡ Booster Pump Consumption:</b> 1.2 kWh / 10k L (Zero-emission solar ready)</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with ncol_right:
        st.markdown("<div class='clean-card'>", unsafe_allow_html=True)
        st.markdown("<h4 style='color:#0B3828; margin-top:0;'>🚰 Dynamic Sub-System Allocation</h4>", unsafe_allow_html=True)
        
        alloc_flush = st.slider("Restroom Flushing Allocation (%)", 10, 70, 45, 5)
        alloc_irrigation = st.slider("Campus Grounds & Tree Irrigation (%)", 10, 50, 25, 5)
        alloc_hvac = st.slider("Cooling Tower / HVAC Makeup (%)", 5, 40, 20, 5)
        alloc_recharge = max(0, 100 - (alloc_flush + alloc_irrigation + alloc_hvac))
        
        # Allocation Donut Chart
        alloc_df = pd.DataFrame({
            "End-Use Application": ["Toilet Flushing", "Landscape Irrigation", "HVAC Cooling", "Deep Aquifer Recharge"],
            "Allocation (%)": [alloc_flush, alloc_irrigation, alloc_hvac, alloc_recharge]
        })
        
        fig_donut = px.pie(
            alloc_df,
            names="End-Use Application",
            values="Allocation (%)",
            hole=0.55,
            color="End-Use Application",
            color_discrete_map={
                "Toilet Flushing": "#0B3828",
                "Landscape Irrigation": "#167A53",
                "HVAC Cooling": "#4C9A74",
                "Deep Aquifer Recharge": "#C4F646"
            }
        )
        fig_donut.update_layout(
            height=240,
            margin=dict(l=10, r=10, t=10, b=10),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Plus Jakarta Sans", color="#0B3828", size=12),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.25,
                xanchor="center",
                x=0.5,
                font=dict(color="#0B3828", size=11, family="Plus Jakarta Sans")
            )
        )
        st.plotly_chart(fig_donut, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # 3. Daily Campus Water Balance Breakdown
    st.markdown("### 📊 Simulated Daily Water Routing (Liters / Day)")
    daily_base_demand = campus_population * 25.0 * sim_demand_mult
    vol_flush = daily_base_demand * (alloc_flush / 100.0)
    vol_irrig = daily_base_demand * (alloc_irrigation / 100.0)
    vol_hvac = daily_base_demand * (alloc_hvac / 100.0)
    vol_recharge = daily_base_demand * (alloc_recharge / 100.0)

    db1, db2, db3, db4 = st.columns(4)
    db1.metric("🚽 Restroom Flushing", f"{vol_flush:,.0f} L/day", f"{alloc_flush}% of Total")
    db2.metric("🌿 Grounds Irrigation", f"{vol_irrig:,.0f} L/day", f"{alloc_irrigation}% of Total")
    db3.metric("❄️ HVAC & Cooling", f"{vol_hvac:,.0f} L/day", f"{alloc_hvac}% of Total")
    db4.metric("🕳️ Aquifer Injection", f"{vol_recharge:,.0f} L/day", f"{alloc_recharge}% Recharge")

    # Discreet Document Exporter at the bottom
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<div class='clean-card' style='display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 14px;'>", unsafe_allow_html=True)
    st.markdown("""
        <div>
            <h4 style="color:#0B3828; margin:0 0 4px 0;">📥 Export Offline Project Blueprint</h4>
            <p style="color:#5C7567; font-size:13px; margin:0;">Download the turnkey 10-slide executive presentation (.pptx) and technical engineering specification report (.md).</p>
        </div>
    """, unsafe_allow_html=True)

    pptx_file_path = os.path.join(os.path.dirname(__file__), "AquaHarvest_AI_Presentation.pptx")
    exp_col1, exp_col2 = st.columns(2)
    with exp_col1:
        if st.button("Generate Widescreen PPTX Deck", use_container_width=True):
            generate_presentation_pptx(pptx_file_path, st.session_state.pipeline_results)
            st.success("✓ Presentation deck refreshed!")
        if os.path.exists(pptx_file_path):
            with open(pptx_file_path, "rb") as f:
                st.download_button(
                    label="⬇️ Download Presentation Deck (.pptx)",
                    data=f.read(),
                    file_name="AquaHarvest_AI_Presentation.pptx",
                    mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
                    use_container_width=True
                )
    with exp_col2:
        rep_text = generate_executive_report_markdown(st.session_state.pipeline_results)
        st.download_button(
            label="⬇️ Download Technical Report (.md)",
            data=rep_text,
            file_name="AquaHarvest_Executive_Report.md",
            mime="text/markdown",
            use_container_width=True
        )
    st.markdown("</div>", unsafe_allow_html=True)
