"""Generate original, light-background Chapter 0 SVGs from saved plot data."""
import json
import math
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import font_manager
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


def configure_fonts():
    for font in (ROOT/'fonts').glob('*.otf'):
        font_manager.fontManager.addfont(font)
    plt.rcParams.update({'font.family':['STIX Two Text','STIX Two Math'],
        'mathtext.fontset':'custom', 'mathtext.rm':'STIX Two Text',
        'mathtext.it':'STIX Two Text:italic', 'mathtext.bf':'STIX Two Text:bold'})


def finish(fig,name,source,metadata=None,source_size=7,footer=.065):
    fig.text(.01,.012,'Source: '+source,fontsize=source_size,color=GREY,ha='left',va='bottom',wrap=True)
    fig.tight_layout(rect=(0,footer,1,1))
    fig.savefig(OUT/(name+'.svg'),facecolor='white',metadata=metadata)
    fig.savefig(OUT/(name+'.png'),facecolor='white',dpi=96)
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
    d=load('03-income-levels')
    # One geometry and population scale for all three years, shared by script and slides.
    colours=['#E69F00','#0072B2','#009E73','#CC79A7']  # Okabe–Ito; bands also labelled.
    for year in d['years']:
        rows=[r for r in d['observations'] if r['year']==year]
        fig,ax=plt.subplots(figsize=(6.8,3.8))
        x=np.arange(len(rows)); values=[r['population_billions'] for r in rows]
        bars=ax.bar(x,values,color=colours,width=.68)
        labels=[f"{r['population_billions']:.2f}\n{r['population_share_percent']:.1f}%"
                for r in rows]
        # Labels must not change the axis geometry between years.
        for label in ax.bar_label(bars,labels=labels,padding=4,fontsize=16):
            label.set_in_layout(False)
        ax.set_xticks(x,[r['income_threshold'] for r in rows])
        ax.tick_params(labelsize=16)
        ax.set(ylim=(0,5.5),yticks=[0,1,2,3,4,5])
        ax.set_ylabel('Population [billion]',fontsize=16)
        ax.set_xlabel('Income or consumption\n[2021 PPP USD / person / day]',fontsize=16)
        ax.grid(True,axis='y',alpha=.18)
        ax.set_axisbelow(True)
        finish(fig,f'income-levels-{year}',
            'World Bank PIP · Sep 2026 · global estimates',
            metadata={'Description':f'{year}; '+d['notes']},source_size=10,footer=.09)


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


def electricity_consumption():
    """National accounting boundaries and nested electricity subsets, one scale."""
    d=load('05-austria-flow')
    fig=plt.figure(figsize=(257/25.4,133/25.4))
    ax=fig.add_axes((.245,.43,.735,.51))
    values=[d['gross_kWh_person_day'],d['final_kWh_person_day'],
        d['carriers_kWh_person_day']['Electricity'],d['household_electricity_kWh_person_day']]
    ys=[3,2,1,0]
    colours=[GREY,BLUE,GREEN,PURPLE]
    ax.barh(ys,values,height=.52,color=colours)
    for y,value in zip(ys,values):
        ax.text(value+1.5,y,f'{value:.1f}',va='center',fontsize=18)
    ax.set_yticks(ys,['Primary energy\n(gross inland)','Final energy',
        'of which: electricity','of which: households'],fontsize=16)
    ax.text(36,1,f"{d['electricity_share_of_final_percent']:.1f}% of final energy",
        va='center',fontsize=17,color=GREEN)
    ax.text(23,0,f"{d['household_share_of_electricity_percent']:.1f}% of electricity = "
        f"{d['household_electricity_share_of_final_percent']:.1f}% of final energy",
        va='center',fontsize=16,color=PURPLE)
    ax.set(xlim=(0,125),ylim=(-.55,3.65),xticks=range(0,121,20))
    ax.tick_params(axis='y',length=0,pad=9)
    ax.tick_params(axis='x',labelsize=13)
    ax.spines['left'].set_visible(False)
    ax.grid(True,axis='x',alpha=.14)
    ax.set_axisbelow(True)
    fig.text(.01,.985,'Austria · 2025 preliminary · kWh/(person day)',
        fontsize=16,color=GREY,va='top')
    gap=values[0]-values[1]
    fig.text(.01,.33,f'Primary − final = {gap:.1f}',fontsize=17)
    for x,key,label in [(.01,'conversion_loss_kWh_person_day','net transformation loss'),
        (.34,'own_use_and_transport_losses_kWh_person_day','energy-sector use + transport losses'),
        (.80,'nonenergy_kWh_person_day','non-energy use')]:
        fig.text(x,.255,f"{d[key]:.1f}",fontsize=18,color=ORANGE)
        fig.text(x,.205,label,fontsize=12.5,color=GREY)
    model=d['thermal_example']
    fig.text(.01,.115,f"Thermal plant · assumed efficiency {model['efficiency']:.0%} · no heat recovery",
        fontsize=15,color=GREY)
    fig.text(.01,.035,f"{model['input_kWh']:g} kWh heat → "
        f"{model['electricity_kWh']:g} kWh electricity + "
        f"{model['rejected_heat_kWh']:g} kWh rejected heat",fontsize=19)
    # Fixed geometry shared unchanged by the slide and reference chapter.
    fig.savefig(OUT/'electricity-consumption.svg',facecolor='white',metadata={
        'Description':'Statistics Austria preliminary energy balance 2025, rows 8–13 and 18; '
        'annual-average population. Thermal example: assumed 40% efficiency, EIA definition.'})
    fig.savefig(OUT/'electricity-consumption.png',facecolor='white',dpi=96)
    plt.close(fig)


