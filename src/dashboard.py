from __future__ import annotations

import json
from pathlib import Path

from .config import PUBLISHED, ROOT


def build_dashboard() -> Path:
    data = {p.stem: json.loads(p.read_text(encoding="utf-8")) for p in PUBLISHED.glob("*.json")}
    for p in PUBLISHED.glob("*.csv"):
        rows = p.read_text(encoding="utf-8").splitlines()
        data[p.stem] = {"headers": rows[0].split(","), "rows": rows[1:]}
    k = data["kpis"]
    html = f'''<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>Olist Marketplace Intelligence</title><script src="https://cdn.plot.ly/plotly-2.35.2.min.js"></script><style>body{{font:15px system-ui;background:#f5f7fb;color:#172033;margin:0}}main{{max-width:1180px;margin:auto;padding:32px}}h1{{font-size:32px}}.sub{{color:#64748b}}.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:14px}}.card,.panel{{background:white;border-radius:12px;padding:18px;box-shadow:0 2px 12px #17203312}}.value{{font-size:25px;font-weight:700;color:#0f766e}}.charts{{display:grid;grid-template-columns:repeat(auto-fit,minmax(420px,1fr));gap:18px;margin-top:20px}}.chart{{height:330px}}li{{margin:10px 0}}footer{{margin-top:30px;color:#64748b}}</style></head><body><main><p class="sub">OLIST MARKETPLACE PERFORMANCE INTELLIGENCE</p><h1>GMV, fulfillment, and customer experience</h1><p class="sub">Decision support for Operations, Finance, and Marketplace leadership.</p><section class="grid"><div class="card">GMV<div class="value">R$ {k['gmv']:,.0f}</div></div><div class="card">Orders<div class="value">{k['orders']:,.0f}</div></div><div class="card">AOV<div class="value">R$ {k['aov']:,.2f}</div></div><div class="card">Late delivery<div class="value">{k['late_delivery_rate']:.1%}</div></div><div class="card">Avg review<div class="value">{k['avg_review']:.2f} / 5</div></div><div class="card">Repeat customers<div class="value">{k['repeat_customer_rate']:.1%}</div></div></section><section class="charts"><div class="panel"><h2>Marketplace trend</h2><div id="trend" class="chart"></div></div><div class="panel"><h2>Leading categories</h2><div id="category" class="chart"></div></div><div class="panel"><h2>Regional GMV and late rate</h2><div id="state" class="chart"></div></div><div class="panel"><h2>Late delivery and reviews</h2><div id="review" class="chart"></div></div></section><section class="panel" style="margin-top:20px"><h2>Management attention</h2><ul><li>Late deliveries average {k['late_avg_review']:.2f} review points versus {k['ontime_avg_review']:.2f} on time.</li><li>Freight represents {k['freight_to_gmv']:.1%} of merchandise value.</li><li>Repeat purchasing is {k['repeat_customer_rate']:.1%} of observed customers.</li></ul></section><footer>Source: Olist Brazilian E-Commerce Public Dataset. GMV means item merchandise value, not recognized marketplace revenue. Static companion; Power BI assets provide the semantic build specification.</footer></main><script>const monthly={json.dumps(data['monthly'])};const category={json.dumps(data['category'])};const states={json.dumps(data['states'])};const review={json.dumps(data['review'])};function rows(x){{return x.rows.map(r=>Object.fromEntries(r.split(',').map((v,i)=>[x.headers[i],v])))}}const m=rows(monthly),c=rows(category),s=rows(states),rv=rows(review);Plotly.newPlot('trend',[{{x:m.map(x=>x.month),y:m.map(x=>+x.gmv),name:'GMV',type:'bar'}},{{x:m.map(x=>x.month),y:m.map(x=>+x.orders),name:'Orders',yaxis:'y2',type:'scatter'}}],{{margin:{{t:10}},yaxis:{{title:'GMV (R$)'}},yaxis2:{{title:'Orders',overlaying:'y',side:'right'}}}});Plotly.newPlot('category',[{{x:c.map(x=>x.category),y:c.map(x=>+x.gmv),type:'bar',marker:{{color:'#0f766e'}}}}],{{margin:{{t:10}},xaxis:{{tickangle:-35}}}});Plotly.newPlot('state',[{{x:s.map(x=>x.state),y:s.map(x=>+x.gmv),type:'bar',name:'GMV'}},{{x:s.map(x=>x.state),y:s.map(x=>+x.late_rate*100),type:'scatter',name:'Late %',yaxis:'y2'}}],{{margin:{{t:10}},yaxis2:{{title:'Late %',overlaying:'y',side:'right'}}}});Plotly.newPlot('review',[{{x:['On time','Late'],y:[+rv.find(x=>x.is_late==='False').avg_review,+rv.find(x=>x.is_late==='True').avg_review],type:'bar',marker:{{color:['#0f766e','#dc2626']}}}}],{{margin:{{t:10}},yaxis:{{range:[0,5],title:'Average review'}}}});</script></body></html>'''
    target = ROOT / "dashboard" / "index.html"
    target.write_text(html, encoding="utf-8")
    return target


if __name__ == "__main__":
    print(build_dashboard())

