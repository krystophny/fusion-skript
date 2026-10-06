"""Generate original, light-background Chapter 0 SVGs from saved plot data."""
import json
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.path import Path as MplPath
from matplotlib.patches import PathPatch, Rectangle

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'derivations/build/plotdata'
OUT=ROOT/'derivations/build/fig'
BLUE='#356AA0'
ORANGE='#B86418'
GREEN='#2F7D5B'
PURPLE='#76528B'
GREY='#526175'


def load(name):
    return json.loads((DATA/(name+'.json')).read_text())


def finish(fig,name,source,metadata=None):
    fig.text(.01,.012,'Source: '+source,fontsize=7,color=GREY,ha='left',va='bottom',wrap=True)
    fig.tight_layout(rect=(0,.065,1,1))
    fig.savefig(OUT/(name+'.svg'),facecolor='white',metadata=metadata)
    plt.close(fig)


def income_energy():
    d=load('02-energy-gdp'); rows=d['observations']
    fig,ax=plt.subplots(figsize=(8,4.6))
    ax.scatter([r['x'] for r in rows],[r['y'] for r in rows],
        s=np.clip(np.array([r['population'] for r in rows])/1e6,4,800),
        color=BLUE,alpha=.45,edgecolors='none')
    for code,color in [('AUT',ORANGE),('USA',GREEN),('CHN',PURPLE),('IND','#CC79A7')]:
        r=next(x for x in rows if x['iso3']==code)
        ax.scatter(r['x'],r['y'],s=max(r['population']/1e6,30),color=color,edgecolor='black',linewidth=.4,zorder=3)
        ax.annotate(code,(r['x'],r['y']),xytext=(4,4),textcoords='offset points',fontsize=8)
    ax.set(xscale='log',yscale='log',xlabel='GDP PPP [2021 international $ / person / year]',
        ylabel='Primary energy [kWh / person / day]')
    ax.grid(True,which='major',alpha=.18)
    finish(fig,'energy-gdp',d['source'])


def income_levels():
    d=load('03-income-levels'); rows=d['observations']
    fig,ax=plt.subplots(figsize=(6.8,3.4))
    x=np.arange(len(rows)); values=[float(r['population_billions']) for r in rows]
    bars=ax.bar(x,values,color=[ORANGE,BLUE,GREEN,PURPLE],width=.68)
    ax.bar_label(bars,labels=[f"{v:g}" for v in values],padding=3)
    ax.set_xticks(x,[f"Level {r['level']}\n{r['income_threshold']}" for r in rows])
    ax.set(ylabel='Population [billion people]',xlabel='Household income or consumption [2011 PPP USD / person / day]')
    ax.grid(True,axis='y',alpha=.18)
    finish(fig,'income-levels',d['source'])


def energy_boundaries():
    d=load('04-micro-macro')
    labels=['2025 bottom-up','2025 gross inland','2025 final energy']
    values=[d['legacy_total'],d['gross_kWh_person_day'],d['final_kWh_person_day']]
    fig,ax=plt.subplots(figsize=(7,2.8))
    bars=ax.barh(labels,values,color=[PURPLE,BLUE,GREEN],height=.58)
    ax.bar_label(bars,fmt='%.1f',padding=4)
    ax.set(xlabel='Energy [kWh / person / day]',xlim=(0,max(values)*1.18))
    ax.grid(True,axis='x',alpha=.18)
    finish(fig,'micro-macro',d['source'])