def austria_sankey_panels(d, threshold=2):
    """Pool final allocations and merge minor carriers without discarding energy.

    The complete published carrier-by-sector matrix remains in the input data.
    Each panel is an accounting balance, not a causal primary-to-sector path.
    """
    original={n['id']:n for n in d['nodes']}
    primary=[dict(l) for l in d['links'] if l['target']=='gross' or l['source']=='gross']
    final=[{**l, 'source':l['target'], 'target':'final'}
           for l in d['links'] if l['source']=='final']
    for node in d['nodes']:
        if node['stage']==4:
            cells=[l for l in d['links'] if l['target']==node['id']]
            final.append({'source':'final', 'target':node['id'],
                'value':sum(l['value'] for l in cells),
                'value_TJ':sum(l['value_TJ'] for l in cells)})
    panels=[]
    for pool,links in [('gross',primary),('final',final)]:
        left={l['source'] for l in links if l['target']==pool}
        right={l['target'] for l in links if l['source']==pool}
        nodes={key:{**original[key], 'stage':0 if key in left else 2}
               for key in left|right}
        nodes[pool]={**original[pool], 'stage':1}
        for side,keys in [('supply',left),('use',right)]:
            small={key for key in keys if sum(l['value'] for l in links
                   if l['source']==key or l['target']==key)<threshold}
            if not small:continue
            other=pool+'_other_'+side
            nodes[other]={'id':other,'label':'Other','stage':0 if side=='supply' else 2}
            for key in small:del nodes[key]
            for link in links:
                for endpoint in ('source','target'):
                    if link[endpoint] in small:link[endpoint]=other
        combined={}
        for link in links:
            key=(link['source'],link['target'])
            if key not in combined:
                combined[key]={**link,'value':0.,'value_TJ':0.}
            for quantity in ('value','value_TJ'):combined[key][quantity]+=link[quantity]
        links=list(combined.values())
        for key,node in nodes.items():
            incoming=sum(l['value'] for l in links if l['target']==key)
            outgoing=sum(l['value'] for l in links if l['source']==key)
            if incoming and outgoing and not math.isclose(incoming,outgoing,abs_tol=1e-8):
                raise ValueError(f'Unbalanced Sankey node: {key}')
            node['value']=max(incoming,outgoing)
        panels.append({'nodes':list(nodes.values()),'links':links})
    return panels


