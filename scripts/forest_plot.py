#!/usr/bin/env python3
import json, argparse
import matplotlib.pyplot as plt

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--summary_json", required=True)
    ap.add_argument("--out_png", default="forest.png")
    a=ap.parse_args()
    data=json.load(open(a.summary_json,"r",encoding="utf-8"))
    labels=[]; pooled=[]; lcl=[]; ucl=[]
    for g,res in data.items():
        labels.append(g); pooled.append(res.get("pooled",0)); lcl.append(res.get("lcl",0)); ucl.append(res.get("ucl",0))
    fig=plt.figure(figsize=(7, max(3, 0.4*len(labels)+1)))
    y=list(range(len(labels)))
    plt.errorbar(pooled, y, xerr=[[p-l for p,l in zip(pooled,lcl)], [u-p for u,p in zip(ucl,pooled)]], fmt='o')
    plt.yticks(y, labels); plt.xlabel("Pooled effect (rate)"); plt.title("Forest plot"); plt.grid(True, axis='x', linestyle='--', alpha=0.4); plt.tight_layout()
    fig.savefig(a.out_png, dpi=200); print(f"[ok] Wrote {a.out_png}")
if __name__=="__main__": main()
