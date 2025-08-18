# Toward Standardized Evaluation of AI/ML-Based NIDS — Lab Guidance (Draft)

**Date:** 2025-08-18

## Executive Summary
Evaluation heterogeneity (datasets, splits, metrics, leakage controls) hinders fair comparison and slows deployment.
This guidance formalizes a checklist and workflow to make NIDS studies comparable and reproducible.

## Key Recommendations
1. Adopt the **NIDS Eval-Check** for all internal studies.
2. Prefer class-aware metrics (macro-F1, MCC, PR-AUC) and report uncertainty.
3. Publish code, exact splits/seeds, and instructions.
4. Use cross-dataset or time-based validation where possible.

## Minimal Taxonomy
See `NIDS_Taxonomy.md` for datasets, metrics, and protocol options.

## Reproducible Workflow
- Extract with `extract_nids_meta.py` → validate with `validate_and_harmonize.py`.
- Pool with `meta_analyze.py` → visualize with `forest_plot.py`.
- Archive clean tables and figures in `results/`.

## Outlook
The artifacts can be versioned and extended as new datasets/metrics appear.