def draw_sankey_panel(ax,panel,total):
    nodes={n['id']:n for n in panel['nodes']};links=panel['links']
    incoming={key:[] for key in nodes}; outgoing={key:[] for key in nodes}
    for link in links:
        incoming[link['target']].append(link);outgoing[link['source']].append(link)
    # One scale in both panels; reserve label space independently of ribbon width.
    scale=1/total;gap=.05
    short={'gross':'Gross inland\nbalance pool','final':'Final energy\nbalance pool',
        'conversion':'Net transformation\nlosses','own':'Energy sector /\ntransport losses',
        'final_35':'Renewable fuels /\ndirect heat'}
    labels={key:short.get(key,n['label'])+f"\n{n['value']:.1f}" for key,n in nodes.items()}
    positions={}; centers={}
    for stage in range(3):
        group=sorted((n for n in nodes.values() if n['stage']==stage),
                     key=lambda n:(-n['value'],n['id']))
        slots_height={n['id']:max(n['value']*scale,
            .16*len(labels[n['id']].splitlines())+.05) for n in group}
        extent=sum(slots_height.values())+gap*max(0,len(group)-1);y=extent/2
        for n in group:
            key=n['id'];h=n['value']*scale;center=y-slots_height[key]/2
            positions[key]=(center-h/2,center+h/2);centers[key]=center
            y-=slots_height[key]+gap
    def slots(node_id, collection, rank_key):
        items=sorted(collection[node_id],key=rank_key)
        lo,hi=positions[node_id];cursor=lo;result={}
        for link in items:
            width=link['value']*scale
            result[(link['source'],link['target'])]=(cursor,cursor+width);cursor+=width
        return result
    source_order=lambda link: centers.get(link['target'],0)
    target_order=lambda link: centers.get(link['source'],0)
    # Okabe–Ito blue; position and direct labels carry all distinctions.
    color='#0072B2'
    for link in links:
        a=link['source'];b=link['target']
        src=slots(a,outgoing,source_order)[(a,b)]
        dst=slots(b,incoming,target_order)[(a,b)]
        x0=nodes[a]['stage'];x1=nodes[b]['stage']
        dx=x1-x0;bend=dx*.38
        vertices=[(x0,src[0]),(x0+bend,src[0]),(x1-bend,dst[0]),(x1,dst[0]),
            (x1,dst[1]),(x1-bend,dst[1]),(x0+bend,src[1]),(x0,src[1]),(x0,src[0])]
        codes=[MplPath.MOVETO,MplPath.CURVE4,MplPath.CURVE4,MplPath.CURVE4,
            MplPath.LINETO,MplPath.CURVE4,MplPath.CURVE4,MplPath.CURVE4,MplPath.CLOSEPOLY]
        ax.add_patch(PathPatch(MplPath(vertices,codes),facecolor=color,edgecolor='none',alpha=.36,zorder=1))
    for key,(lo,hi) in positions.items():
        node=nodes[key];x=node['stage']
        ax.add_patch(Rectangle((x-.025,lo),.05,hi-lo,facecolor=color,
                              edgecolor='white',lw=.5,zorder=3,gid=key))
        label_x=x-.06 if x==0 else x+.06 if x==2 else x
        ax.text(label_x,centers[key],labels[key],ha='right' if x==0 else 'left' if x==2 else 'center',
            va='center',fontsize=12,zorder=4,
            bbox=dict(facecolor='white',edgecolor='none',pad=2))
    ax.set(xlim=(-1.05,3.05),ylim=(-1.65,1.65));ax.axis('off')


def austria_sankey():
    d=load('05-austria-flow')
    fig,axes=plt.subplots(2,1,figsize=(8,10.6))
    for ax,panel,title in zip(axes,austria_sankey_panels(d),[
        'Primary supply and gross inland partitions',
        'Final carriers and use sectors (pooled balance)']):
        draw_sankey_panel(ax,panel,d['gross_kWh_person_day'])
        ax.set_title(title,fontsize=12,pad=12)
    finish(fig,'austria-sankey',
        'Statistics Austria, 2025 preliminary; all values in kWh/(person d).\n'
        'Carriers below 2 grouped as Other; final allocations shown as pooled totals.\n'
        'Both panels use the same flow scale; they show successive energy boundaries.',
        source_size=12,footer=.11)


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
    # CSV/legacy JSON strings must not reach Matplotlib's categorical converter.
    rows=sorted(rows,key=lambda r:float(r['deaths_per_TWh']))
    bars=ax.barh([r['source_type'] for r in rows],
                 [float(r['deaths_per_TWh']) for r in rows],color=GREEN)
    ax.bar_label(bars,labels=[f"{float(r['deaths_per_TWh']):g}" for r in rows],padding=4)
    ax.set(xscale='log',xlabel='Deaths per TWh of electricity [deaths / TWh; 2021 estimates]')
    ax.set_xlim(.01,100)
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



