"""Task 2 — streaming descriptive and grouped statistics using only the standard library."""
import argparse, collections, csv, json, math, statistics
from pathlib import Path

MISSING = {'', 'na', 'n/a', 'none', 'null', 'nan', 'not available'}
NUMERIC = ('estimated_audience_size', 'estimated_impressions', 'estimated_spend')
GROUP_METRIC = 'estimated_spend'

def valid(value):
    return value is not None and str(value).strip().lower() not in MISSING

def number(value):
    if not valid(value): return None
    try:
        x = float(str(value).strip().replace(',', '').replace('$', ''))
        return x if math.isfinite(x) else None
    except ValueError: return None

def grouped_row(row, key):
    return tuple(row.get(col, '') for col in key)

def describe(values):
    if not values: return {'count':0,'mean':None,'min':None,'max':None,'std':None,'median':None}
    return {'count':len(values),'mean':statistics.fmean(values),'min':min(values),'max':max(values),
            'std':statistics.stdev(values) if len(values)>1 else None,'median':statistics.median(values)}

def analyze(path):
    with open(path, newline='', encoding='utf-8-sig') as handle:
        reader=csv.DictReader(handle); fields=reader.fieldnames or []
        if not {'page_id','ad_id'}.issubset(fields): raise ValueError('Dataset must have page_id and ad_id')
        missing=collections.Counter(); value_counts={c:collections.Counter() for c in fields if c not in NUMERIC}
        numeric={c:[] for c in NUMERIC if c in fields}
        groups={keys:collections.defaultdict(lambda:[0,0.0]) for keys in [('page_id',),('page_id','ad_id')]}
        rows=0; invalid_numeric=collections.Counter()
        for row in reader:
            rows+=1
            for c in fields:
                v=row.get(c)
                if not valid(v): missing[c]+=1
                elif c in numeric:
                    n=number(v)
                    if n is None: invalid_numeric[c]+=1
                    else: numeric[c].append(n)
                else: value_counts[c][v]+=1
            n=number(row.get(GROUP_METRIC))
            for keys, table in groups.items():
                record=table[grouped_row(row,keys)]; record[0]+=1
                if n is not None:record[1]+=n
    categorical={}
    for c, counts in value_counts.items():
        top=sorted(counts.items(),key=lambda kv:(-kv[1],kv[0]))[:5]
        categorical[c]={'count':sum(counts.values()),'unique':len(counts),
                        'mode':top[0][0] if top else None,'mode_frequency':top[0][1] if top else 0,
                        'top_5':[{'value':v,'frequency':k} for v,k in top]}
    grouped={}
    for keys, table in groups.items():
        top=sorted(table.items(),key=lambda item:(-item[1][1],item[0]))[:10]
        grouped['+'.join(keys)]={'group_count':len(table),'top_10_by_estimated_spend':[
            {'group':list(key),'ad_records':val[0],'estimated_spend_total':round(val[1],6)} for key,val in top]}
    return {'dataset':Path(path).name,'rows':rows,'columns':len(fields),'missing':dict(missing),
            'missing_percent':{c:round(100*missing[c]/rows,4) if rows else None for c in fields},
            'inferred_types':{c:('numeric' if c in numeric else 'categorical_or_date_or_structured') for c in fields},
            'numeric':{c:describe(v) for c,v in numeric.items()},'non_numeric':categorical,
            'invalid_numeric':dict(invalid_numeric),'grouped':grouped,
            'note':'Sample standard deviation (ddof=1); estimated_spend totals are summed estimates, not audited expenditure.'}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('csv_file');p.add_argument('--output',default='outputs/pure_python_results.json');a=p.parse_args()
    result=analyze(a.csv_file);out=Path(a.output);out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(result,indent=2,ensure_ascii=False),encoding='utf-8')
    print('Rows:',result['rows'],'Columns:',result['columns'],'Groups:',{k:v['group_count'] for k,v in result['grouped'].items()})
    print('Estimated spend:',result['numeric'].get('estimated_spend'));print('Saved',out)