def austria_sankey():
    d=load('05-austria-flow'); nodes={n['id']:n for n in d['nodes']}; links=d['links']
    incoming={key:[] for key in nodes}; outgoing={key:[] for key in nodes}
    for link in links:
        incoming[link['target']].append(link);outgoing[link['source']].append(link)
    scale=9.5/d['gross_kWh_person_day']; gap=.16
    positions={}; centers={}
    for stage in range(5):
        group=[n for n in nodes.values() if n['stage']==stage]
        if stage==4: group=[n for n in group if n['id'].startswith('sector_')]
        if stage==3: group=[n for n in group if n['id'].startswith('final_')]
        if stage==2: group=[n for n in group if n['id'] in ('conversion','own','nonenergy','final')]
        if stage==1: group=[n for n in group if n['id']=='gross']
        if stage==0: group=[n for n in group if n['id'].startswith('primary_')]
        heights={n['id']:sum(l['value'] for l in outgoing[n['id']])*scale for n in group}
        total=sum(heights.values())+gap*max(0,len(group)-1); y=-total/2
        for n in group:
            key=n['id']; h=heights[key]; positions[key]=(y,y+h);centers[key]=y+h/2;y+=h+gap
    def slots(node_id, collection, rank_key):
        items=sorted(collection[node_id],key=rank_key)
        lo,hi=positions[node_id];cursor=lo;result={}
        for link in items:
            width=link['value']*scale
            result[(link['source'],link['target'])]=(cursor,cursor+width);cursor+=width
        return result
    source_order=lambda link: centers.get(link['target'],0)
    target_order=lambda link: centers.get(link['source'],0)
    color_lookup={key:color for key,color in zip(
        [n['id'] for n in nodes.values() if n['stage']==0],
        [BLUE,ORANGE,GREEN,PURPLE,'#CC79A7',GREY])}
    fig,ax=plt.subplots(figsize=(11,5.2))
    for link in links:
        a=link['source'];b=link['target']
        src=slots(a,outgoing,source_order)[(a,b)]
        dst=slots(b,incoming,target_order)[(a,b)]
        x0=nodes[a]['stage']*1.25; x1=nodes[b]['stage']*1.25
        dx=x1-x0; bend=dx*.38; color=color_lookup.get(a,BLUE if not a.startswith('primary_') else GREY)
        vertices=[(x0,src[0]),(x0+bend,src[0]),(x1-bend,dst[0]),(x1,dst[0]),
            (x1,dst[1]),(x1-bend,dst[1]),(x0+bend,src[1]),(x0,src[1]),(x0,src[0])]
        codes=[MplPath.MOVETO,MplPath.CURVE4,MplPath.CURVE4,MplPath.CURVE4,
            MplPath.LINETO,MplPath.CURVE4,MplPath.CURVE4,MplPath.CURVE4,MplPath.CLOSEPOLY]
        ax.add_patch(PathPatch(MplPath(vertices,codes),facecolor=color,edgecolor='none',alpha=.36,zorder=1))
    for key,(lo,hi) in positions.items():
        node=nodes[key];x=node['stage']*1.25
        ax.add_patch(Rectangle((x-.045,lo),.09,hi-lo,facecolor=GREY,edgecolor='white',lw=.5,zorder=3))
        if hi-lo>.30:
            ax.text(x,hi+.10,node['label'],ha='center',va='bottom',fontsize=7,rotation=0,zorder=4)
    ax.set_xlim(-.5,5.5);ax.set_ylim(-5.8,5.8);ax.axis('off')
    for x,label in [(0,'Primary carriers'),(1.25,'Gross inland'),(2.5,'Gross partitions'),(3.75,'Final carriers'),(5,'Final sectors')]:
        ax.text(x,5.3,label,ha='center',va='top',fontsize=9,weight='bold')
    finish(fig,'austria-sankey',d['source']+'; 2025 preliminary, kWh/(person day)')


def solar_chain():
    d=load('07-solar-chain')
    fig,ax=plt.subplots(figsize=(7.6,3.3))
    ax.bar(d['months'],d['monthly_horizontal_kWh_m2'],color=BLUE,width=.75)
    ax.axhline(d['horizontal_kWh_m2_year']/12,color=ORANGE,ls='--',lw=1,
        label=f"annual mean / 12 = {d['horizontal_kWh_m2_year']/12:.1f}")
    ax.set(xticks=d['months'],xlabel='Month',ylabel='Horizontal irradiation [kWh / m² / month]')
    ax.grid(True,axis='y',alpha=.18);ax.legend(frameon=False,fontsize=8)
    finish(fig,'solar-monthly',d['source'])


def pv_trend():
    prices=load('09-pv-prices'); cap=load('09-pv-capacity')
    fig,axes=plt.subplots(1,2,figsize=(9,3.7))
    axes[0].plot(prices['years'],prices['prices'],color=BLUE,lw=2)
    axes[0].set(yscale='log',xlabel='Year',ylabel='Module price [constant 2025 USD / Wp]')
    axes[0].grid(True,which='major',alpha=.18)
    for key,label,color in [('world_PV','World',BLUE),('austria_PV','Austria',ORANGE)]:
        axes[1].plot(cap['years'],np.array(cap[key])/1000,'o-',label=label,color=color)
    axes[1].set(xlabel='Year end',ylabel='Installed solar PV [GW]')
    axes[1].grid(True,alpha=.18);axes[1].legend(frameon=False)
    finish(fig,'pv-price-capacity',prices['source']+'; '+cap['source'])


def land_density():
    d=load('11-area-budget'); corn=d['corn_ethanol']
    labels=['Corn ethanol\n(gross)','Wind\n(scenario)','Solar\n(low)','Solar\n(high)']
    values=[corn['density_W_m2'],2,10,20]
    fig,ax=plt.subplots(figsize=(7,3.5))
    bars=ax.bar(labels,values,color=[ORANGE,GREEN,BLUE,BLUE],width=.65)
    ax.bar_label(bars,fmt='%.2g',padding=3)
    ax.set(ylabel='Average power per land area [W / m²]',yscale='log',ylim=(.15,35))
    ax.grid(True,axis='y',which='major',alpha=.18)
    finish(fig,'land-power-density',d['source']+'; wind/solar densities are stated scenarios')


