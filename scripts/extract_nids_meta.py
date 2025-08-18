#!/usr/bin/env python3
# (full extractor, as before)
import os, re, csv, json, argparse
try:
    import PyPDF2
    HAVE_PYPDF2 = True
except Exception:
    HAVE_PYPDF2 = False

DATASET_PATTERNS = [r'NSL[-\s]?KDD', r'KDD\s?Cup\s?99', r'UNSW[-\s]?NB15', r'CIC[-\s]?IDS[-\s]?2017', r'CIC[-\s]?IDS[-\s]?2018', r'CSE[-\s]?CIC[-\s]?IDS[-\s]?2018', r'CIC[-\s]?DDoS[-\s]?2019', r'BoT[-\s]?IoT', r'ToN[-\s]?IoT', r'ISCX\s?2012', r'CIC[-\s]?DoHBrw[-\s]?2020', r'UNSW[-\s]?Edge[-\s]?IIoT', r'Darknet[-\s]?2020', r'MAWILab', r'CTU[-\s]?13']

METRIC_PATTERNS = {
    "accuracy": r'(?:Acc(?:uracy)?)[^\d]{0,10}([0-9]*\.?[0-9]+)\s?%?',
    "precision_macro": r'(?:macro[-\s]?precision)[^\d]{0,10}([0-9]*\.?[0-9]+)\s?%?',
    "recall_macro": r'(?:macro[-\s]?recall)[^\d]{0,10}([0-9]*\.?[0-9]+)\s?%?',
    "f1_macro": r'(?:macro[-\s]?F1|F1[-\s]?macro)[^\d]{0,10}([0-9]*\.?[0-9]+)\s?%?',
    "f1_weighted": r'(?:weighted[-\s]?F1|F1[-\s]?weighted)[^\d]{0,10}([0-9]*\.?[0-9]+)\s?%?',
    "roc_auc": r'(?:ROC[-\s]?AUC|AUC[-\s]?ROC)[^\d]{0,10}([0-9]*\.?[0-9]+)',
    "mcc": r'(?:MCC)[^\d\-]{0,10}([-+]?[0-9]*\.?[0-9]+)',
    "far": r'(?:FAR|False\s?Alarm\s?Rate)[^\d]{0,10}([0-9]*\.?[0-9]+)\s?%?',
    "dr": r'(?:DR|Detection\s?Rate)[^\d]{0,10}([0-9]*\.?[0-9]+)\s?%?'
}

SPLIT_HINTS = {
    "k-fold-cv": r'(\d+)[-\s]?fold(?:\s+cross[-\s]?validation)?',
    "time-based": r'(?:time[-\s]?split|chronological|temporal)\s+(?:split|validation)',
    "holdout": r'(?:train(?:ing)?/test|hold[-\s]?out|(?:\d{1,3})\s?/\s?(?:\d{1,3}))',
    "LOSO": r'leave[-\s]?one[-\s]?subject[-\s]?out|LOSO',
    "leave-one-attack-out": r'leave[-\s]?one[-\s]?attack[-\s]?out'
}

def extract_text(pdf_path):
    if HAVE_PYPDF2:
        try:
            text = []
            with open(pdf_path, "rb") as f:
                reader = PyPDF2.PdfReader(f)
                for page in reader.pages:
                    text.append(page.extract_text() or "")
            return "\n".join(text)
        except Exception:
            pass
    try:
        with open(pdf_path, "rb") as f:
            raw = f.read()
        return raw.decode("latin-1", errors="ignore")
    except Exception:
        return ""

def find_all(patterns, text):
    found = set()
    for p in patterns:
        for m in re.finditer(p, text, flags=re.I):
            found.add(m.group(0).strip())
    return sorted(found)

def extract_metrics(text):
    out = {}
    for key, pat in METRIC_PATTERNS.items():
        m = re.search(pat, text, flags=re.I)
        if m:
            try:
                val = float(m.group(1))
                if val > 1.0 and val <= 100.0:
                    val = val / 100.0
                out[key] = round(val, 4)
            except Exception:
                pass
    return out

def infer_split(text):
    for split, pat in SPLIT_HINTS.items():
        if re.search(pat, text, flags=re.I):
            k = None
            if split == "k-fold-cv":
                mk = re.search(SPLIT_HINTS["k-fold-cv"], text, flags=re.I)
                if mk:
                    try:
                        k = int(mk.group(1))
                    except Exception:
                        k = None
            return {"split_type": split, "k": k}
    return {"split_type": "not-reported", "k": None}

def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--pdf_dir", required=True)
    ap.add_argument("--out_csv", default="extracted.csv")
    ap.add_argument("--schema", default="data_extraction_schema.json")
    args = ap.parse_args()

    pdfs = [os.path.join(args.pdf_dir, f) for f in os.listdir(args.pdf_dir) if f.lower().endswith(".pdf")]
    rows = []
    for p in sorted(pdfs):
        text = extract_text(p)
        datasets = find_all(DATASET_PATTERNS, text)
        metrics = extract_metrics(text)
        split = infer_split(text)
        task = "binary" if re.search(r'\\bbinary\\b', text, re.I) else ("multiclass" if re.search(r'\\bmulticlass|\\bmulti[-\\s]?class', text, re.I) else "")
        rows.append({
            "study_id":"", "title":"", "year":"", "ml_family":"",
            "datasets":";".join(datasets), "task_type":task,
            "metrics_reported":";".join(metrics.keys()),
            "evaluation_protocol.split_type": split["split_type"],
            "evaluation_protocol.k": split["k"],
            "performance.accuracy": metrics.get("accuracy",""),
            "performance.precision_macro": metrics.get("precision_macro",""),
            "performance.recall_macro": metrics.get("recall_macro",""),
            "performance.f1_macro": metrics.get("f1_macro",""),
            "performance.f1_weighted": metrics.get("f1_weighted",""),
            "performance.roc_auc": metrics.get("roc_auc",""),
            "performance.mcc": metrics.get("mcc",""),
            "performance.far": metrics.get("far",""),
            "performance.dr": metrics.get("dr",""),
            "pdf_filename": os.path.basename(p)
        })

    out_cols = ["study_id","title","year","ml_family","datasets","task_type","metrics_reported","evaluation_protocol.split_type","evaluation_protocol.k","performance.accuracy","performance.precision_macro","performance.recall_macro","performance.f1_macro","performance.f1_weighted","performance.roc_auc","performance.mcc","performance.far","performance.dr","pdf_filename"]
    with open(args.out_csv, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=out_cols)
        w.writeheader()
        for r in rows:
            w.writerow(r)
    print(f"[ok] Parsed {len(rows)} PDFs. Wrote {args.out_csv}.")

if __name__ == "__main__":
    main()
