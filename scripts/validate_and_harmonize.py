#!/usr/bin/env python3
import csv, json, argparse, datetime

REQUIRED = ["study_id","title","year","ml_family","datasets","task_type"]
NUMERIC_FIELDS = ["performance.accuracy","performance.precision_macro","performance.recall_macro","performance.f1_macro","performance.f1_weighted","performance.roc_auc","performance.mcc","performance.far","performance.dr"]

def to_rate(x):
    try:
        v = float(x)
        if v > 1 and v <= 100:
            return v / 100.0
        return v
    except Exception:
        return ""

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in_csv", required=True)
    ap.add_argument("--out_csv", default="clean.csv")
    ap.add_argument("--out_jsonl", default="clean.jsonl")
    args = ap.parse_args()

    with open(args.in_csv, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    errors = []
    for i, r in enumerate(rows, start=2):
        for key in REQUIRED:
            if not r.get(key):
                errors.append((i, key, "missing"))
        for key in NUMERIC_FIELDS:
            if r.get(key) not in (None, ""):
                r[key] = to_rate(r[key])
        if not r.get("extracted_on"):
            r["extracted_on"] = str(datetime.date.today())

    with open(args.out_csv, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=rows[0].keys())
        w.writeheader()
        for r in rows:
            w.writerow(r)

    with open(args.out_jsonl, "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    if errors:
        print("[warn] Validation issues (first 20):")
        for e in errors[:20]:
            print(f"  line {e[0]}: {e[1]} -> {e[2]}")
    print(f"[ok] Wrote {args.out_csv} and {args.out_jsonl}")

if __name__ == "__main__":
    main()
