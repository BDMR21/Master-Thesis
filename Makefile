
.PHONY: extract validate meta forest all
extract:
	python scripts/extract_nids_meta.py --pdf_dir data/raw --out_csv data/interim/extracted.csv --schema data/schema/data_extraction_schema.json
validate:
	python scripts/validate_and_harmonize.py --in_csv data/interim/extracted.csv --out_csv data/interim/clean.csv --out_jsonl data/interim/clean.jsonl
meta:
	python scripts/meta_analyze.py --in data/interim/clean.csv --metric performance.f1_macro --group datasets --out results/tables/meta_summary.csv --json_out results/tables/meta_summary.json
forest:
	python scripts/forest_plot.py --summary_json results/tables/meta_summary.json --out_png results/figures/forest.png
all: extract validate meta forest