def resource_lifetime_plot(rows, labels, name, xlabel):
    """Shared years scale and geometry for fuel and blanket resource budgets."""
    fig, ax = plt.subplots(figsize=(257/25.4, 83/25.4))
    for y,row in enumerate(rows):
        value = row['static_years']
        if value is None:
            ax.text(.025,y,f"Total unknown; fleet needs {row['fleet_initial_t']/1e6:.1f} Mt",
                    transform=ax.get_yaxis_transform(),va='center',fontsize=17,color='#B55000')
            continue
        colour = '#B55000' if row.get('resource')=='deuterium_seawater' else '#0072B2'
        ax.barh(y,value-1,left=1,height=.48,color=colour)
        label = (f'{value:.0f} years' if value < 1000 else
                 f'{value:,.0f} years'.replace(',',' ') if value < 1e6 else
                 f'{value/1e6:.1f} million years' if value < 1e9 else
                 f'{value/1e9:.0f} billion years')
        if row.get('stock_qualifier') == '>':
            label = '> ' + label
        inside = value > 1e9
        ax.text(value*(.7 if inside else 1.22),y,label,va='center',
                ha='right' if inside else 'left',color='white' if inside else '#17202A',fontsize=17)
    ax.set_yticks(range(len(rows)),labels,fontsize=17)
    ax.set_ylim(len(rows)-.5,-.5)
    ax.set_xscale('log')
    ax.set_xlim(1,1e12)
    ax.set_xticks([1,1e3,1e6,1e9,1e12],['1','1 000','1 million','1 billion','1 trillion'],fontsize=14)
    ax.set_xlabel(xlabel+' · logarithmic scale',fontsize=16)
    ax.grid(axis='x',alpha=.18)
    ax.set_axisbelow(True)
    ax.spines['left'].set_visible(False)
    ax.tick_params(axis='y',length=0)
    fig.subplots_adjust(left=.365,right=.94,bottom=.25,top=.96)
    fig.savefig(OUT/(name+'.svg'),facecolor='white')
    fig.savefig(OUT/(name+'.png'),facecolor='white',dpi=110)
    plt.close(fig)


def fusion_resource_lifetimes():
    data = load('13-fusion-resources')
    rows = data['fuel']
    labels = [f"Lithium · {rows[0]['stock_kg']/1e9:g} Mt reserves",
              'Lithium · seawater inventory','Deuterium · seawater (D–T)']
    resource_lifetime_plot(rows,labels,'fusion-resource-lifetimes',
                           'Stock / annual fuel requirement [years]')


def fusion_blanket_lifetimes():
    data = load('13-fusion-resources')
    rows = data['blanket_lifetimes']
    labels = [f"Lead · {rows[0]['stock_t']/1e6:g} Mt reserves",
              f"Lead · >{rows[1]['stock_t']/1e9:g} Gt resources",
              f"Beryllium · >{rows[2]['stock_t']/1000:g} kt resources"]
    resource_lifetime_plot(rows,labels,'fusion-blanket-lifetimes',
                           'Years after supplying all plants')



