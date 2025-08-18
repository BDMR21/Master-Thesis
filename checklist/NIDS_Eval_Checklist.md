# NIDS Eval-Check — Reporting & Evaluation Checklist (v1.0)

Use this list when designing and reporting AI/ML-based NIDS experiments.

## A. Dataset & Task
- [ ] Dataset name(s), version(s), and citation(s) clearly stated
- [ ] Data modality (flow/packet/payload/log) and acquisition context described
- [ ] Task type (binary/multiclass/multilabel) defined; class labels listed
- [ ] Class distribution and imbalance ratio reported
- [ ] Train/val/test partitions documented (counts per class)

## B. Preprocessing & Features
- [ ] Normalization/encoding steps specified (fit on train-only)
- [ ] Feature selection/engineering clearly described
- [ ] Leakage controls (no host overlap, time separation, deduplication)

## C. Model & Hyperparameters
- [ ] Algorithm family and specific architecture disclosed
- [ ] Hyperparameters with search ranges/strategy
- [ ] Random seeds for initialization and splits

## D. Evaluation Protocol
- [ ] Split type (holdout/k-fold/stratified/time-based/cross-dataset) justified
- [ ] For CV: k, repeats, stratification
- [ ] Threshold selection procedure (if applicable)
- [ ] External validation (cross-dataset/time-split) discussed

## E. Metrics & Reporting
- [ ] Primary metrics suitable for imbalance (macro-F1, MCC, PR-AUC)
- [ ] Per-class precision/recall/F1 and support
- [ ] Confidence intervals or variance across runs
- [ ] Confusion matrix for main setting
- [ ] Runtime/throughput and compute budget

## F. Baselines & Comparability
- [ ] Strong classical baselines and prior SOTA on same dataset/split
- [ ] Ablations for key design choices (features, architecture, sampling)
- [ ] Same preprocessing and splits across methods compared

## G. Reproducibility
- [ ] Code repository URL and license
- [ ] Exact data split files or seeds
- [ ] Environment details (framework, versions, hardware)
- [ ] End-to-end run instructions

## H. Threats to Validity
- [ ] Dataset bias or drift discussed
- [ ] Evaluation leakage risks assessed
- [ ] Limitations and external validity addressed
