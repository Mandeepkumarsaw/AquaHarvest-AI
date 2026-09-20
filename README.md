# 💧 AquaHarvest AI
### Next-Generation Smart Rainwater Harvesting, Runoff Mitigation & Aquifer Recharge Platform

---

## 🌍 Overview

**AquaHarvest AI** is an intelligent, multimodal climate-resilience decision-support system designed to solve the urban water paradox: **catastrophic monsoon runoff wastage and waterlogging followed by acute summer water distress and expensive commercial water tanker dependency.**

By combining **multimodal computer vision** for rooftop texture analysis with an **autonomous 5-stage engineering pipeline** and a **standards-based RAG engine**, AquaHarvest AI democratizes hydrological engineering, converting seasonal flood distress into circular, permanent water security.

## 🌐 Live Demo

🚀 **Hosted Application:** [AquaHarvest AI](https://aquaharvest-ai.streamlit.app/)

Try the deployed Streamlit application directly in your browser.

## ⚡ Key Highlights
1. **Multimodal Rooftop Computer Vision**: Classifies catchment surface materials (Concrete Slab $C=0.85$, Clay Tiles $C=0.75$, Corrugated Metal $C=0.90$, Green Roof $C=0.20$) and features a **98.5% precision debris/waste rejection guard**.
2. **Deterministic Civil Engineering Engine**: Mathematically verified Rational Method calculations ($Q = C \times I \times A$), 1.5mm first-flush diversion (IS 15797:2008), and cumulative inflow deficit storage tank sizing.
3. **Autonomous Multi-Stage Pipeline**: 5 specialized agents coordinating catchment yield, climate volatility modeling, modular cistern dimensions, financial payback, and civil safety safeguards.
4. **Offline-First RAG Standards Engine**: Built-in zero-cost hybrid vector search indexing Central Ground Water Board (CGWB) guidelines, BIS IS 15797:2008 codes, and state municipal bylaws.
5. **100% Free & Zero External Costs**: Operates completely offline with zero mandatory paid external APIs or cloud dependencies.

---

## 🤖 Multi-Stage Collaborative Workflow

```mermaid
sequenceDiagram
    autonumber
    actor User as Facility Manager
    participant Vision as Multimodal Vision Analyzer
    participant Agent1 as Catchment & Yield Analyst
    participant Agent2 as Climate Risk Predictor
    participant Agent3 as Storage & Sizing Engineer
    participant Agent4 as Financial ROI Auditor
    participant Agent5 as Civil Safety Auditor
    participant Exporter as Blueprint Generator

    User->>Vision: Uploads Rooftop Photo / Aerial View
    Vision-->>Agent1: Extracted Surface Type (Concrete Slab, C = 0.85)
    User->>Agent1: Catchment Footprint (e.g. 2,500 m²) & Population
    Agent1->>Agent1: Computes Annual Harvestable Yield (Q = C * I * A)
    Agent1->>Agent2: Passes Total Yield & Geo-Location (e.g. Bangalore)
    Agent2->>Agent2: Analyzes Monsoon Distribution & Dry Spell Length
    Agent2->>Agent3: Passes Peak Day Inflow & Buffer Requirements
    Agent3->>Agent3: Sizes Modular Cistern (m³) & Recharge Shaft Depth (m)
    Agent3->>Agent4: Passes Bill of Materials (BOM) & Sizing Schedule
    Agent4->>Agent4: Compares Against Commercial Tankers & Calculates Payback
    Agent4->>Agent5: Passes Complete Engineering & Financial Proposal
    Agent5->>Agent5: Enforces Filtration Safeguards & BIS 10500 Health Standards
    Agent5-->>User: Displays Verified System Blueprint & Interactive Charts
    User->>Exporter: Clicks "Build Presentation Deck & Reports"
    Exporter-->>User: Generates 10-Slide PPTX Deck & Executive Report
```

---

## 📂 Project Directory Structure

```
AquaHarvest AI/
├── .env.example                       # Optional environment configuration
├── README.md                          # Master documentation
├── requirements.txt                   # Free Python dependencies
├── app.py                             # Modern Streamlit web application
│
├── core/                              # Deterministic & multimodal engines
│   ├── __init__.py
│   ├── config.py                      # Rainfall databases, runoff coefficients & rates
│   ├── hydrology_math.py              # Rational Method & civil engineering math
│   ├── multimodal_vision.py           # Roof surface classifier & debris guard
│   └── deliverable_generator.py       # PPTX deck & executive report generator
│
├── ai/                                # Multi-agent AI subsystem
│   ├── __init__.py
│   ├── granite_client.py              # Offline reasoning core + optional live API
│   ├── agents.py                      # 5 Specialized Autonomous Agents
│   └── orchestrator.py                # Multi-agent sequential coordinator
│
├── rag/                               # Knowledge base & regulatory RAG
│   ├── __init__.py
│   ├── vector_store.py                # Zero-cost hybrid vector search manager
│   ├── embeddings.py                  # Text chunking & local TF-IDF vectorizer
│   └── data/
│       ├── cgwb_rwh_guidelines.txt    # CGWB official rainwater harvesting manual
│       ├── is_15797_standards.txt     # BIS IS 15797:2008 specifications
│       ├── municipal_bylaws.txt       # State municipal mandates & penalties
│       └── water_quality_norms.txt    # Non-potable reuse and filtration criteria
│
├── assets/                            # Visual assets & styling
│   ├── style.css                      # Modern eco-luxury editorial CSS theme
│   └── sample_roof.jpg                # Benchmark rooftop test image
│
└── tests/                             # Automated test suite
    ├── __init__.py
    ├── test_hydrology.py              # Hydrological formula assertions
    ├── test_agents.py                 # Multi-agent pipeline tests
    ├── test_rag.py                    # RAG retrieval and citation tests
    └── test_vision.py                 # Computer vision & debris rejection tests
```

---


## 🎯 Problem Statement

Urban areas face two connected water-management challenges:

- Excess monsoon runoff that is lost as surface drainage or contributes to waterlogging.
- Seasonal water stress that can increase dependence on commercial water tankers.

AquaHarvest AI is designed as a decision-support platform that connects rooftop rainwater capture, runoff mitigation, storage sizing, aquifer recharge, financial analysis, and standards-oriented safeguards in one workflow.

## 🏗️ Core Capabilities

| Capability | What it does |
|---|---|
| 🏠 Rooftop Analysis | Uses multimodal computer vision to identify rooftop/catchment surface characteristics. |
| 🌧️ Rainwater Yield | Estimates harvestable runoff using catchment area, rainfall, and runoff coefficient inputs. |
| 💧 Storage & Recharge | Supports cistern sizing and recharge planning based on modeled inflow and demand/deficit conditions. |
| 🤖 Multi-Agent Pipeline | Coordinates specialized agents for hydrology, climate risk, storage, finance, and civil safety. |
| 📚 Standards RAG | Retrieves relevant information from the project's embedded CGWB, BIS, municipal, and water-quality knowledge base. |
| 💰 Financial Analysis | Compares proposed water infrastructure with commercial tanker expenditure and estimates payback. |
| 📊 Reports & Decks | Generates engineering/financial deliverables including presentation and executive-report outputs. |

## 🛠️ Technology Stack

- **Python**
- **Streamlit** — interactive web application
- **Multimodal Computer Vision** — rooftop/catchment analysis
- **Multi-Agent AI Pipeline** — specialized engineering and analysis agents
- **RAG / Hybrid Vector Search** — standards and regulatory knowledge retrieval
- **Pandas / NumPy** — data processing and numerical calculations
- **Matplotlib / Plotting Components** — analytical visualization
- **python-pptx / Report Generation** — project deliverables
- **Unit Testing** — automated verification of core modules

## 📋 Typical Workflow

1. Upload a rooftop photo or aerial/catchment image.
2. Provide catchment footprint and relevant location/population inputs.
3. Analyze rooftop surface characteristics and runoff coefficient.
4. Calculate harvestable rainfall/runoff.
5. Model rainfall distribution, dry spells, and climate-related requirements.
6. Size storage and recharge infrastructure.
7. Estimate material requirements and financial payback.
8. Apply filtration, water-quality, and civil-safety safeguards.
9. Review the generated system blueprint and interactive analysis.
10. Export the engineering/financial reports and presentation deck.

## ⚙️ Configuration

If configuration is required, start from the provided environment template:

```bash
cp .env.example .env
```

Keep secrets and API credentials in `.env` and **do not commit them to GitHub**.

The project is designed with an offline-first approach, so the core workflow does not require mandatory paid external APIs.

## 🧪 Testing

Run the complete automated test suite with:

```bash
python -m unittest discover -s tests -v
```

The repository includes tests covering:

- Hydrological calculations
- Multi-agent behavior
- RAG retrieval/citation functionality
- Rooftop vision/debris rejection

## 📸 Demo / Screenshots

For a stronger GitHub project presentation, add screenshots or GIFs of:

- Streamlit landing page
- Rooftop image analysis
- Hydrological calculations
- Storage/recharge sizing
- Financial ROI/payback analysis
- RAG/standards results
- Final blueprint/report generation

Place project screenshots under `assets/` and reference them from this README.

## 🚀 Live Application

**Try AquaHarvest AI online:**  
https://aquaharvest-ai.streamlit.app/

**Source Code:**  
https://github.com/Mandeepkumarsaw/AquaHarvest-AI

> The hosted application provides the easiest way to explore the project without setting up the repository locally.

## 👥 Intended Users

AquaHarvest AI is intended as a decision-support and planning platform for:

- Facility and building managers
- Urban water-management teams
- Civil/environmental engineering workflows
- Sustainability teams
- Rainwater-harvesting planners
- Researchers and students exploring climate-resilience systems

> **Note:** AquaHarvest AI is a decision-support system. Site-specific construction, structural, groundwater, drinking-water, and regulatory decisions should be independently reviewed by appropriately qualified professionals and local authorities.


## 🚀 Quickstart Guide

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run Verification Unit Tests
```bash
python -m unittest discover -s tests -v
```

### 3. Launch the Application
```bash
streamlit run app.py
```
Open your browser at `http://localhost:8501`.


