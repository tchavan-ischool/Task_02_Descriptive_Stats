"""Compare the numeric and grouped output of three implementations."""
import json, math
from pathlib import Path
p=Path('outputs')
names=[name for name in ('pure_python','pandas','polars') if (p/f'{name}_results.json').exists()]
results={name:json.loads((p/f'{name}_results.json').read_text()) for name in names}
if len(names)<2: raise SystemExit('Run at least two analysis scripts before validating')
base=results['pure_python']
issues=[]
for name,other in results.items():
    for field in ('rows','columns'):
        if base[field]!=other[field]:issues.append((name,field,base[field],other[field]))
    for c,metric in base['numeric'].items():
        for stat,v in metric.items():
            w=other['numeric'][c][stat]
            if v is None or w is None:
                if v!=w:issues.append((name,c,stat,v,w))
            elif not math.isclose(v,w,rel_tol=1e-9,abs_tol=1e-5):issues.append((name,c,stat,v,w))
    for group,val in base['grouped'].items():
        if val['group_count']!=other['grouped'][group]['group_count']:
            issues.append((name,group,'group_count'))
    if any(base['missing'].get(c,0)!=other['missing'].get(c,0) for c in base['inferred_types']):issues.append((name,'missing value counts differ'))
if issues:
    print('Discrepancies:',*issues[:30],sep='\n');raise SystemExit(1)
print('PASS for',', '.join(names),': dataset dimensions, numeric statistics, missing counts and group counts match.')