def true_scale():
    d=load('08-park-and-graz')
    img=plt.imread(ROOT/'slides/photos/weesow-sentinel-same-scale.jpg')
    extent=np.array(d['map_extent_relative_to_park_m'])/1000
    boundary=json.loads((ROOT/'data/ch00/processed/graz-outline-metres.geojson').read_text())
    ring=np.array(boundary['features'][0]['geometry']['coordinates'][0])/1000
    fig,(a,b)=plt.subplots(1,2,figsize=(9,4.7))
    a.imshow(img,extent=extent)
    a.set_title('Weesow-Willmersdorf solar park')
    a.text(.02,.02,'1.64 km² · 187 MWp · 180 GWh/a expected',transform=a.transAxes,
        color='white',fontsize=8,ha='left',va='bottom',bbox=dict(facecolor='#17202A',alpha=.75,edgecolor='none'))
    b.fill(ring[:,0],ring[:,1],color='#D8F0F0',edgecolor=BLUE,lw=.7)
    side=np.sqrt(d['area_for_1_GW_average_km2'])
    cx,cy=ring[:,0].mean(),ring[:,1].mean()
    b.add_patch(Rectangle((cx-side/2,cy-side/2),side,side,facecolor=ORANGE,alpha=.35,edgecolor=ORANGE,lw=1.2))
    b.text(cx,cy,f'{d["area_for_1_GW_average_km2"]:.1f} km²\n1 GW average',ha='center',va='center',fontsize=8,color='#17202A')
    b.set_title('Graz boundary with equal-scale area square')
    for ax in (a,b):ax.set(xlim=(-8,8),ylim=(-8,8),xlabel='East [km]',ylabel='North [km]');ax.set_aspect('equal')
    finish(fig,'true-scale-park-graz',d['source']+'; Contains modified Copernicus Sentinel data 2025; Stadt Graz OGD CC BY 4.0')


def wildlife():
    d=load('14-wildlife-risk'); rows=[r for r in d['annual_estimates'] if r['unit']=='birds/year']
    fig,ax=plt.subplots(figsize=(8,4.6))
    ys=np.arange(len(rows)); low=np.array([float(r['low']) for r in rows]); high=np.array([float(r['high']) for r in rows])
    ax.hlines(ys,low,high,color=BLUE,lw=5,alpha=.8)
    for y,r in zip(ys,rows):
        if r.get('median'):ax.plot(float(r['median']),y,'|',color=ORANGE,markersize=12,mew=2)
        ax.text(float(r['high'])*1.12,y,f"{float(r['low']):.2g}–{float(r['high']):.2g}",va='center',fontsize=8)
    ax.set_yticks(ys,[r['cause'].replace(', collision + electrocution','') for r in rows])
    ax.invert_yaxis();ax.set_xscale('log');ax.set_xlim(5e4,1.3e10)
    ax.set_xlabel('Estimated annual bird deaths [birds / year; United States]')
    ax.grid(True,axis='x',which='major',alpha=.18)
    finish(fig,'bird-mortality',d['source']+'; estimates span different study periods and methods')


def risk_energy():
    d=load('14-energy-deaths'); rows=d['observations']
    fig,ax=plt.subplots(figsize=(7.4,3.6))
    rows=sorted(rows,key=lambda r:r['deaths_per_TWh'])
    ax.barh([r['source_type'] for r in rows],[r['deaths_per_TWh'] for r in rows],color=GREEN)
    ax.set(xscale='log',xlabel='Deaths per TWh of electricity [deaths / TWh; 2021 estimates]')
    ax.grid(True,axis='x',which='major',alpha=.18)
    finish(fig,'energy-deaths-twh',d['source'])


def emissions():
    d=load('15-lifecycle-emissions'); rows=d['observations']
    fig,ax=plt.subplots(figsize=(8,5.2))
    y=np.arange(len(rows))
    for yi,r in zip(y,rows):
        lo=float(r['min_gCO2eq_kWh']); mid=float(r['median_gCO2eq_kWh']); hi=float(r['max_gCO2eq_kWh'])
        ax.hlines(yi,lo,hi,color=GREY,lw=2)
        ax.plot(mid,yi,'o',color=BLUE,markersize=5)
    ax.set_yticks(y,[r['technology'] for r in rows]);ax.invert_yaxis()
    ax.set(xscale='log',xlabel='Lifecycle emissions [g CO₂-eq / kWh electricity]')
    ax.grid(True,axis='x',which='major',alpha=.18)
    finish(fig,'lifecycle-emissions',d['source'],metadata={'Description':d['required_data_notice']})


def build():
    OUT.mkdir(parents=True,exist_ok=True)
    plt.rcParams.update({'font.size':9,'axes.spines.top':False,'axes.spines.right':False,
        'svg.fonttype':'none','axes.labelcolor':'#17202A','text.color':'#17202A',
        'xtick.color':'#17202A','ytick.color':'#17202A'})
    for make in (income_energy,income_levels,energy_boundaries,austria_sankey,solar_chain,pv_trend,land_density,true_scale,wildlife,risk_energy,emissions):make()
    print('Wrote 11 original light-theme Chapter 0 SVGs.')


if __name__=='__main__':build()
