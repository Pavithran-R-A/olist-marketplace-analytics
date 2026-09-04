from __future__ import annotations

import csv
import json
from pathlib import Path

from .config import REPORTS, ROOT


def _records(name: str) -> list[dict[str, str]]:
    with (REPORTS / f"{name}.csv").open(encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def build_dashboard() -> Path:
    k = json.loads((REPORTS / "kpis.json").read_text(encoding="utf-8"))
    data = {name: _records(name) for name in (
        "monthly_kpis", "category_kpis", "state_kpis", "seller_kpis",
        "fulfillment_category", "freight_state", "review_outcomes",
        "customer_cohorts", "rfm_segments")}
    payload = json.dumps(data)
    html = f"""<!doctype html><html><head><meta charset='utf-8'>
<meta name='viewport' content='width=device-width'><title>Olist Marketplace Intelligence</title>
<script src='https://cdn.plot.ly/plotly-2.35.2.min.js'></script>
<style>body{{font:15px system-ui;background:#f5f7fb;color:#172033;margin:0}}main{{max-width:1200px;margin:auto;padding:24px}}.sub{{color:#64748b}}nav{{display:flex;gap:8px;flex-wrap:wrap;margin:24px 0}}button{{border:0;border-radius:8px;padding:11px 16px;background:#dbe4ef;font-weight:600}}button.active{{background:#0f766e;color:white}}.view{{display:none}}.view.active{{display:block}}.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:14px}}.card,.panel{{background:white;border-radius:12px;padding:18px;box-shadow:0 2px 12px #17203312}}.value{{font-size:25px;font-weight:700;color:#0f766e}}.charts{{display:grid;grid-template-columns:repeat(auto-fit,minmax(380px,1fr));gap:18px;margin-top:18px}}.chart{{height:320px}}li{{margin:10px 0}}footer{{margin-top:28px;color:#64748b}}</style></head>
<body><main><p class='sub'>OLIST MARKETPLACE PERFORMANCE INTELLIGENCE</p>
<h1>GMV, fulfillment, and customer experience</h1>
<p class='sub'>Decision support for Operations, Finance, and Marketplace leadership.</p>
<nav><button class='tab active' data-view='executive'>Executive Overview</button><button class='tab' data-view='fulfillment'>Fulfillment &amp; Customer Experience</button><button class='tab' data-view='customer'>Customer &amp; Growth</button></nav>
<section id='executive' class='view active'><div class='grid'>
<div class='card'>GMV<div class='value'>R$ {k['gmv']:,.0f}</div></div><div class='card'>Orders<div class='value'>{k['orders']:,.0f}</div></div><div class='card'>AOV<div class='value'>R$ {k['aov']:,.2f}</div></div><div class='card'>Delivered<div class='value'>{k['delivered_orders']:,.0f}</div></div><div class='card'>Late rate<div class='value'>{k['late_delivery_rate']:.1%}</div></div><div class='card'>Review<div class='value'>{k['avg_review']:.2f} / 5</div></div><div class='card'>Repeat rate<div class='value'>{k['repeat_customer_rate']:.1%}</div></div></div>
<div class='charts'><div class='panel'><h2>Monthly GMV and orders</h2><div id='trend' class='chart'></div></div><div class='panel'><h2>Category contribution</h2><div id='categories' class='chart'></div></div><div class='panel'><h2>State performance</h2><div id='states' class='chart'></div></div></div>
<div class='panel'><h2>Management attention</h2><ul><li>Late orders average {k['late_review']['mean']:.2f} reviews versus {k['ontime_review']['mean']:.2f} on time.</li><li>Freight equals {k['freight_to_gmv']:.1%} of merchandise value.</li><li>Repeat purchasing is {k['repeat_customer_rate']:.1%} of observed customers.</li></ul></div></section>
<section id='fulfillment' class='view'><div class='charts'><div class='panel'><h2>Late delivery by state</h2><div id='stateLate' class='chart'></div></div><div class='panel'><h2>Late delivery by category</h2><div id='categoryLate' class='chart'></div></div><div class='panel'><h2>Freight burden by state</h2><div id='freight' class='chart'></div></div><div class='panel'><h2>Review outcomes</h2><div id='reviews' class='chart'></div></div><div class='panel'><h2>High-volume seller exceptions</h2><div id='sellers' class='chart'></div></div></div></section>
<section id='customer' class='view'><div class='charts'><div class='panel'><h2>RFM segment distribution</h2><div id='rfm' class='chart'></div></div><div class='panel'><h2>Cohort retention heatmap</h2><div id='cohort' class='chart'></div></div></div><div class='panel'><p>Repeat rate excludes canceled and unavailable orders. Cohorts show observed retention only.</p></div></section>
<footer>Source: Olist Brazilian E-Commerce Public Dataset. GMV means item merchandise value, not recognized revenue.</footer></main>
<script>const D={payload};const n=(r,k)=>+r[k];const p=(id,t,l={{}})=>Plotly.newPlot(id,t,Object.assign({{margin:{{t:20,l:55,r:20,b:55}},paper_bgcolor:'white',font:{{family:'system-ui'}}}},l),{{responsive:true,displaylogo:false}});const m=D.monthly_kpis,c=D.category_kpis.slice(0,12),s=D.state_kpis,fc=D.fulfillment_category,fs=D.freight_state,rv=D.review_outcomes,se=D.seller_kpis.slice(0,12),rf=D.rfm_segments,co=D.customer_cohorts;
p('trend',[{{x:m.map(r=>r.month),y:m.map(r=>n(r,'gmv')),name:'GMV',type:'bar'}},{{x:m.map(r=>r.month),y:m.map(r=>n(r,'orders')),name:'Orders',yaxis:'y2',type:'scatter'}}],{{yaxis:{{title:'GMV (R$)'}},yaxis2:{{title:'Orders',overlaying:'y',side:'right'}}}});p('categories',[{{x:c.map(r=>r.category),y:c.map(r=>n(r,'gmv')),type:'bar',marker:{{color:'#0f766e'}}}}],{{xaxis:{{tickangle:-35}}}});p('states',[{{x:s.map(r=>r.state),y:s.map(r=>n(r,'gmv')),type:'bar'}},{{x:s.map(r=>r.state),y:s.map(r=>n(r,'late_rate')*100),type:'scatter',yaxis:'y2'}}],{{yaxis2:{{title:'Late %',overlaying:'y',side:'right'}}}});p('stateLate',[{{x:s.map(r=>r.state),y:s.map(r=>n(r,'late_rate')*100),type:'bar'}}]);p('categoryLate',[{{x:fc.map(r=>r.category),y:fc.map(r=>n(r,'late_rate')*100),type:'bar'}}],{{xaxis:{{tickangle:-35}},yaxis:{{title:'Late %'}}}});p('freight',[{{x:fs.map(r=>r.state),y:fs.map(r=>n(r,'freight_to_gmv')*100),type:'bar'}}]);p('reviews',[{{x:['On time','Late'],y:[n(rv.find(r=>r.is_late==='False'),'mean_review'),n(rv.find(r=>r.is_late==='True'),'mean_review')],type:'bar',marker:{{color:['#0f766e','#dc2626']}}}}],{{yaxis:{{range:[0,5]}}}});p('sellers',[{{x:se.map(r=>r.seller_id),y:se.map(r=>n(r,'late_rate')*100),text:se.map(r=>'Orders: '+r.orders),type:'bar'}}]);p('rfm',[{{x:rf.map(r=>r.segment),y:rf.map(r=>n(r,'customers')),type:'bar'}}]);p('cohort',[{{x:co.map(r=>+r.months_since_first),y:co.map(r=>r.cohort_month),z:co.map(r=>n(r,'retention_rate')*100),type:'heatmap',colorscale:'Teal'}}]);document.querySelectorAll('.tab').forEach(b=>b.onclick=()=>{{document.querySelectorAll('.tab,.view').forEach(x=>x.classList.remove('active'));b.classList.add('active');document.getElementById(b.dataset.view).classList.add('active');window.dispatchEvent(new Event('resize'))}});</script></body></html>"""
    target = ROOT / "dashboard" / "index.html"
    target.write_text(html, encoding="utf-8")
    return target


if __name__ == "__main__":
    print(build_dashboard())
