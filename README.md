# Gallium TEA – ESCAPE 36 Paper

Techno-Economic Analysis (TEA) model for the recovery of **4N-grade gallium** from GaAs
semiconductor manufacturing wastewater. This repository accompanies the ESCAPE 36 conference
paper:

> Kozerke, K. et al. (2026). *Techno-economic feasibility of gallium recovery from
> semiconductor wastewater*. ESCAPE 36, Sheffield, 21–24 June 2026.

## Scope

**In scope:** LCOGa (levelised cost of gallium), annual production, cost breakdown, and
break-even throughput (Q*).

**Out of scope:** LCA (life-cycle assessment) and CO₂ tax. Carbon costs are excluded from
all cost outputs.

## Process Overview

Two recovery routes share a common upstream section and diverge at the selective separation step:

```
Route A — Ion Exchange (IX)
  Raw feed → Filtration → RO Split → pH Adjust → IX Separation
           → Precipitation → Selective Leaching → Electrowinning

Route B — Solvent Extraction (SX)
  Raw feed → Filtration → RO Split → pH Adjust → SX Separation
           → Precipitation → Selective Leaching → Electrowinning
```

**Feed:** GaAs process wastewater, **34.6 mg/L Ga**, pH 3.8 (Jain 2019).

**Throughput range:** Q = 10 – 100 m³/d

## TEA Methodology

**System boundary:** Gate-to-gate, from raw GaAs wastewater inlet to refined 4N gallium product.

**Functional unit:** 1 kg of 4N gallium produced.

**Cost framework:** LCOGa = TC / m_Ga,ann, where total annual cost TC = CapEx + OpEx + REP + Labour.

**Capital recovery factor:** AF = r(1+r)^n / ((1+r)^n − 1); default r=0.08, n=20 years.

## Key Outputs

| Q (m³/d) | LCOGa IX (€/kg) | LCOGa SX (€/kg) |
|----------|-----------------|-----------------|
| 10       | 563             | 701             |
| 20       | 329             | 408             |
| 50       | 189             | 219             |
| 100      | 144             | 161             |

**Break-even throughput (Q*):** IX ≈ 14.2 m³/d, SX ≈ 19.3 m³/d (market price 423 €/kg).

## Requirements

- Python ≥ 3.9
- NumPy, Matplotlib, Pandas

```bash
pip install -r requirements.txt
```

## Usage

```python
import tea_model_ga_escape36 as tea

Q = 30.0  # m³/d

lco_ix = tea.calc_lco_ga(Q, route='IX')
lco_sx = tea.calc_lco_ga(Q, route='SX')
print(f"IX: {lco_ix:.1f} EUR/kg   SX: {lco_sx:.1f} EUR/kg")

bd = tea.calc_cost_breakdown(Q, route='IX')
```

`DEFAULT_CONFIG` already encodes the ESCAPE baseline.
Pass a custom config via `tea.calc_lco_ga(Q, config=my_config)` if needed.

## Reproducing Paper Results

From the repository root:

```bash
python scripts/run_all.py
```

This generates:
- `outputs/csv/` — lcoga_vs_q.csv, annual_production.csv, cost_breakdown_by_block.csv,
  cost_breakdown_by_step.csv, q_star.csv
- `outputs/figures/` — figure2a_production.svg, figure2b_lcoga.svg, figure3_cost_breakdown.svg
- `outputs/metadata.json` — baseline configuration and timestamp

## File Structure

```
tea_model_ga_escape36.py         Core TEA model
config/
  escape36_config.py        ESCAPE baseline configuration
scripts/
  export_baseline.py        CSV and metadata export
  fig_lcoga_vs_q.py         LCOGa vs Q figure
  run_all.py                Master runner
outputs/                    Generated on first run
README.md
requirements.txt
LICENSE
```

## Related Work

This repository accompanies the ESCAPE 36 conference paper. A more comprehensive analysis—
including LCA, carbon-cost integration, sensitivity analysis, and scenario robustness—is
available in the associated master's thesis:

> Kozerke, K. (2025). *Techno-Economic Analysis of Gallium Recovery from GaAs Semiconductor
> Manufacturing Wastewater* (Master's Thesis). University of Cambridge / WZL RWTH Aachen
> University. [PDF – link to be added when available]

## Citation

If you use this model in academic work, please cite the ESCAPE 36 paper and, where
appropriate, the thesis.

## Licence

MIT — see [LICENSE](LICENSE).
