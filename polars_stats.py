"""Task 2 — Polars expression-based column statistics and grouped analysis.

Requires polars; uses scan_csv for lazy input and expressions for aggregation.
"""
import argparse, collections, json, math
from pathlib import Path
import polars as pl
from pure_python_stats import NUMERIC, MISSING, describe


def analyze(path):
    lf=pl.scan_csv(path, infer_schema_length=0,encoding='utf8-lossy')
    fields=lf.collect_schema().names()
    if not {'page_id','ad_id'}.issubset(fields):raise ValueError('Missing page_id/ad_id')
    # Normalize missing sentinels. Keep all source columns as strings to avoid silent type inference.
    normalized=lf.select([pl.when(pl.col(c).str.strip_chars().str.to_lowercase().is_in(list(MISSING)))
                            .then(None).otherwise(pl.col(c)).alias(c) for c in fields])
    rows=normalized.select(pl.len()).collect().item()
    missing=normalized.select([pl.col(c).is_null().sum().alias(c) for c in fields]).collect().row(0,named=True)
    numeric={};categorical={};invalid={}
    for c in fields:
        if c in NUMERIC:
            expr=pl.col(c).str.replace_all(',','').str.replace_all(r'\$','').cast(pl.Float64,strict=False)
            stats=normalized.select(expr.alias('v')).select([
                pl.col('v').count().alias('count'),pl.col('v').mean().alias('mean'),
                pl.col('v').min().alias('min'),pl.col('v').max().alias('max'),
                pl.col('v').std(ddof=1).alias('std'),pl.col('v').median().alias('median')]).collect().row(0,named=True)
            numeric[c]=stats
            invalid[c]=int(normalized.select((pl.col(c).is_not_null() & expr.is_null()).sum()).collect().item())
        else:
            frequency=normalized.group_by(c).agg(pl.len().alias('frequency')).filter(pl.col(c).is_not_null())
            agg=frequency.select(pl.col('frequency').sum().alias('count'),pl.len().alias('unique')).collect().row(0,named=True)
            top=frequency.sort(['frequency',c],descending=[True,False]).limit(5).collect().iter_rows(named=True)
            top=[{'value':rec[c],'frequency':rec['frequency']} for rec in top]
            categorical[c]={'count':int(agg['count'] or 0),'unique':int(agg['unique']),
                            'mode':top[0]['value'] if top else None,'mode_frequency':top[0]['frequency'] if top else 0,'top_5':top}
    spend=pl.col('estimated_spend').cast(pl.Float64,strict=False).fill_null(0)
    grouped={}
    for keys in [['page_id'],['page_id','ad_id']]:
        g=normalized.group_by(keys).agg(pl.len().alias('ad_records'),spend.sum().alias('estimated_spend_total'))
        group_count=g.select(pl.len()).collect().item()
        top=g.sort(['estimated_spend_total']+keys,descending=[True]+[False]*len(keys)).limit(10).collect()
        grouped['+'.join(keys)]={'group_count':group_count,'top_10_by_estimated_spend':[
            {'group':[rec[k] for k in keys],'ad_records':rec['ad_records'],
             'estimated_spend_total':round(rec['estimated_spend_total'],6)} for rec in top.iter_rows(named=True)]}
    return {'dataset':Path(path).name,'rows':rows,'columns':len(fields),'missing':missing,
            'missing_percent':{c:round(100*missing[c]/rows,4) if rows else None for c in fields},
            'inferred_types':{c:('numeric' if c in numeric else 'categorical_or_date_or_structured') for c in fields},
            'numeric':numeric,'non_numeric':categorical,'invalid_numeric':invalid,'grouped':grouped,
            'note':'Sample standard deviation (ddof=1); estimated_spend totals are summed estimates, not audited expenditure.'}
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('csv_file');p.add_argument('--output',default='outputs/polars_results.json');a=p.parse_args()
    result=analyze(a.csv_file);out=Path(a.output);out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(result,indent=2,ensure_ascii=False),encoding='utf-8');print('Saved',out)
