#!/usr/bin/env python3
import csv, math, argparse, json

EPS = 1e-6
def logit(p): p=min(max(p,EPS),1-EPS); return math.log(p/(1-p))
def inv_logit(x): ex=math.exp(x); return ex/(1+ex)

def ds_laird(y, v):
    k=len(y); w=[1/vi for vi in v]; ybar=sum(wi*yi for wi,yi in zip(w,y))/sum(w)
    Q=sum(wi*(yi-ybar)**2 for wi,yi in zip(w,y)); c=sum(w)-sum(wi**2 for wi in w)/sum(w)
    tau2=max(0.0, (Q-(k-1))/c) if k>1 else 0.0
    wstar=[1/(vi+tau2) for vi in v]; mu=sum(wi*yi for wi,yi in zip(wstar,y))/sum(wstar)
    se=(1/sum(wstar))**0.5; I2=max(0.0,(Q-(k-1))/Q) if k>1 and Q>0 else 0.0
    return {"mu":mu,"se":se,"tau2":tau2,"Q":Q,"I2":I2,"k":k}

def pool_group(rows, metric, use_logit=True):
    y,v=[],[]
    for r in rows:
        try: p=float(r[metric])
        except: continue
        if use_logit: y.append(logit(p)); v.append(1.0/(p*(1-p)))
        else: y.append(p); v.append(1.0)
    if not y: return None
    out=ds_laird(y,v)
    if use_logit:
        out["pooled"]=inv_logit(out["mu"]); out["lcl"]=inv_logit(out["mu"]-1.96*out["se"]); out["ucl"]=inv_logit(out["mu"]+1.96*out["se"])
    else:
        out["pooled"]=out["mu"]; out["lcl"]=out["mu"]-1.96*out["se"]; out["ucl"]=out["mu"]+1.96*out["se"]
    return out

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--in", dest="in_csv", required=True)
    ap.add_argument("--metric", required=True)
    ap.add_argument("--group", default=None)
    ap.add_argument("--out", default="meta_summary.csv")
    ap.add_argument("--json_out", default="meta_summary.json")
    ap.add_argument("--no_logit", action="store_true")
    a=ap.parse_args()
    rows=list(csv.DictReader(open(a.in_csv, newline='', encoding='utf-8')))
    use_logit=not a.no_logit
    groups={"ALL":rows} if not a.group else {}
    if a.group:
        from collections import defaultdict
        gm=defaultdict(list)
        for r in rows: gm[r.get(a.group,"(missing)")].append(r)
        groups=dict(gm)
    summary=[]; report={}
    for g,rs in groups.items():
        res=pool_group(rs,a.metric,use_logit)
        if not res: continue
        summary.append({"group":g,"k":res["k"],"pooled":round(res["pooled"],4),"lcl":round(res["lcl"],4),"ucl":round(res["ucl"],4),"tau2":round(res["tau2"],6),"Q":round(res["Q"],4),"I2":round(100*res["I2"],1)})
        report[g]=res
    if summary:
        w=csv.DictWriter(open(a.out,"w",newline='',encoding='utf-8'), fieldnames=list(summary[0].keys())); w.writeheader(); [w.writerow(r) for r in summary]
    json.dump(report, open(a.json_out,"w",encoding="utf-8"), indent=2)
    print(f"[ok] Wrote {a.out} and {a.json_out}")
if __name__=="__main__": main()
