# \# Data Extraction Codebook — NIDS AI/ML (2019–2025)

# 

# Use this guide when extracting data from each paper. Field names map to `data\_extraction\_schema.json`.

# 

# \## Identification

# \- \*\*study\_id\*\* (required): unique slug (e.g., `lee2021-acsac` or BibTeX key).

# \- \*\*title\*\*, \*\*authors\*\*, \*\*year\*\*, \*\*venue\*\*, \*\*doi\*\*, \*\*url\*\*, \*\*pdf\_filename\*\*.

# 

# \## Taxonomy

# \- \*\*nids\_type\*\*: `anomaly | signature | hybrid | unspecified`.

# \- \*\*traffic\_modality\*\*: any of `flow | packet | payload | netflow/ipfix | pcap | logs | other`.

# \- \*\*features\*\*: `statistical | header | payload-bytes | embeddings | time-series | graph | image | other`.

# \- \*\*ml\_family\*\* (required): coarse model family (e.g., `tree-ensemble`, `cnn`, `autoencoder`).

# \- \*\*model.algorithm\*\*: specific algorithm (e.g., RandomForest, BiLSTM).

# \- \*\*model.architecture\*\*: brief layout for DL (layers/units).

# \- \*\*model.hyperparameters\*\*: short JSON-like text or sentence.

# 

# \## Datasets \& Task

# \- \*\*datasets\*\* (required): choose from enumerated list; if custom, use `Other` and fill `dataset\_other\_names`.

# \- \*\*task\_type\*\* (required): `binary | multiclass | multilabel`.

# \- \*\*class\_imbalance\_ratio\*\*: majority/minority ratio.

# \- \*\*imbalance\_handling\*\*: `smote | undersampling | oversampling | class-weights | threshold-tuning | focal-loss | none | other`.

# 

# \## Evaluation

# \- \*\*evaluation\_protocol.split\_type\*\*: `holdout | k-fold-cv | stratified-k-fold | time-based | LOSO | leave-one-attack-out | cross-dataset | nested-cv | not-reported`.

# \- \*\*k\*\*, \*\*train\_test\_split\*\*, \*\*validation\_split\*\*, \*\*random\_seed\_reported\*\*.

# \- \*\*leakage\_controls\*\*: `no-host-overlap | time-separated | deduplicated | feature-fit-only-train | not-reported`.

# 

# \## Metrics

# \- \*\*metrics\_reported\*\*: list the metrics as claimed.

# \- \*\*performance.\\\*\*\*: enter standardized rates in \[0,1] (MCC in \[-1,1]).

# \- \*\*per\_class\_metrics\*\*: per-class P/R/F1/support when given.

# \- \*\*confusion\_matrix.{tp,fp,fn,tn}\*\*: counts if provided.

# 

# \## Baselines \& Efficiency

# \- \*\*baselines\*\*: items with `{name,type,performance}`.

# \- \*\*runtime.\\\*\*\* and \*\*compute.\\\*\*\*: report training and inference results and the hardware used.

# 

# \## Reproducibility \& Risk

# \- \*\*reproducibility.\\\*\*\*: code URL, license, splits/seeds availability.

# \- \*\*threats\_to\_validity\*\*: select from the enumerated list; add notes in \*\*notes\*\*.

# \- \*\*quality\_score\*\*: subjective 0–10.

# 

# \## Tips

# \- Prefer macro-F1/MCC for imbalanced tasks.

# \- If papers report percentages, input the numeric value (validator will normalize to 0–1).

# \- Write N/A if truly not reported; avoid leaving cells blank.



