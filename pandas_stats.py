"""Task 2 — equivalent statistics with Pandas, reading CSV in chunks to limit memory use."""
import argparse, collections, json
from pathlib import Path
import pandas as pd
from pure_python_stats import NUMERIC, MISSING, number, describe


def analyze(path, chunk_size=20000):
    # The descriptive and categorical aggregation APIs are Pandas-specific;
    # chunking avoids requiring enough RAM for the entire 500 MB CSV at once.
    categorical={};numeric={};missing=collections.Counter();groups={};rows=0;columns=None;invalid=collections.Counter()
    for chunk in pd.read_csv(path,dtype=str,keep_default_na=False,chunksize=chunk_size,encoding='utf-8-sig'):
        if columns is None:
            columns=list(chunk.columns)
            if not {'page_id','ad_id'}.issubset(columns):raise ValueError('Missing page_id/ad_id')
            categorical={c:collections.Counter() for c in columns if c not in NUMERIC}
            numeric={c:[] for c in NUMERIC if c in columns}
            groups={'page_id':collections.defaultdict(lambda:[0,0.0]),'page_id+ad_id':collections.defaultdict(lambda:[0,0.0])}
        rows+=len(chunk)
        clean=chunk.replace(r'^\s*(?:|na|n/a|none|null|nan|not available)\s*$',pd.NA,regex=True)
        missing.update(clean.isna().sum().to_dict())
        for c in categorical:
            counts=clean[c].dropna().value_counts(dropna=True)
            categorical[c].update({str(v):int(n) for v,n in counts.items()})
        for c in numeric:
            parsed=pd.to_numeric(clean[c].str.replace(',','',regex=False).str.replace('$','',regex=False),errors='coerce')
            invalid[c]+=int(parsed.isna().sum()-clean[c].isna().sum())
            numeric[c].extend(parsed.dropna().astype(float).tolist())
        spend=pd.to_numeric(clean['estimated_spend'],errors='coerce').fillna(0.)
        subset=chunk[['page_id','ad_id']].copy();subset['spend']=spend
        for group_cols,name in [(['page_id'],'page_id'),(['page_id','ad_id'],'page_id+ad_id')]:
            aggregated=subset.groupby(group_cols,dropna=False).agg(ad_records=('spend','size'),estimated_spend_total=('spend','sum')).reset_index()
            for record in aggregated.itertuples(index=False,name=None):
                key=tuple(str(v) for v in record[:len(group_cols)])
                obj=groups[name][key];obj[0]+=int(record[-2]);obj[1]+=float(record[-1])
    non_numeric={}
    for c, counts in categorical.items():
        top=sorted(counts.items(),key=lambda kv:(-kv[1],kv[0]))[:5]
        non_numeric[c]={'count':sum(counts.values()),'unique':len(counts),
                        'mode':top[0][0] if top else None,'mode_frequency':top[0][1] if top else 0,
                        'top_5':[{'value':v,'frequency':n} for v,n in top]}
    grouped={}
    for name,table in groups.items():
        top=sorted(table.items(),key=lambda item:(-item[1][1],item[0]))[:10]
        grouped[name]={'group_count':len(table),'top_10_by_estimated_spend':[
            {'group':list(k),'ad_records':v[0],'estimated_spend_total':round(v[1],6)} for k,v in top]}
    return {'dataset':Path(path).name,'rows':rows,'columns':len(columns),'missing':dict(missing),
            'missing_percent':{c:round(100*missing[c]/rows,4) if rows else None for c in columns},
            'inferred_types':{c:('numeric' if c in numeric else 'categorical_or_date_or_structured') for c in columns},
            'numeric':{c:describe(vals) for c,vals in numeric.items()},'non_numeric':non_numeric,
            'invalid_numeric':dict(invalid),'grouped':grouped,
            'note':'Sample standard deviation (ddof=1); estimated_spend totals are summed estimates, not audited expenditure.'}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('csv_file');p.add_argument('--output',default='outputs/pandas_results.json');a=p.parse_args()
    result=analyze(a.csv_file);out=Path(a.output);out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(result,indent=2,ensure_ascii=False),encoding='utf-8')
    print('Rows:',result['rows'],'Columns:',result['columns'],'Groups:',{k:v['group_count'] for k,v in result['grouped'].items()}); print('Saved',out)
