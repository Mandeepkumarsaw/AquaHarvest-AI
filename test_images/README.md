# 📸 AquaHarvest AI - Open-Source Benchmark Test Images

This directory contains curated, open-source benchmark test images for testing the **AquaHarvest AI Multimodal Computer Vision Engine**.

---

## 📂 Test Images Catalog

### 1. `01_concrete_terrace_roof.jpg`
- **Surface Category**: Urban Concrete Flat Slab / RCC Terrace
- **Expected Classification**: `Concrete Flat Slab`
- **Runoff Coefficient ($C$)**: `0.85`
- **Debris Risk**: Low (Uniform architectural plane)
- **Catchment Validity**: `True` (Certified Catchment)
- **Open-Source Origin**: Wikimedia Commons / Public Domain Architectural Catchments
  - Reference: [Wikimedia Commons - Concrete Roofs](https://commons.wikimedia.org/wiki/Category:Concrete_roof_tiles)

---

### 2. `02_terracotta_clay_tiles.jpg`
- **Surface Category**: Sloped Terracotta / Clay Tile Array
- **Expected Classification**: `Terracotta / Clay Tiles`
- **Runoff Coefficient ($C$)**: `0.75`
- **Debris Risk**: Moderate (Valleys & joints)
- **Catchment Validity**: `True` (Certified Catchment)
- **Open-Source Origin**: Wikimedia Commons / Public Domain
  - Reference: [Wikimedia Commons - Terracotta Roof Tiles](https://commons.wikimedia.org/wiki/File:Terracotta_roof_tiles.jpg)

---

### 3. `03_industrial_corrugated_metal.jpg`
- **Surface Category**: Galvanized Iron / Corrugated Metal Industrial Sheeting
- **Expected Classification**: `Corrugated GI Sheets`
- **Runoff Coefficient ($C$)**: `0.90` (Peak Hydraulic Efficiency)
- **Debris Risk**: Low to Moderate (Atmospheric soot)
- **Catchment Validity**: `True` (Certified Catchment)
- **Open-Source Origin**: Wikimedia Commons / Public Domain
  - Reference: [Wikimedia Commons - Corrugated Metal Roof](https://commons.wikimedia.org/wiki/File:Corrugated_metal_roof-2.jpg)

---

### 4. `04_vegetated_green_roof.jpg`
- **Surface Category**: Vegetated Substrate / Sedum Green Eco-Roof
- **Expected Classification**: `Grass / Green Roof`
- **Runoff Coefficient ($C$)**: `0.20` (High Biological Retention)
- **Debris Risk**: High (Organic matter & root sediment)
- **Catchment Validity**: `True` (Certified Catchment with Bio-Filtration)
- **Open-Source Origin**: Wikimedia Commons / Public Domain
  - Reference: [Wikimedia Commons - Green Roofs](https://commons.wikimedia.org/wiki/Category:Green_roofs)

---

### 5. `05_solid_waste_hazard_debris.png`
- **Surface Category**: Non-Catchment Municipal Solid Waste & Plastic Clutter
- **Expected Classification**: `Contaminated Surface: High-Density Solid Waste & Debris`
- **Runoff Coefficient ($C$)**: `0.0`
- **Waste Detection Confidence**: `98.5%`
- **Catchment Validity**: `False` (**AUTOMATIC SAFETY REJECTION**)
- **Safety Alert**: `⛔ CONTAMINATION HAZARD: Water diversion aborted to safeguard cistern health.`
- **Open-Source Origin**: Public Domain Waste / Litter Benchmark Imagery

---

## 🧪 How to Test in the Application
1. Open the app at **[http://localhost:8501](http://localhost:8501)**.
2. Go to **Tab 1: Catchment & Roof Vision**.
3. Under **"Instant Open-Source Test Gallery"**, click any benchmark button to test in 1 click, or drag-and-drop any of these files into the **Upload Rooftop Imagery** uploader!
