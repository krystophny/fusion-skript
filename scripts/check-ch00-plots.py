"""Default-Matplotlib numerical checks; these are not final slide artwork."""
import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT/'derivations/build/plotdata'
OUT = ROOT/'derivations/build/check'


def load(name):
    return json.loads((DATA/(name+'.json')).read_text())


def save(fig, name):
    fig.tight_layout()
    fig.savefig(OUT/(name+'.png'), dpi=120)
    plt.close(fig)


def build():
    OUT.mkdir(parents=True, exist_ok=True)
    d = load('02-energy-gdp')
    rows = d['observations']
    fig,ax = plt.subplots()
    ax.scatter([r['x'] for r in rows],[r['y'] for r in rows],s=[r['population']/1e6 for r in rows],alpha=.5)
    for r in rows:
        if r['iso3'] in ['AUT','USA','CHN','IND']:ax.annotate(r['iso3'],(r['x'],r['y']))
    ax.set(xscale='log',yscale='log',xlabel='GDP PPP [2021 international $ / person / year]',
        ylabel='Primary energy [kWh / person / day]',title='CHECK: 2024; marker area ∝ population')
    save(fig,'02-energy-gdp')
    d = load('03-access-and-dollarstreet')
    fig,axes = plt.subplots(1,4,figsize=(12,4))
    for ax,p in zip(axes,sorted(d['photos'],key=lambda p:p['income'])):
        ax.imshow(Image.open(ROOT/'slides/photos'/p['file']))
        ax.set_title(f"{p['title']}\nPPP ${p['income']:g} / equivalent adult / month",fontsize=8)
        ax.axis('off')
    save(fig,'03-dollarstreet')
    d = load('04-micro-macro')
    fig,axes = plt.subplots(1,2,figsize=(10,4))
    axes[0].barh(list(d['legacy_components']),list(d['legacy_components'].values()))
    axes[0].set(xlabel='kWh / person / day',title='CHECK: 2025 handwritten budget')
    axes[1].bar(['Bottom-up','Gross inland','Final'],[d['legacy_total'],d['gross_kWh_person_day'],d['final_kWh_person_day']])
    axes[1].set(ylabel='kWh / person / day',title='Different accounting boundaries; 2025 preliminary')
    save(fig,'04-micro-macro')
    d = load('05-austria-flow')
    carriers = [n for n in d['nodes'] if n['stage']==3]
    sectors = [n for n in d['nodes'] if n['stage']==4]
    matrix = np.zeros((len(carriers),len(sectors)))
    for i,c in enumerate(carriers):
        for j,s in enumerate(sectors):
            matrix[i,j] = sum(l['value'] for l in d['links'] if l['source']==c['id'] and l['target']==s['id'])
    fig,axes = plt.subplots(1,2,figsize=(12,5))
    im = axes[0].imshow(matrix,aspect='auto')
    axes[0].set_xticks(range(len(sectors)),[s['label'] for s in sectors],rotation=45,ha='right')
    axes[0].set_yticks(range(len(carriers)),[c['label'] for c in carriers])
    axes[0].set_title('CHECK: actual final carrier × sector cells')
    fig.colorbar(im,ax=axes[0],label='kWh / person / day')
    labels = ['Final','Conversion','Energy sector / losses','Nonenergy']
    vals = [d['final_kWh_person_day'],d['conversion_loss_kWh_person_day'],d['own_use_and_transport_losses_kWh_person_day'],d['nonenergy_kWh_person_day']]
    axes[1].barh(labels,vals);axes[1].set(xlabel='kWh / person / day',title='Gross inland partitions')
    save(fig,'05-flow-conservation')
    d = load('06-resource-lifetimes')
    fig,axes = plt.subplots(1,2,figsize=(11,4))
    records = [r for r in d['resources'] if r['resource'] in ['coal_combined','oil','gas','uranium_identified_below_260_USD_kg']]
    for r in records:axes[0].plot(r['growth_continuous_percent_year'],r['growth_lifetime_years'],label=r['resource'])
    axes[0].set(xlabel='Continuous demand growth [% / year]',ylabel='Exhaustion [year]',title='CHECK: finite-stock model; BGR licence hold')
    axes[0].legend(fontsize=7)
    axes[1].barh([r['resource'] for r in records],[r['power_W_person_for_1000_years'] for r in records])
    axes[1].set(xlabel='Thermal W / person for 1000 years',title='2024 world population; U once-through model')
    save(fig,'06-resource-lifetimes')
    d = load('07-solar-chain')
    fig,axes = plt.subplots(1,2,figsize=(12,4))
    names = [r['stage'] for r in d['stages']]
    values = [r['W_m2'] for r in d['stages']]
    axes[0].plot(range(len(values)),values,'o-')
    axes[0].set_xticks(range(len(names)),names,rotation=60,ha='right')
    axes[0].set(ylabel='W / m²',title='CHECK: calibrated chain to module-area PV mean')
    axes[1].bar(d['months'],d['monthly_horizontal_kWh_m2'])
    axes[1].set(xlabel='Month',ylabel='Horizontal irradiation [kWh / m²]',title='Graz SARAH3 2005–2023 climatology')
    save(fig,'07-solar-chain')
    d = load('09-pv-prices')
    fig,ax = plt.subplots()
    for keep,label in [(True,'Nemet and Farmer–Lafond'),(False,'IRENA / pvXchange attributed series')]:
        pairs = [(y,p) for y,p in zip(d['years'],d['prices']) if (y<=2009)==keep]
        ax.plot([y for y,p in pairs],[p for y,p in pairs],label=label)
    ax.set(yscale='log',xlabel='Year',ylabel='Module price [constant 2025 USD / Wp]',title='CHECK: modules, not installed-system cost');ax.legend()
    save(fig,'09-pv-prices')
    d = load('09-pv-capacity')
    fig,axes = plt.subplots(1,2,figsize=(10,4))
    for ax,key,label in [(axes[0],'world_PV','World'),(axes[1],'austria_PV','Austria')]:
        ax.plot(d['years'],np.asarray(d[key])/1000);ax.set(xlabel='Year',ylabel='PV [GW, year end]',title=label+'; © IRENA 2026 attributed reuse')
    save(fig,'09-pv-capacity')
    d = load('10-wind')
    fig,axes = plt.subplots(1,2,figsize=(10,4))
    axes[0].bar(['US onshore 2016','Horns Rev + EU CF'],[d['us_onshore_W_m2'],d['offshore_HornsRev_W_m2_scenario']])
    axes[0].set(ylabel='Average W / m²',title='CHECK: observed sample vs offshore scenario')
    axes[1].bar(['EU onshore 2024','EU offshore 2024','Austria 2025 proxy'],
        np.asarray([d['eu_onshore_cf'],d['eu_offshore_cf'],d['austria_cf_endyear_proxy']])*100)
    axes[1].set(ylabel='Capacity factor [%]',title='Fleet values; Austria end-year capacity proxy')
    save(fig,'10-wind')
    d = load('11-area-budget')
    fig,ax = plt.subplots()
    names = ['biofuel','wind','solar_low','solar_high']
    for i,boundary in enumerate(['final','gross_inland']):
        vals = [r['fraction_of_Austria']*100 for r in d['scenarios'] if r['boundary']==boundary]
        ax.bar(np.arange(4)+i*.35,vals,width=.35,label=boundary)
    ax.set_xticks(np.arange(4)+.175,names);ax.set(ylabel='Austria area [%]',title='CHECK: prescribed 0.5 / 2 / 10 / 20 W/m²');ax.legend()
    save(fig,'11-area-budget')
    corn=d['corn_ethanol']
    fig,ax=plt.subplots()
    ax.bar(['Corn ethanol gross','Wind scenario','Solar scenario'],[corn['density_W_m2'],2,10],color=['#D55E00','#009E73','#0072B2'])
    ax.set(yscale='log',ylabel='Average energy output [W/m²]',title='CHECK: corn chain excludes inputs/coproduct credit')
    save(fig,'11-corn-ethanol')
    d = load('12-fission')
    fig,axes = plt.subplots(1,2,figsize=(11,4))
    axes[0].bar(['Enriched U','Natural U'],[d['enriched_t_U'],d['natural_t_U']]);axes[0].set(ylabel='t U / GW(e) full-power year',title='Once-through, 45 GWd/t, 33%, 4.5% enrichment')
    axes[1].bar(['Austria / 30 yr','World-at-Austria / 30 yr','Historical grid peak'],
        list(d['reactors_per_year_over_30_years'].values())+[33]);axes[1].set(yscale='log',ylabel='1 GW(e) units / year',title='CHECK: 90% CF; scenario vs observed connections')
    save(fig,'12-fission')
    d = load('13-fusion')
    fig,ax = plt.subplots()
    ax.bar(['D','T','D + T','Coal, 24 MJ/kg'],[d['deuterium_kg'],d['tritium_kg'],d['fuel_kg'],d['coal_kg']])
    ax.set(yscale='log',ylabel='kg / GW(thermal) full-power year',title='CHECK: burned fuel, not plant inventory or electricity')
    save(fig,'13-fusion')
    d=load('14-wildlife-risk'); rows=[r for r in d['annual_estimates'] if r['unit']=='birds/year']
    fig,ax=plt.subplots()
    ys=np.arange(len(rows)); low=np.array([float(r['low']) for r in rows]);high=np.array([float(r['high']) for r in rows])
    ax.hlines(ys,low,high,lw=4);ax.set_xscale('log');ax.set_yticks(ys,[r['cause'] for r in rows]);ax.invert_yaxis()
    ax.set(xlabel='Annual US bird deaths [birds/year]',title='CHECK: heterogeneous bird mortality ranges')
    save(fig,'14-bird-mortality')
    d=load('14-energy-deaths'); rows=d['observations']
    fig,ax=plt.subplots();rows=sorted(rows,key=lambda r:float(r['deaths_per_TWh']))
    ax.barh([r['source_type'] for r in rows],[float(r['deaths_per_TWh']) for r in rows])
    ax.set(xscale='log',xlabel='Deaths per TWh electricity',title='CHECK: OWID 2021 mixed air-pollution / accident sources')
    save(fig,'14-energy-deaths')
    d=load('15-lifecycle-emissions'); rows=d['observations'];fig,ax=plt.subplots()
    for y,r in enumerate(rows):
        ax.hlines(y,float(r['min_gCO2eq_kWh']),float(r['max_gCO2eq_kWh']))
        ax.plot(float(r['median_gCO2eq_kWh']),y,'o')
    ax.set_xscale('log');ax.set_yticks(range(len(rows)),[r['technology'] for r in rows]);ax.invert_yaxis()
    ax.set(xlabel='g CO₂-eq/kWh electricity',title='CHECK: lifecycle study ranges')
    save(fig,'15-lifecycle-emissions')
    print('Wrote 16 default-Matplotlib check plots; geographic equal-scale check is separate.')


if __name__ == '__main__':
    build()