def energy_outlook():
    """One comparison plot: literature ranges, observations and fusion timelines."""
    data = load('16-energy-scenarios')
    years = data['years']
    colors = {'Fossils':'#555555', 'Wind + solar':'#A87500',
              'Bioenergy':'#009E73', 'Fission':'#8060A0', 'Other':'#0072B2'}
    styles = {'Fossils':'--', 'Wind + solar':'-', 'Bioenergy':'-.',
              'Fission':':', 'Other':'--'}
    label_y = {'Fossils':27, 'Wind + solar':49, 'Bioenergy':22,
               'Fission':2.7, 'Other':6.7}
    labels = {'Fossils':'Fossils', 'Wind + solar':'Wind + solar',
              'Bioenergy':'Bioenergy', 'Fission':'Fission', 'Other':'Hydro + other'}
    fig, ax = plt.subplots(figsize=(257/25.4,134/25.4))
    fig.subplots_adjust(left=.09,right=.99,bottom=.14,top=.91)

    def endpoint(values, label, color, height):
        ax.plot([2100,2103,2105],[values[-1],height,height],color=color,lw=.8)
        ax.text(2105.5,height,label,color=color,fontsize=13.5,va='center')

    for name, color in colors.items():
        series = data['shares_percent'][name]
        # Ranges for the two contested land-based/variable-renewable groups.
        if name in ('Wind + solar','Bioenergy'):
            ax.fill_between(years,series['p10'],series['p90'],color=color,alpha=.10,lw=0)
        ax.plot(years,series['median'],color=color,ls=styles[name],lw=1.9)
        endpoint(series['median'],labels[name],color,label_y[name])

    policies = data['current_policy_fossils_percent']['median']
    ax.plot(years,policies,color='#777777',ls=(0,(5,3)),lw=1.2)
    endpoint(policies,'Fossils: current policies','#777777',72)

    obs = data['observed']
    obs_groups = {'Fossils':sum(obs['values'][k] for k in ('Coal','Oil','Gas')),
                  'Fission':obs['values']['Nuclear'],
                  'Renewables total':obs['values']['Renewables']}
    for name, value in obs_groups.items():
        ax.plot(obs['year'],100*value/obs['total'],'o',mfc='white',
                mec=colors.get(name,'#222222'),ms=6.5,mew=1.4,zorder=7)
    ax.annotate('Renewables total',xy=(2024,100*96/646),
                xytext=(2028,19),fontsize=11.5,color='#333333',
                arrowprops={'arrowstyle':'-','color':'#333333','lw':.7})

    fusion_color = '#C62828'
    mit = data['fusion_mit']
    cases = mit['cases']
    curve_values = np.array([case['scaled_primary_shares_percent'] for case in cases])
    ax.fill_between(mit['years'],curve_values.min(axis=0),curve_values.max(axis=0),
                    color=fusion_color,alpha=.08,lw=0)
    for case, style in zip(cases, [':','--','-','-.']):
        base = case['cost_2050_USD_kW']==8000
        ax.plot(case['years'],case['scaled_primary_shares_percent'],
                color=fusion_color,ls=style,lw=2.3 if base else .9,zorder=5)
    base = next(case for case in cases if case['cost_2050_USD_kW']==8000)
    endpoint(base['scaled_primary_shares_percent'],'Fusion: MIT',fusion_color,11)

    etm = data['fusion_etm_timeline']
    ax.plot(etm['years'],etm['scaled_primary_shares_percent'],'--o',
            color=fusion_color,lw=1.7,ms=5,mfc='white',mew=1.2,zorder=7)
    endpoint(etm['scaled_primary_shares_percent'],'Fusion: EUROfusion',fusion_color,16.5)
    ax.plot(2100,data['fusion']['scaled_primary_share_percent'],marker='*',ms=16,
            color=fusion_color,mec='white',mew=.6,zorder=8)

    solar = data['solar']
    ax.plot(solar['observation_years'],solar['observed_shares_percent'],
            '-D',color='#D55E00',ms=4,lw=2,zorder=8)
    ax.plot(solar['guide_years'],solar['guide_shares_percent'],
            '--',color='#D55E00',lw=2,zorder=7)
    ax.annotate('PV: 510 GW/year held',xy=(2035,solar['guide_shares_percent'][-1]),
                xytext=(2037,8.2),fontsize=11.5,color='#D55E00',
                arrowprops={'arrowstyle':'-','color':'#D55E00','lw':.8})

    ax.text(.01,1.04,'IPCC 1.5–2°C: medians + 10–90% ranges    Fusion: published cost cases',
            transform=ax.transAxes,fontsize=12.3,color=GREY)
    ax.text(.01,.965,'○ Observed 2024',transform=ax.transAxes,fontsize=12,color=GREY)
    ax.text(.55,.965,'Fusion: 4 MIT cost cases; ○ ETM 2024; ★ ETM 2026',
            transform=ax.transAxes,fontsize=11.5,color=fusion_color,ha='center')
    ax.set_xlim(2020,2135)
    ax.set_ylim(0,86)
    ax.set_xticks([2024,2040,2060,2080,2100])
    ax.set_yticks([0,20,40,60,80],['0%','20%','40%','60%','80%'])
    ax.tick_params(labelsize=14)
    ax.set_ylabel('Share of world primary energy',fontsize=15)
    ax.grid(alpha=.13)
    ax.set_axisbelow(True)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    fig.savefig(OUT/'energy-outlook.svg',facecolor='white')
    fig.savefig(OUT/'energy-outlook.png',facecolor='white',dpi=120)
    plt.close(fig)


def build():
    OUT.mkdir(parents=True,exist_ok=True)
    configure_fonts()
    plt.rcParams.update({'font.size':9,'axes.spines.top':False,'axes.spines.right':False,
        # Outline the bundled STIX glyphs: SVG images cannot inherit page webfonts.
        'svg.fonttype':'path','axes.labelcolor':'#17202A','text.color':'#17202A',
        'xtick.color':'#17202A','ytick.color':'#17202A'})
    for make in (income_energy,income_levels,energy_boundaries,electricity_consumption,austria_sankey,solar_chain,pv_trend,land_density,true_scale,wildlife,risk_energy,emissions,fusion_resource_lifetimes,fusion_blanket_lifetimes,energy_outlook):make()
    print('Wrote original light-theme Chapter 0 SVGs.')


if __name__=='__main__':build()
