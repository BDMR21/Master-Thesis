# Concise Taxonomy — Datasets, Metrics, Protocols

## Datasets (common 2019–2025)
NSL-KDD, UNSW-NB15, CIC-IDS2017, CSE-CIC-IDS2018, CIC-DDoS2019, BoT-IoT, ToN-IoT,
CTU-13, MAWILab, ISCX2012, CIC-DoHBrw-2020, UNSW-Edge-IIoT, Darknet-2020, plus domain-specific sets.

## Metrics
- Class-aware: macro-F1, MCC, PR-AUC, per-class P/R/F1
- Aggregate/legacy: Accuracy, ROC-AUC
- Operational: FAR, DR/TPR, FPR/FNR, latency/throughput, memory/params

## Protocols
- Holdout (80/20, 70/30) with stratification
- k-fold CV / Stratified k-fold (k=5 or 10), repeated CV
- Time-based splits; cross-host/cross-scenario splits
- Cross-dataset evaluation (train on A, test on B)
- Leakage controls: no-host overlap, time separation, deduplication, fit transforms on train-only
