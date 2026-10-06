"""Chapter 0: independently derived energy estimates and empirical plot data.

MIT code; original derivations CC BY 4.0. Third-party inputs retain their terms.
Run: python3 derivations/chapters/ch00_energy_context.py
Every physical numerical calculation substitutes SymPy quantities with units.
Python loads records and constructs arrays; it does not supply hidden formulas.
"""
# %% Sources, units and symbols
import csv
import json
import sys
from pathlib import Path
import sympy as sp
from sympy.physics import units as u
from sympy.physics.units import convert_to

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'derivations'))
from si import check, si_unit, same_unit

DATA = ROOT/'data/ch00/processed'
OUT = ROOT/'derivations/build/plotdata'
INPUTS = json.loads((DATA/'inputs.json').read_text())
YEAR = sp.Rational(str(INPUTS['seconds_per_year']['value']))*u.second
KWH = sp.Integer(3600000)*u.joule
UNITS = {'person':1, '1':1, 'J':u.joule, 'degree':sp.pi/180, 's/year':u.second/YEAR,
         'km^2':10**6*u.meter**2, 'MWp':10**6*u.watt, 'MW':10**6*u.watt,
         'GWh/year':10**6*KWH/YEAR, 'W/m^2':u.watt/u.meter**2,
         'kg/m^3':u.kilogram/u.meter**3, 'km^3':10**9*u.meter**3,
         'kg':u.kilogram, 't Li':1000*u.kilogram, 't U':1000*u.kilogram,
         't Li/year':1000*u.kilogram/YEAR,'t U/year':1000*u.kilogram/YEAR,
         'kt U':10**6*u.kilogram,'kt U/year':10**6*u.kilogram/YEAR,
         'Mt':10**9*u.kilogram,'Mt/year':10**9*u.kilogram/YEAR,
         'billion m^3':10**9*u.meter**3,'billion m^3/year':10**9*u.meter**3/YEAR,
         'EJ':10**18*u.joule,'year':YEAR,'GW day/t':10**9*u.watt*u.day/(1000*u.kilogram),
         'kWh/kg':KWH/u.kilogram,'MJ/kg':10**6*u.joule/u.kilogram,
         'kWh/(person day)':KWH/u.day,
         'C':u.coulomb,'u':sp.Rational(INPUTS['atomic_mass']['value'])*u.kilogram,
         'MeV/reaction':10**6*sp.Rational(INPUTS['elementary_charge']['value'])*u.coulomb*u.volt,
         'J/Btu_IT':u.joule, 'EUR/(person year)':1/YEAR, 'MW(e)':10**6*u.watt,
         'reactor/year':1/YEAR,
         'bushel/(acre year)':1/(sp.Rational('4046.8564224')*u.meter**2*YEAR),
         'gal/bushel':sp.Rational('0.003785411784')*u.meter**3,
         'Btu/gal':sp.Rational('1055.05585262')*u.joule/(sp.Rational('0.003785411784')*u.meter**3)}


def v(key):
    """Input magnitude as an exact decimal rational."""
    return sp.Rational(str(INPUTS[key]['value']))


def quantity(key):
    return v(key)*UNITS[INPUTS[key]['unit']]


def number(expression, target=1):
    # Numerical data are evaluated numerically; retain exact symbolic formulas above.
    normalized = sp.simplify(convert_to((expression/target).evalf(), [u.kilogram,u.meter,u.second,u.coulomb]))
    assert not normalized.atoms(u.Quantity), f'Uncancelled units: {normalized}'
    return float(normalized.evalf())


def load(name):
    return json.loads((DATA/name).read_text())


def csv_output(name, rows):
    with (DATA/name).open('w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


# %% Average power, area, finite stocks, continuously growing demand
E, N, T, P, q, A, R, D, g, t = sp.symbols('E N T P q A R D g t', positive=True)
power_per_person = sp.solve(sp.Eq(E, N*P*T), P)[0]
area_per_person = sp.solve(sp.Eq(P, q*A), A)[0]
stock_years = sp.solve(sp.Eq(R, D*T), T)[0]
consumed = sp.integrate(D*sp.exp(g*t), (t, 0, T))
growth_solution = sp.solve(sp.Eq(consumed, R), T)[0]
# Recombine solver-expanded logs before inserting dimensionful quantities.
growth_lifetime = sp.logcombine(growth_solution*g, force=True)/g
zero_growth_lifetime = sp.limit(growth_lifetime, g, 0)
r, interval = sp.symbols('r Delta_t', positive=True)
continuous_growth_from_discrete = sp.solve(sp.Eq(1+r,sp.exp(g*interval)),g)[0]
stock_power = sp.solve(sp.Eq(E, N*P*T), P)[0]
FORMULAS = {
    'average_power_per_person': power_per_person, 'area_per_person':area_per_person,
    'static_stock_horizon':stock_years, 'integrated_growing_demand':consumed,
    'growth_lifetime':growth_lifetime, 'zero_growth_limit':zero_growth_lifetime,
    'continuous_growth_from_discrete':continuous_growth_from_discrete,
    'finite_stock_power_per_person':stock_power}
GDP, intensity, CF, unit_power, count = sp.symbols('GDP I CF P_unit n_unit', positive=True)
energy_intensity = sp.solve(sp.Eq(E,N*T*GDP*intensity),intensity)[0]
economic_power = sp.solve(sp.Eq(P,GDP*intensity),P)[0]
capacity_factor = sp.solve(sp.Eq(E,P*T*CF),CF)[0]
ground_power_density = sp.solve(sp.Eq(E,q*A*T),q)[0]
deployment_count = sp.solve(sp.Eq(P,count*unit_power*CF),count)[0]
deployment_rate = deployment_count/T
nameplate_for_mean = sp.solve(sp.Eq(P,CF*unit_power),unit_power)[0]
fuel_heat, consumption_per_distance, distance_rate = sp.symbols('H_fuel C_distance v_distance',positive=True)
car_power = sp.solve(sp.Eq(P,fuel_heat*consumption_per_distance*distance_rate),P)[0]
crop_yield, ethanol_rate, ethanol_heat = sp.symbols('Y_crop r_ethanol H_ethanol', positive=True)
biofuel_density = sp.solve(sp.Eq(q,crop_yield*ethanol_rate*ethanol_heat),q)[0]
FORMULAS.update(energy_intensity=energy_intensity,economic_power=economic_power,capacity_factor=capacity_factor,
    ground_power_density=ground_power_density,deployment_count=deployment_count,deployment_rate=deployment_rate,
    nameplate_for_mean=nameplate_for_mean,car_power=car_power,biofuel_power_density=biofuel_density)
DIMENSIONS = {E:u.joule,N:1,T:u.second,P:u.watt,q:u.watt/u.meter**2,
              A:u.meter**2,R:u.kilogram,D:u.kilogram/u.second,g:1/u.second,t:u.second}
DIMENSIONS.update({GDP:1/u.second,intensity:u.joule,CF:1,unit_power:u.watt,count:1})
DIMENSIONS.update({r:1,interval:u.second})
DIMENSIONS.update({fuel_heat:u.joule/u.meter**3,consumption_per_distance:u.meter**2,
                   distance_rate:u.meter/u.second})
DIMENSIONS.update({crop_yield:1/(u.meter**2*u.second),ethanol_rate:u.meter**3,
                   ethanol_heat:u.joule/u.meter**3})
check(power_per_person, E/(N*T), u.watt, DIMENSIONS)
check(area_per_person, P/q, u.meter**2, DIMENSIONS)
check(stock_years, R/D, u.second, DIMENSIONS)
check(growth_lifetime, sp.log(1+g*R/D)/g, u.second, DIMENSIONS)
assert sp.simplify(consumed.subs(T, growth_lifetime)-R) == 0
check(capacity_factor,E/(P*T),1,DIMENSIONS)
check(ground_power_density,E/(A*T),u.watt/u.meter**2,DIMENSIONS)
check(deployment_count,P/(unit_power*CF),1,DIMENSIONS)
check(deployment_rate,P/(unit_power*CF*T),1/u.second,DIMENSIONS)
check(nameplate_for_mean,P/CF,u.watt,DIMENSIONS)
check(car_power,fuel_heat*consumption_per_distance*distance_rate,u.watt,DIMENSIONS)
check(continuous_growth_from_discrete,sp.log(1+r)/interval,1/u.second,DIMENSIONS)
check(energy_intensity,E/(N*T*GDP),u.joule,DIMENSIONS)
check(economic_power,GDP*intensity,u.watt,DIMENSIONS)
check(biofuel_density,crop_yield*ethanol_rate*ethanol_heat,u.watt/u.meter**2,DIMENSIONS)


def biofuel():
    density = biofuel_density.subs({crop_yield:quantity('corn_yield'),
        ethanol_rate:quantity('ethanol_yield'),ethanol_heat:quantity('ethanol_lhv')})
    return number(density,u.watt/u.meter**2)


def daily(tj, population):
    return number(power_per_person.subs({E:sp.Rational(str(tj))*10**12*u.joule,
                  N:sp.Rational(str(population)),T:YEAR}), KWH/u.day)


def horizon(reserve, production):
    return number(stock_years.subs({R:reserve,D:production}), YEAR)


# %% PV chain: geometry derived, empirical annual climate used once
h, phi, delta = sp.symbols('h phi delta', real=True)
h0 = sp.acos(-sp.tan(phi)*sp.tan(delta))
projection = sp.sin(phi)*sp.sin(delta)+sp.cos(phi)*sp.cos(delta)*sp.cos(h)
daily_geometry = sp.integrate(projection, (h,-h0,h0))/(2*sp.pi)
night_factor = sp.integrate(sp.cos(h), (h,-sp.pi/2,sp.pi/2))/(2*sp.pi)
latitude_factor = sp.cos(phi)
H, H_i, efficiency, pr, peak, Y = sp.symbols('H H_i eta PR P_STC Y', positive=True)
annual_module_energy = H_i*A*efficiency*pr
module_peak = peak*A*efficiency
specific_yield = sp.cancel(annual_module_energy/module_peak)
performance_ratio = sp.solve(sp.Eq(Y,specific_yield),pr)[0]
delivered_module_density = sp.cancel(annual_module_energy/(A*T))
f_night, f_latitude, f_season, f_weather, f_tilt = sp.symbols(
    'f_night f_latitude f_season f_weather f_tilt', positive=True)
solar_factor_chain = peak*f_night*f_latitude*f_season*f_weather*f_tilt*efficiency*pr
FORMULAS.update(daily_geometry=daily_geometry, equinox_daynight=night_factor,
    equinox_latitude=latitude_factor, module_annual_energy=annual_module_energy,
    module_STC_power=module_peak, specific_yield=specific_yield,
    performance_ratio=performance_ratio, delivered_module_density=delivered_module_density,
    solar_factor_chain=solar_factor_chain)
DIMENSIONS.update({H:u.joule/u.meter**2,H_i:u.joule/u.meter**2,
                   efficiency:1,pr:1,peak:u.watt/u.meter**2,Y:u.second})
DIMENSIONS.update({s:1 for s in (f_night,f_latitude,f_season,f_weather,f_tilt)})
check(delivered_module_density,H_i*efficiency*pr/T,u.watt/u.meter**2,DIMENSIONS)
assert same_unit(si_unit(solar_factor_chain,DIMENSIONS),u.watt/u.meter**2)


def solar():
    raw = json.loads((ROOT/'data/ch00/raw/pvgis_graz_horizontal.json').read_text())
    records = raw['outputs']['monthly']
    climatology = [number(sum(sp.Rational(str(r['H(h)_m'])) for r in records if r['month']==m)/19)
                   for m in range(1,13)]
    horizontal = sum(sp.Rational(str(x)) for x in climatology)*KWH/u.meter**2
    totals = json.loads((ROOT/'data/ch00/raw/pvgis_graz.json').read_text())['outputs']['totals']['fixed']
    inclined = sp.Rational(str(totals['H(i)_y']))*KWH/u.meter**2
    yearly_yield = sp.Rational(str(totals['E_y']))*KWH/(1000*u.watt)
    ratio = performance_ratio.subs({Y:yearly_yield,peak:quantity('solar_noon'),H_i:inclined})
    density = delivered_module_density.subs({H_i:inclined,efficiency:quantity('pv_efficiency'),pr:ratio,T:YEAR})
    # Twelve equal-duration midpoint samples of a simple annual declination model.
    ideal = sum(daily_geometry.subs({phi:quantity('graz_latitude'),
        delta:quantity('obliquity')*sp.sin(2*sp.pi*(sp.Rational(365)*(sp.Rational(k,12)+sp.Rational(1,24))-80)/365)}).evalf()
        for k in range(12))/12
    factors = {'day_night':number(night_factor),'latitude':number(latitude_factor.subs(phi,quantity('graz_latitude'))),
        'season':number(ideal/(night_factor*latitude_factor.subs(phi,quantity('graz_latitude')))),
        'atmosphere_weather_residual':number(horizontal/YEAR/(quantity('solar_noon')*ideal)),
        'tilt_gain':number(inclined/horizontal),'module_efficiency':number(quantity('pv_efficiency')),
        'performance_ratio':number(ratio)}
    chain_values = [night_factor,latitude_factor.subs(phi,quantity('graz_latitude')),
        ideal/(night_factor*latitude_factor.subs(phi,quantity('graz_latitude'))),
        horizontal/YEAR/(quantity('solar_noon')*ideal),inclined/horizontal,
        quantity('pv_efficiency'),ratio]
    cumulative = quantity('solar_noon')
    stages = [{'stage':'noon_peak','W_m2':number(cumulative,u.watt/u.meter**2)}]
    for name,factor in zip(factors,chain_values):
        cumulative *= factor
        stages.append({'stage':name,'W_m2':number(cumulative,u.watt/u.meter**2)})
    chain_result = solar_factor_chain.subs(dict(zip(
        [peak,f_night,f_latitude,f_season,f_weather,f_tilt,efficiency,pr],
        [quantity('solar_noon'),*chain_values])))
    assert abs(number(chain_result-density,u.watt/u.meter**2)) < 1e-8
    return {'horizontal_kWh_m2_year':number(horizontal,KWH/u.meter**2),
        'horizontal_W_m2':number(horizontal/YEAR,u.watt/u.meter**2),
        'inclined_kWh_m2_year':number(inclined,KWH/u.meter**2),
        'specific_yield_kWh_kWp_year':totals['E_y'], 'module_W_m2':number(density,u.watt/u.meter**2),
        'monthly_horizontal_kWh_m2':climatology,'months':list(range(1,13)), 'factors':factors,
        'stages':stages,'pvgis_loss_percent':{k:totals[k] for k in ['l_aoi','l_spec','l_tg','l_total']},
        'year_range':[2005,2023],'latitude_deg':float(v('graz_latitude')),'tilt_deg':35,'system_loss_percent':14,
        'notes':'Satellite-derived climatology and PVGIS model, not a ground-station measurement. Weather residual is calibrated and includes atmosphere/horizon, not an independently measured weather factor. Geometry toy model uses 12 equal-duration midpoint samples. No factor is applied twice.'}


# %% Fission: burnup, electrical conversion and enrichment mass balance
B, eta, M, F, W, xp, xf, xt = sp.symbols('B eta M F W x_p x_f x_t', positive=True)
enriched_fuel = sp.solve(sp.Eq(P*T,eta*B*M),M)[0]
enrichment = sp.solve([sp.Eq(F,M+W),sp.Eq(xf*F,xp*M+xt*W)],(F,W))
FORMULAS.update(enriched_uranium=enriched_fuel,natural_uranium=enrichment[F],tails_uranium=enrichment[W])
DIMENSIONS.update({B:u.joule/u.kilogram,eta:1,M:u.kilogram,F:u.kilogram,W:u.kilogram,xp:1,xf:1,xt:1})
check(enriched_fuel,P*T/(eta*B),u.kilogram,DIMENSIONS)
check(enrichment[F],M*(xp-xt)/(xf-xt),u.kilogram,DIMENSIONS)


def fission(power=10**9*u.watt):
    product = enriched_fuel.subs({P:power,T:YEAR,eta:quantity('nuclear_efficiency'),B:quantity('nuclear_burnup')})
    masses = {k:expr.subs({M:product,xp:quantity('enrichment_product'),xf:quantity('enrichment_feed'),xt:quantity('enrichment_tails')})
              for k,expr in enrichment.items()}
    return {'enriched_t_U':number(product,1000*u.kilogram),
            'natural_t_U':number(masses[F],1000*u.kilogram),'tails_t_U':number(masses[W],1000*u.kilogram),
            'natural_specific_thermal_J_kg':number(power*YEAR/(masses[F]*quantity('nuclear_efficiency')),u.joule/u.kilogram)}


# %% Fusion, coal and geophysical inventories
Q, mD, mT, calorific, rho, fw, watermass, ratioD, volume = sp.symbols('Q m_D m_T q_coal rho f_water m_water r_DH V', positive=True)
reaction_count = sp.solve(sp.Eq(E,sp.Symbol('n')*Q),sp.Symbol('n'))[0]
fusion_fuel = reaction_count*(mD+mT)
coal_mass = sp.solve(sp.Eq(E,calorific*M),M)[0]
deuterium_concentration = rho*fw*2*mD/watermass*ratioD/(1+ratioD)
deuterium_inventory = deuterium_concentration*volume
FORMULAS.update(reaction_count=reaction_count, fusion_fuel=fusion_fuel,coal_mass=coal_mass,
    deuterium_concentration=deuterium_concentration,deuterium_inventory=deuterium_inventory)
DIMENSIONS.update({Q:u.joule,mD:u.kilogram,mT:u.kilogram,calorific:u.joule/u.kilogram,
    rho:u.kilogram/u.meter**3,fw:1,watermass:u.kilogram,ratioD:1,volume:u.meter**3})
check(fusion_fuel,E*(mD+mT)/Q,u.kilogram,DIMENSIONS)
check(deuterium_inventory,deuterium_concentration*volume,u.kilogram,DIMENSIONS)


def fusion():
    masses = {mD:v('deuterium_atomic_mass')*quantity('atomic_mass'),
              mT:v('tritium_atomic_mass')*quantity('atomic_mass')}
    energy = 10**9*u.watt*YEAR
    n = reaction_count.subs({E:energy,Q:quantity('dt_energy')})
    concentration = deuterium_concentration.subs({rho:quantity('seawater_density'),fw:quantity('seawater_water_fraction'),
        mD:masses[mD],watermass:v('water_molecular_mass')*quantity('atomic_mass'),ratioD:quantity('deuterium_hydrogen_ratio')})
    inventory = concentration*quantity('ocean_volume')
    return {'Q_MeV':float(v('dt_energy')),'Q_J':number(quantity('dt_energy'),u.joule),
        'reactions_per_GW_fusion_year':number(n),'deuterium_kg':number(n*masses[mD],u.kilogram),
        'tritium_kg':number(n*masses[mT],u.kilogram),'fuel_kg':number(n*(masses[mD]+masses[mT]),u.kilogram),
        'coal_kg':number(coal_mass.subs({E:energy,calorific:quantity('coal_heat')}),u.kilogram),
        'deuterium_g_m3':number(concentration,sp.Rational(1,1000)*u.kilogram/u.meter**3),
        'ocean_deuterium_kg':number(inventory,u.kilogram),
        'ocean_deuterium_kg_per_person':number(inventory/quantity('world_population_2025'),u.kilogram),
        'lithium_kg_per_person':number(quantity('lithium_reserves')/quantity('world_population_2025'),u.kilogram),
        'inventory_population':float(v('world_population_2025')),'inventory_population_year':2025}


# %% Balance pools preserve published totals; no invented primary-to-sector paths
def austria_flow():
    balance = load('austria-balance.json')
    rows, n = balance['rows'], balance['population']
    def tj(row, col=37): return sp.Rational(str(rows[str(row)][col]))
    primary_columns = {'Coal':32,'Oil':33,'Gas':34,'Renewables':35,'Waste':36,'Net electricity imports':31}
    final_columns = {'Coal':32,'Oil products':33,'Gas':34,'Renewable fuels / direct heat':35,
                     'Waste':36,'District heat':27,'Electricity':31}
    sectors = {'Industry':14,'Transport':15,'Services':17,'Households':18,'Agriculture':19}
    nodes, links = [], []
    def node(key, label, stage):
        if not any(x['id']==key for x in nodes): nodes.append({'id':key,'label':label,'stage':stage})
        return key
    def link(a, b, value):
        if value != 0: links.append({'source':a,'target':b,'value_TJ':float(value),'value':daily(value,n)})
    primary = node('gross','Gross inland balance pool',1)
    final = node('final','Final energy balance pool',2)
    for label,col in primary_columns.items():
        link(node('primary_'+str(col),label,0),primary,tj(8,col))
    for key,label,value in [('conversion','Net transformation losses',tj(9)-tj(10)),
                            ('own','Energy sector / transport losses',tj(11)),
                            ('nonenergy','Non-energy uses',tj(12))]:
        link(primary,node(key,label,2),value)
    link(primary,final,tj(13))
    for label,col in final_columns.items():
        carrier = node('final_'+str(col),label,3)
        link(final,carrier,tj(13,col))
        for sector,row in sectors.items():
            link(carrier,node('sector_'+str(row),sector,4),tj(row,col))
    gross, end = daily(tj(8),n), daily(tj(13),n)
    return {'year':2025,'status':'preliminary','population':n,'nodes':nodes,'links':links,
        'unit':'kWh/(person day)','gross_TJ':float(tj(8)),'final_TJ':float(tj(13)),
        'gross_kWh_person_day':gross,'final_kWh_person_day':end,
        'conversion_loss_kWh_person_day':daily(tj(9)-tj(10),n),
        'own_use_and_transport_losses_kWh_person_day':daily(tj(11),n),
        'nonenergy_kWh_person_day':daily(tj(12),n),
        'sectors_kWh_person_day':{s:daily(tj(row),n) for s,row in sectors.items()},
        'carriers_kWh_person_day':{s:daily(tj(13,col),n) for s,col in final_columns.items()},
        'notes':'Aggregated balance pools: primary inputs cannot be traced causally to final sectors. Actual published final-carrier × sector cells are retained. Row 16 is an aggregate and is not added again. Conversion losses are net input minus output, not all gross minus final.'}


def resources():
    records = []
    for name in ['hardcoal','lignite','oil','gas','uranium_lowcost']:
        production = 'uranium_production' if name=='uranium_lowcost' else name+'_production'
        record = {'resource':name,'stock':float(v(name+'_stock')),'stock_unit':INPUTS[name+'_stock']['unit'],
            'production':float(v(production)),'production_unit':INPUTS[production]['unit'],'year':2024,
            'static_years':horizon(quantity(name+'_stock'),quantity(production)),
            'energy_EJ':float(v(name+'_stock_energy')),
            'power_W_person_for_1000_years':number(stock_power.subs({E:quantity(name+'_stock_energy'),
                N:quantity('world_population'),T:quantity('sustainable_horizon')}),u.watt),
            'source':'bgr','licence_status':'Free numeric data re-plotted with attribution per lecturer policy; not represented as CC'}
        records.append(record)
    coal_stock = quantity('hardcoal_stock')+quantity('lignite_stock')
    coal_prod = quantity('hardcoal_production')+quantity('lignite_production')
    coal_energy = quantity('hardcoal_stock_energy')+quantity('lignite_stock_energy')
    records.append({'resource':'coal_combined','static_years':horizon(coal_stock,coal_prod),
        'stock':number(coal_stock,10**9*u.kilogram),'stock_unit':'Mt','production':number(coal_prod,10**9*u.kilogram/YEAR),
        'production_unit':'Mt/year','year':2024,'energy_EJ':number(coal_energy,10**18*u.joule),
        'power_W_person_for_1000_years':number(coal_energy/(quantity('world_population')*quantity('sustainable_horizon')),u.watt),
        'source':'bgr','licence_status':'Attributed numerical-data reuse per lecturer policy; coal mass R/P is not an energy-weighted R/P.'})
    fission_energy = quantity('uranium_identified')*sp.Rational(str(fission()['natural_specific_thermal_J_kg']))*u.joule/u.kilogram
    records.append({'resource':'uranium_identified_below_260_USD_kg','stock':float(v('uranium_identified')),
        'stock_unit':'t U','production':float(v('uranium_production_2023')),'production_unit':'t U/year',
        'year':'resources at 2023-01-01 / production 2023','static_years':horizon(quantity('uranium_identified'),quantity('uranium_production_2023')),
        'power_W_person_for_1000_years':number(fission_energy/(quantity('world_population')*quantity('sustainable_horizon')),u.watt),
        'source':'redbook + wna_fuel','licence_status':'CC BY 4.0 Red Book; independently derived cycle model',
        'notes':'Identified recoverable resources RAR+inferred, not proven reserves. Thermal once-through power; multiply by 0.33 for electricity.'})
    growth = [sp.Rational(k,1000) for k in range(31)]
    for record in records:
        tau = sp.Rational(str(record['static_years']))*YEAR
        record['growth_continuous_percent_year'] = [number(x*100) for x in growth]
        record['growth_lifetime_years'] = [number(tau if x==0 else growth_lifetime.subs({R:tau,D:1,g:x/YEAR}),YEAR) for x in growth]
    return records


def historical_deployment():
    history = json.loads((ROOT/'data/ch00/raw/iaea-history-1954-2024.json').read_text())['rows']
    grid = sp.Max(*(sp.Integer(r['grid_connections']) for r in history))
    starts = sp.Max(*(sp.Integer(r['construction_starts']) for r in history))
    capacity = sp.Max(*(sp.Integer(r['grid_MWe']) for r in history))
    return {'coverage':[1954,2024], 'grid_peak_units_per_year':int(grid),
        'grid_peak_years':[r['year'] for r in history if r['grid_connections']==grid],
        'construction_peak_units_per_year':int(starts),
        'construction_peak_years':[r['year'] for r in history if r['construction_starts']==starts],
        'grid_capacity_peak_GWe_per_year':number(capacity*10**6*u.watt,10**9*u.watt),
        'grid_capacity_peak_years':[r['year'] for r in history if r['grid_MWe']==capacity],
        'grid_connections_2024':history[-1]['grid_connections'],
        'grid_capacity_2024_GWe':number(sp.Integer(history[-1]['grid_MWe'])*10**6*u.watt,10**9*u.watt)}


def build():
    OUT.mkdir(parents=True, exist_ok=True)
    results = {}
    def emit(name, page, data, source, status='cleared'):
        record = {'page':page,**data,'source':source,'licence_status':status}
        (OUT/(name+'.json')).write_text(json.dumps(record,indent=2,ensure_ascii=False)+'\n')
        results[name] = record
        return record
    photos = load('photos.json')
    emit('01-earth-at-night',1,{'photos':[p for p in photos if p['file']=='earth-at-night-2016.jpg']},'NASA Earth Observatory, Black Marble 2016; public domain.')
    scatter = []
    for row in csv.DictReader((DATA/'energy-gdp-input.csv').open()):
        energy = sp.Rational(row['primary_energy_QBTU'])*10**15*quantity('btu_IT')
        power = power_per_person.subs({E:energy,N:sp.Rational(row['population']),T:YEAR})
        scatter.append({'iso3':row['iso3'],'country':row['country'],'year':2024,
            'x':float(row['gdp_ppp_per_person_2021_international_dollar']), 'y':number(power,KWH/u.day),
            'population':int(row['population']),'energy_kWh_person_year':number(energy/sp.Rational(row['population']),KWH)})
    emit('02-energy-gdp',2,{'observations':scatter,'units':{'x':'constant 2021 international dollar/(person year)',
        'y':'kWh/(person day)','bubble_area':'person'},'bubble_rule':'Marker area, not radius, proportional to population.',
        'notes':'All 188 EIA countries/economies with positive matching 2024 WDI GDP PPP and population. 41 EIA country records excluded with reasons in processed/energy-gdp-exclusions.json. EIA primary-energy accounting differs from Austria gross inland consumption; 365-day normalization even for leap years.'},
        'EIA International annual primary energy consumption, 2024 (public domain); World Bank WDI GDP PPP NY.GDP.PCAP.PP.KD and population SP.POP.TOTL, 2024 (CC BY 4.0). Accessed 2026-10-06.')
    income_levels = [dict(r) for r in csv.DictReader((DATA/'income-levels-2017.csv').open())]
    emit('03-income-levels',3,{'observations':income_levels,
        'income_unit':'2011 PPP USD/(person day)','population_unit':'billion people','year':2017,
        'notes':'Rounded Gapminder estimates use a PovcalNet 2013 survey base extended to 2017; not a current survey or precise census.'},
        'Gapminder Factfulness notes p.32 and Income Levels; CC BY 4.0. Original plot.')
    access = load('access.json')
    emit('03-access-and-dollarstreet',3,{'access':[next(r for r in access if r['series']=='electricity')],
        'photos':[p for p in photos if p['file'].startswith('dollarstreet')],
        'notes':'Dollar Street PPP monthly amounts are per equivalent adult, not whole-household totals. Global washing-machine, car and refrigerator ownership shares are not included because a comparable sourced series was not verified. Clean-cooking figures are excluded: the WDI indicator source note specifies CC BY-NC 3.0 IGO.'},
        'World Bank WDI EG.ELC.ACCS.ZS (latest world observation, CC BY 4.0); Gapminder Dollar Street, individual photographers, CC BY 4.0.')
    land = [dict(r) for r in csv.DictReader((DATA/'land-use.csv').open())]
    emit('03-land-use',3,{'observations':land,'unit':'ha/person','year':2023,
        'notes':'Arable land is FAO/WDI cropland under temporary crops, temporary meadows, kitchen gardens and temporary fallow; cropland includes arable plus permanent crops under HYDE. The series differ in definition and source method; do not add them.'},
        'FAO via World Bank WDI (CC BY 4.0); PBL HYDE 3.5 via OWID (OWID processing CC BY 4.0; source credited; no standalone source licence asserted).')
    flow = austria_flow()
    legacy = load('legacy-estimates.json')
    total = number(sum(sp.Integer(x) for x in legacy['components'].values()))
    gross_annual = sp.Rational(str(flow['gross_TJ']))*10**12*u.joule/quantity('austria_population')
    intensity_value = number(energy_intensity.subs({E:gross_annual,N:1,T:YEAR,GDP:quantity('austria_gdp')}),KWH)
    emit('04-micro-macro',4,{'legacy_components':legacy['components'],'legacy_total':total,
        'unit':'kWh/(person day)','legacy_GDP_EUR_person_year':legacy['gdp_EUR_per_person_year'],
        'legacy_intensity_kWh_EUR':legacy['intensity_kWh_per_EUR'],
        'legacy_GDP_crosscheck_kWh_person_day':number(economic_power.subs({
            GDP:sp.Integer(legacy['gdp_EUR_per_person_year'])/YEAR,
            intensity:sp.Integer(legacy['intensity_kWh_per_EUR'])*KWH}),KWH/u.day),
        'legacy_car_arithmetic_kWh_person_day':number(car_power.subs({
            fuel_heat:sp.Integer(legacy['car_example']['kWh_per_litre'])*KWH/u.liter,
            consumption_per_distance:sp.Integer(legacy['car_example']['litres_per_100km'])*u.liter/(100000*u.meter),
            distance_rate:sp.Integer(legacy['car_example']['km_per_day'])*1000*u.meter/u.day}),KWH/u.day),
        'gross_kWh_person_day':flow['gross_kWh_person_day'],'final_kWh_person_day':flow['final_kWh_person_day'],
        'gross_W_person':number(gross_annual/YEAR,u.watt),
        'final_W_person':number(sp.Rational(str(flow['final_TJ']))*10**12*u.joule/(quantity('austria_population')*YEAR),u.watt),
        'gross_GW_average':number(sp.Rational(str(flow['gross_TJ']))*10**12*u.joule/YEAR,10**9*u.watt),
        'final_GW_average':number(sp.Rational(str(flow['final_TJ']))*10**12*u.joule/YEAR,10**9*u.watt),
        'population':flow['population'],'GDP_EUR_person_year':float(v('austria_gdp')),
        'derived_gross_intensity_kWh_EUR':intensity_value,
        'notes':'GDP × intensity from the same energy balance is an accounting identity, not an independent validation. Handwritten 120 is a bottom-up estimate; car example arithmetic gives 15, while its budget line rounds to 20. Different accounting boundaries prevent interpreting differences as estimation error alone.'},
        'Chris, 2025 handwritten Chapter00_Intro.pdf p.10; Statistics Austria preliminary 2025 Balance rows 8/13 and annual-average population; World Bank 2025 GDP in current Austrian EUR.',
        'Statistics Austria custom attributed-reuse terms accepted for original data figures; not represented as CC.')
    emit('05-austria-flow',5,flow,'Statistics Austria preliminary energy balance 2025, Balance rows 8–19; author aggregation and unit conversion.',
         'Statistics Austria custom attributed-reuse terms accepted for original data figures; not represented as CC.')
    csv_output('austria-sankey-nodes.csv',flow['nodes'])
    csv_output('austria-sankey-links.csv',[{'source':r['source'],'target':r['target'],
        'energy_TJ':r['value_TJ'],'energy_kWh_person_day':r['value'],'year':2025,
        'source_key':'stat_balance + stat_population'} for r in flow['links']])
    resource_records = resources()
    csv_output('resource-lifetimes.csv',[{k:r[k] for k in ['resource','stock','stock_unit','production','production_unit',
        'year','static_years','power_W_person_for_1000_years','source','licence_status']} for r in resource_records])
    legacy_power = {s:number(quantity('legacy_'+s+'_stock')*quantity('legacy_'+s+'_heat')/
                   (quantity('legacy_world_population')*quantity('sustainable_horizon')),u.watt) for s in ['coal','uranium']}
    legacy_demand_lifetime = {s:horizon(quantity('legacy_'+s+'_stock')*quantity('legacy_'+s+'_heat'),
        quantity('legacy_world_population')*quantity('legacy_daily_demand')) for s in ['coal','uranium']}
    emit('06-resource-lifetimes',6,{'resources':resource_records,'legacy_1000_years_W_person':legacy_power,
        'legacy_lifetime_at_100_kWh_person_day_years':legacy_demand_lifetime,
        'legacy_world_population':1e10,'modern_normalization_population':float(v('world_population')),
        'notes':'Static R/P and prescribed-growth exhaustion are stock models, not forecasts. Continuous g differs from a discrete annual rate r: g=ln(1+r). BGR low-cost uranium RAR and Red Book broad identified resources are not interchangeable. Old oil/gas handwriting supplies qualitative lifetimes but no legible separate 1000-year power estimates.'},
        'BGR Energiedaten 2025 (data 2024); IAEA/NEA Uranium 2024 (published 2025, CC BY 4.0); Chris handwritten pp.14/29; own stock calculations.',
        'BGR attributed numerical-data reuse per lecturer policy; Red Book CC BY 4.0; legacy own handwriting.')
    sol = solar()
    csv_output('graz-monthly-horizontal.csv',[{'month':m,'irradiation_kWh_m2':v,'year_range':'2005–2023',
        'source_key':'pvgis'} for m,v in zip(sol['months'],sol['monthly_horizontal_kWh_m2'])])
    emit('07-solar-chain',7,sol,'EU JRC PVGIS 5.3, SARAH3/ERA5 2005–2023; Graz 47.0707°N, 15.4395°E; 35° south, c-Si 1 kWp, 14% system loss; own SymPy factorization.',
        'PVGIS free reuse with attribution; source terms are not described as a CC licence.')
    geo = load('geography.json')
    park_density = ground_power_density.subs({E:quantity('park_annual_energy')*YEAR,A:quantity('park_area'),T:YEAR})
    park_cf = capacity_factor.subs({E:quantity('park_annual_energy')*YEAR,P:quantity('park_peak'),T:YEAR})
    park_area_needed = area_per_person.subs({P:10**9*u.watt,q:park_density})
    emit('08-park-and-graz',8,{**geo,'park_area_km2':float(v('park_area')),'peak_MWp':float(v('park_peak')),
        'expected_GWh_year':float(v('park_annual_energy')),'ground_W_m2':number(park_density,u.watt/u.meter**2),
        'capacity_factor_expected':number(park_cf),
        'area_for_1_GW_average_km2':number(park_area_needed,10**6*u.meter**2),
        'peak_GWp_for_1_GW_average':number(nameplate_for_mean.subs({P:10**9*u.watt,CF:park_cf}),10**9*u.watt),
        'park_equivalents_for_1_GW_average':number(park_area_needed/quantity('park_area')),
        'fraction_of_Graz_geometry_for_1_GW_average':number(park_area_needed/(sp.Rational(str(geo['graz_projected_area_km2']))*10**6*u.meter**2)),
        'notes':'Operator forecast, not a measured park yield. Native 10 m true colour; two 16 km × 16 km panels at identical projected metre scale. Published city area 127.58 km² differs slightly from current projected OGD geometry. Separate 5 km detail must not replace the 16 km panel in the same-scale comparison.'},
        'EnBW Weesow-Willmersdorf inauguration (2021); Sentinel-2A L2A 2025-09-11 via public AWS STAC; Stadt Graz OGD boundary (CC BY 4.0).',
        'Copernicus free/open attribution policy; city boundary CC BY 4.0; operator facts independently calculated.')
    price_rows = list(csv.DictReader((DATA/'pv-module-prices.csv').open()))
    emit('09-pv-prices',9,{'years':[int(r['year']) for r in price_rows],
        'prices':[float(r['USD_2025_per_Wp']) for r in price_rows],'unit':'constant 2025 USD/Wp',
        'cleared_through_year':2024,'notes':'Module prices, not installed-system cost. OWID splice is global before 2010 / European module benchmark thereafter. The IRENA report permits free reuse with attribution; attribute the pvXchange market benchmark as the underlying source.'},
        'OWID processing CC BY 4.0; Nemet 2009; Farmer & Lafond 2016; IRENA Renewable Power Generation Costs 2024, © IRENA 2025; pvXchange benchmark, attribution retained.')
    emit('09-pv-capacity',9,load('pv-capacity.json'),'IRENA Renewable capacity statistics 2026, explicit Solar photovoltaic table; © IRENA 2026.',
        'IRENA publication permits free reuse with attribution; © IRENA 2026; not represented as CC.')
    wind_tj = load('austria-balance.json')['rows']['3'][29]
    wind_energy = sp.Rational(str(wind_tj))*10**12*u.joule/YEAR
    emit('10-wind',10,{'eu_onshore_cf':float(v('eu_onshore_cf')),'eu_offshore_cf':float(v('eu_offshore_cf')),
        'eu_new_onshore_cf_range':[float(v('eu_new_onshore_cf_low')),float(v('eu_new_onshore_cf_high'))],
        'eu_new_offshore_cf_range':[float(v('eu_new_offshore_cf_low')),float(v('eu_new_offshore_cf_high'))],
        'austria_actual_generation_TWh':number(wind_energy*YEAR,10**9*KWH),
        'austria_yearend_MW':float(v('austria_wind_capacity')),
        'austria_cf_endyear_proxy':number(wind_energy/quantity('austria_wind_capacity')),
        'us_onshore_W_m2':float(v('us_wind_density')),'us_solar_W_m2':float(v('us_solar_density')),
        'offshore_HornsRev_W_m2_scenario':number(quantity('hornsrev_peak')*quantity('eu_offshore_cf')/quantity('hornsrev_area'),u.watt/u.meter**2),
        'offshore_site_MW':158,'offshore_site_km2':20,
        'photos':[p for p in photos if p['file']=='wind-freilaenderalm.jpg'],
        'notes':'Horns Rev area × current 158 MW operator capacity × EU fleet CF = scenario, not a measured site-specific mean. Austria year-end denominator is a CF proxy, not time-weighted capacity. Corrected US densities are capacity-weighted samples and use different land boundaries from the area-budget assumptions.'},
        'Miller & Keith 2019 corrigendum, DOI 10.1088/1748-9326/aaf9cf (CC BY 3.0); WindEurope Statistics 2024 p.20; Statistics Austria wind generation 2025; IG Windkraft year-end 2025; Vattenfall Horns Rev 1; Naturpuur photo (CC BY-SA 4.0).',
        'CC paper/photo cleared; WindEurope/IG/operator numerical facts only; Austrian raw balance custom terms.')
    area_rows = []
    for boundary,demand in [('final',flow['final_kWh_person_day']),('gross_inland',flow['gross_kWh_person_day'])]:
        per_power = sp.Rational(str(demand))*KWH/u.day
        for technology,density in [('biofuel',.5),('wind',2),('solar_low',10),('solar_high',20)]:
            ap = area_per_person.subs({P:per_power,q:sp.Rational(str(density))*u.watt/u.meter**2})
            area_rows.append({'boundary':boundary,'technology':technology,'density_W_m2':density,
                'area_km2_person':number(ap,10**6*u.meter**2),'national_area_km2':number(ap*quantity('austria_population'),10**6*u.meter**2),
                'fraction_of_Austria':number(ap*quantity('austria_population')/quantity('austria_area'))})
    corn_density = biofuel()*u.watt/u.meter**2
    final_power = sp.Rational(str(flow['final_kWh_person_day']))*KWH/u.day
    corn_area_person = area_per_person.subs({P:final_power,q:corn_density})
    corn_area_austria = corn_area_person*quantity('austria_population')
    corn_estimate = {'crop':'US corn → dry-mill ethanol (gross fuel energy)',
        'density_W_m2':number(corn_density,u.watt/u.meter**2),
        'final_energy_area_m2_person':number(corn_area_person,u.meter**2),
        'final_energy_area_km2_person':number(corn_area_person,10**6*u.meter**2),
        'Austria_area_km2':number(corn_area_austria,10**6*u.meter**2),
        'fraction_of_Austria':number(corn_area_austria/quantity('austria_area')),
        'vs_2_W_m2_wind':number(sp.Rational(2)*u.watt/u.meter**2/corn_density),
        'vs_10_W_m2_solar':number(sp.Rational(10)*u.watt/u.meter**2/corn_density),
        'vs_20_W_m2_solar':number(sp.Rational(20)*u.watt/u.meter**2/corn_density),
        'notes':'Gross ethanol LHV per harvested acre, before farm/distillery energy, land-use change and allocation of distillers grains; US crop yield is not an Austrian biofuel yield.'}
    csv_output('corn-ethanol-land.csv',[corn_estimate])
    emit('11-area-budget',11,{'Austria_km2':float(v('austria_area')),
        'Austria_km2_person':number(quantity('austria_area')/quantity('austria_population'),10**6*u.meter**2),
        'scenarios':area_rows,'corn_ethanol':corn_estimate,
        'notes':'Prescribed delivered densities, not predictions. The corn-to-ethanol chain is a separate gross fuel-energy estimate and should not be mistaken for the 0.5 W/m² area-budget scenario. Food competition depends on the crop, land quality, coproduct allocation and counterfactual; dedicated energy crops can displace food production or ecosystems.'},
        'Statistics Austria 2025 energy/population; Austrian ministry area 83,884 km²; FAO/WDI 2023 arable land; USDA 2024 corn yield; DOE ethanol yield/LHV; own SymPy calculation.',
        'Statistics Austria data reused with attribution per lecturer policy; USDA/DOE numerical facts are US public domain; original calculation.')
    csv_output('area-budget.csv',area_rows)
    fis = fission()
    history = historical_deployment()
    average = sp.Rational(str(flow['final_kWh_person_day']))*KWH/u.day
    counts = {region:number(deployment_count.subs({P:average*population,unit_power:10**9*u.watt,CF:quantity('nuclear_capacity_factor')}))
              for region,population in [('Austria',quantity('austria_population')),('world_at_Austrian_final_demand',quantity('world_population_2025'))]}
    emit('12-fission',12,{**fis,'historical_benchmark':history,'once_through_assumptions':{k:INPUTS[k] for k in ['nuclear_efficiency','nuclear_burnup','enrichment_product','enrichment_feed','enrichment_tails']},
        'deployment_world_population_2025':float(v('world_population_2025')),
        'reactors_1GWe_at_90percent_CF':counts,'reactors_per_year_over_30_years':{k:number(sp.Rational(str(x))/quantity('deployment_horizon'),1/YEAR) for k,x in counts.items()},
        'historical_grid_connections_per_year':history['grid_peak_units_per_year'],'historical_grid_peak_years':history['grid_peak_years'],
        'historical_construction_starts_per_year':history['construction_peak_units_per_year'],'historical_construction_peak_year':history['construction_peak_years'][0],
        'plant_photo_candidates':[p for p in photos if 'nuclear' in p['file'] or 'besse' in p['file']],
        'goesgen_net_MWe':1010,'notes':'Fuel is uranium heavy metal, not UO2 or initial core loading; full-power 1 GW(e) × 365 days. Deployment uses 2025 world population and compares a stated world-at-Austrian-final-energy scenario with first grid connections, not construction starts. Historical reactors vary in size; the scenario units are 1 GW(e). This accounting substitution is not a transition plan. IAEA 2025 historical peak verified over 1954–2024; capacities revised since the 2014 edition.'},
        'WNA Nuclear Fuel Cycle Overview fuel-cycle assumptions and rounded 24.3 t product / 211 t natural U benchmark; IAEA Nuclear Power Reactors in the World 2025 table 7; KKG technical data.', 'Numerical facts and original calculations; candidate photo licence verified, download status explicit.')
    emit('13-fusion',13,{**fusion(),'thermal_energy_GWh':number(10**9*u.watt*YEAR,10**6*KWH),
        'fuel_thermal_energy_TJ_kg':number(quantity('dt_energy')/
            ((v('deuterium_atomic_mass')+v('tritium_atomic_mass'))*quantity('atomic_mass')),10**12*u.joule/u.kilogram),
        'photos':[p for p in photos if p['file']=='jet-vessel-interior.jpg'],
        'notes':'GW(fusion) is thermal reaction power, not net electric output. Burned D+T only, excluding inventory, recycling losses and breeding overhead. Coal lower heating value assumed 24 MJ/kg. Seawater D is an inventory, not a recoverable reserve. Lithium reserves are elemental Li, not all Li-6; tritium must be bred, not extracted as a natural fuel reserve. Per-person normalization uses latest WDI 2025 population with 2025 lithium reserves.'},
        'IAEA D–T 17.6 MeV; NIST atomic masses and VSMOW D/H; NOAA ocean volume; USGS MCS Lithium 2026 (2025 data, public domain); EUROfusion JET vessel photo, CC BY 4.0.')
    bird_rows = [dict(r) for r in csv.DictReader((DATA/'wildlife-risk.csv').open())]
    emit('14-wildlife-risk',14,{'annual_estimates':bird_rows,
        'notes':'United States estimates cover different years, models, and taxa; ranges must not be summed as a common-year census. European wind-farm result is a median per-turbine rate from the reviewed sites, not a Europe-wide total.'},
        'Loss et al. 2013/2014 US studies; Naturvårdsverket Vindval Report 6511, review of European facilities; figures are independently plotted numeric estimates.')
    death_rows = [dict(r) for r in csv.DictReader((DATA/'energy-deaths-per-TWh.csv').open())]
    emit('14-energy-deaths',14,{'observations':death_rows,
        'notes':'2021 processed rates per TWh of electricity combine air-pollution and accidents using studies with different boundaries and observation periods. They are contextual estimates, not direct counts from a single harmonized life-cycle study.'},
        'Our World in Data, based on Markandya & Wilkinson (2007), Sovacool et al. (2016), UNSCEAR (2008/2018); OWID compilation CC BY 4.0.')
    with (DATA/'lifecycle-emissions.csv').open() as stream:
        emissions = [dict(r) for r in csv.DictReader(line for line in stream if not line.startswith('#'))]
    nrel_notice = (DATA/'nrel-lifecycle-notice.txt').read_text().strip()
    emit('15-lifecycle-emissions',15,{'observations':emissions,'unit':'g CO2-eq/kWh electricity','year':2026,
        'required_data_notice':nrel_notice,
        'notes':'NREL harmonized literature dataset, updated 2026-05-22; min/median/max for total lifecycle estimates. Technology/system boundaries vary; these distributions are not universal constants.'},
        'DOE/NREL/ALLIANCE Life Cycle Emissions Factors dataset; total lifecycle columns W/Y/AA, original plot with required attribution and full notice included in payload.')
    (OUT/'formulas.json').write_text(json.dumps({k:{'expression':str(x),'latex':sp.latex(x)} for k,x in FORMULAS.items()},indent=2)+'\n')
    write_numbers(results)
    print(f'Built {len(results)} plot-data files and {len(FORMULAS)} symbolic formulas; no slide design changed.')


# %% Lecturer's numerical ledger, with separate source keys and accounting years
def write_numbers(results):
    ledger = []
    def add(page,label,value,unit,year,key,note=''):
        ledger.append(dict(page=page,label=label,value=value,unit=unit,year=year,source_key=key,note=note))
    add(1,'Black Marble composite',2016,'year',2016,'nasa')
    add(2,'Countries/economies plotted',len(results['02-energy-gdp']['observations']),'count',2024,'eia + wb_gdp_ppp + wb_population')
    for row in results['02-energy-gdp']['observations']:
        if row['iso3'] in ['AUT','USA','CHN','IND','DEU','CHE']:
            add(2,row['country']+' energy',row['y'],'kWh/(person day)',2024,'eia + wb_population')
            add(2,row['country']+' GDP PPP',row['x'],'2021 international dollar/(person year)',2024,'wb_gdp_ppp')
            add(2,row['country']+' population',row['population'],'person',2024,'wb_population')
    for row in results['03-access-and-dollarstreet']['access']:
        add(3,row['series']+' access',row['value'],row['unit'],row['year'],row['source'])
    for row in results['03-income-levels']['observations']:
        add(3,f"Level {row['level']} income threshold {row['income_threshold']}",row['income_threshold'],
            '2011 PPP USD/(person day)',2017,'gapminder_income_levels')
        add(3,f"Level {row['level']} population",float(row['population_billions']),'billion people',2017,
            'gapminder_income_levels','Rounded published estimate.')
    for row in results['03-land-use']['observations']:
        add(3,row['place']+' arable land',row['faostat_arable_ha_person'],'ha/person',2023,'faostat_arable')
        add(3,row['place']+' cropland',row['hyde_cropland_ha_person'],'ha/person',2023,'hyde_cropland')
    for p in results['03-access-and-dollarstreet']['photos']:
        add(3,p['title'],p['income'],p['income_unit'],p['date'],'dollarstreet',p['author']+'; '+p['family'])
    micro = results['04-micro-macro']
    for name,value in micro['legacy_components'].items():add(4,name,value,'kWh/(person day)',2025,'legacy_handwriting')
    for name,unit,key,year in [('legacy_total','kWh/(person day)','legacy_handwriting',2025),
        ('legacy_GDP_EUR_person_year','EUR/(person year)','legacy_handwriting',2025),
        ('legacy_intensity_kWh_EUR','kWh/EUR','legacy_handwriting',2025),
        ('legacy_GDP_crosscheck_kWh_person_day','kWh/(person day)','legacy_handwriting',2025),
        ('legacy_car_arithmetic_kWh_person_day','kWh/(person day)','legacy_handwriting',2025),
        ('gross_kWh_person_day','kWh/(person day)','stat_balance + stat_population',2025),
        ('final_kWh_person_day','kWh/(person day)','stat_balance + stat_population',2025),
        ('gross_W_person','W/person','stat_balance + stat_population',2025),
        ('final_W_person','W/person','stat_balance + stat_population',2025),
        ('gross_GW_average','GW','stat_balance',2025),('final_GW_average','GW','stat_balance',2025),
        ('population','person','stat_population',2025),('GDP_EUR_person_year','EUR/(person year)','wb_gdp_austria',2025),
        ('derived_gross_intensity_kWh_EUR','kWh/EUR','stat_balance + stat_population + wb_gdp_austria',2025)]:
        add(4,name,micro[name],unit,year,key)
    flow = results['05-austria-flow']
    for name in ['gross_TJ','final_TJ']:add(5,name,flow[name],'TJ',2025,'stat_balance')
    for name in ['conversion_loss','own_use_and_transport_losses','nonenergy']:
        add(5,name,flow[name+'_kWh_person_day'],'kWh/(person day)',2025,'stat_balance + stat_population')
    for kind in ['sectors','carriers']:
        for label,value in flow[kind+'_kWh_person_day'].items():
            add(5,kind+': '+label,value,'kWh/(person day)',2025,'stat_balance + stat_population')
    for record in results['06-resource-lifetimes']['resources']:
        label=record['resource'];key=record['source'];year=record['year']
        for name,unit in [('stock',record['stock_unit']),('production',record['production_unit']),('static_years','year'),
            ('power_W_person_for_1000_years','W(thermal)/person')]:add(6,label+' '+name,record[name],unit,year,key)
        if 'energy_EJ' in record:add(6,label+' energy reserve',record['energy_EJ'],'EJ',year,key)
        add(6,label+' lifetime at continuous 2%/year',record['growth_lifetime_years'][20],'year',year,key+' + assumptions')
    for s,power in results['06-resource-lifetimes']['legacy_1000_years_W_person'].items():
        add(6,'2025 handwritten '+s+' 1000-year power',power,'W/person',2025,'legacy_handwriting',
            '10 billion people; coal 10 kWh/kg; uranium 10 million kWh/kg near-complete fission potential.')
        add(6,'2025 handwritten '+s+' 1000-year daily energy',number(sp.Rational(str(power))*u.watt,KWH/u.day),'kWh/(person day)',2025,'legacy_handwriting')
        add(6,'2025 handwritten '+s+' lifetime at 100 kWh/person/day',results['06-resource-lifetimes']['legacy_lifetime_at_100_kWh_person_day_years'][s],'year',2025,'legacy_handwriting')
    sol = results['07-solar-chain']
    for name,unit in [('horizontal_kWh_m2_year','kWh/(m² year)'),('horizontal_W_m2','W/m²'),
        ('inclined_kWh_m2_year','kWh/(m² year)'),('specific_yield_kWh_kWp_year','kWh/(kWp year)'),('module_W_m2','W/m²')]:
        add(7,name,sol[name],unit,'2005–2023','pvgis + assumptions')
    for name,value in sol['factors'].items():add(7,name+' factor',value,'1','model / 2005–2023','pvgis + assumptions')
    for row in sol['stages']:add(7,'After '+row['stage'],row['W_m2'],'W/m²','model / 2005–2023','pvgis + assumptions')
    for name,value in sol['pvgis_loss_percent'].items():add(7,name,value,'%', '2005–2023','pvgis','Signed PVGIS model percentage; do not apply these again to the exported performance ratio.')
    for m,value in zip(sol['months'],sol['monthly_horizontal_kWh_m2']):add(7,'Month '+str(m)+' horizontal irradiation',value,'kWh/m²','2005–2023','pvgis')
    geo = results['08-park-and-graz']
    for name,unit in [('park_area_km2','km²'),('peak_MWp','MWp'),('expected_GWh_year','GWh/year'),
        ('ground_W_m2','W/m²'),('capacity_factor_expected','1'),('area_for_1_GW_average_km2','km²'),
        ('peak_GWp_for_1_GW_average','GWp'),('park_equivalents_for_1_GW_average','1'),
        ('fraction_of_Graz_geometry_for_1_GW_average','1')]:
        add(8,name,geo[name],unit,2021,'enbw_weesow','Design expectation; not observed yield.')
    add(8,'Graz OGD projected boundary area',geo['graz_projected_area_km2'],'km²',2026,'graz_boundary')
    add(8,'Graz published area',127.58,'km²',2026,'graz_boundary')
    add(8,'True-colour native pixel',10,'m','2025-09-11','sentinel')
    add(8,'Each same-scale panel width/height',16,'km','2025-09-11','sentinel')
    for axis,value in geo['park_coordinates_wgs84'].items():add(8,'Park '+axis,value,'degree',2026,'wikidata')
    prices = results['09-pv-prices']
    for year,value in zip(prices['years'],prices['prices']):add(9,'PV module price',value,prices['unit'],year,'owid_prices','IRENA segment: © IRENA 2025; pvXchange benchmark attribution retained.')
    cap = results['09-pv-capacity']
    for year,world,at in zip(cap['years'],cap['world_PV'],cap['austria_PV']):
        add(9,'World installed PV',world,'MW, year-end',year,'irena_capacity','Provider-reported installed capacity; AC/DC conventions vary. © IRENA 2026.')
        add(9,'Austria installed PV',at,'MW, year-end',year,'irena_capacity','Provider-reported installed capacity. © IRENA 2026.')
    wind = results['10-wind']
    for name,unit,key,year in [('eu_onshore_cf','1','windeurope',2024),('eu_offshore_cf','1','windeurope',2024),
        ('austria_actual_generation_TWh','TWh/year','stat_balance',2025),('austria_yearend_MW','MW','igwind',2025),
        ('austria_cf_endyear_proxy','1','stat_balance + igwind',2025),('us_onshore_W_m2','W/m²','miller_corrigendum',2016),
        ('us_solar_W_m2','W/m²','miller_corrigendum',2016),('offshore_HornsRev_W_m2_scenario','W/m²','vattenfall_hornsrev + windeurope','scenario')]:
        add(10,name,wind[name],unit,year,key)
    for name in ['eu_new_onshore_cf_range','eu_new_offshore_cf_range']:add(10,name,wind[name],'1',2024,'windeurope','New-farm estimate.')
    for row in results['14-wildlife-risk']['annual_estimates']:
        for bound in ('low','median','high'):
            if row[bound] not in ('',None):
                add(14,row['cause']+' '+bound,row[bound],row['unit'],row['year'],row['source'],row['scope'])
    for row in results['14-energy-deaths']['observations']:
        add(14,row['source_type']+' deaths per TWh',row['deaths_per_TWh'],'deaths/TWh electricity',row['year'],'owid_deaths',
            'Processed source estimates mix air-pollution and accident evidence.')
    for row in results['15-lifecycle-emissions']['observations']:
        for bound in ('min','median','max'):
            add(15,row['technology']+' '+bound,row[bound+'_gCO2eq_kWh'],row['unit'],2026,'nrel_lifecycle')
    area = results['11-area-budget']
    add(11,'Austria area',area['Austria_km2'],'km²',2024,'bml_area')
    add(11,'Austria area per person',area['Austria_km2_person'],'km²/person',2025,'bml_area + stat_population')
    for r in area['scenarios']:
        for name,unit in [('density_W_m2','W/m²'),('area_km2_person','km²/person'),('national_area_km2','km²'),('fraction_of_Austria','1')]:
            add(11,r['boundary']+' '+r['technology']+' '+name,r[name],unit,2025,'assumptions + stat_balance + stat_population + bml_area')
    for name,value,unit in [('Corn ethanol gross power density',area['corn_ethanol']['density_W_m2'],'W/m²'),
        ('Corn ethanol area per person',area['corn_ethanol']['final_energy_area_km2_person'],'km²/person'),
        ('Corn ethanol national area',area['corn_ethanol']['Austria_area_km2'],'km²'),
        ('Corn ethanol fraction of Austria',area['corn_ethanol']['fraction_of_Austria'],'1'),
        ('Wind 2 W/m² divided by corn ethanol',area['corn_ethanol']['vs_2_W_m2_wind'],'1'),
        ('Solar 10 W/m² divided by corn ethanol',area['corn_ethanol']['vs_10_W_m2_solar'],'1'),
        ('Solar 20 W/m² divided by corn ethanol',area['corn_ethanol']['vs_20_W_m2_solar'],'1')]:
        add(11,name,value,unit,2024,'usda_corn + doe_ethanol + stat_balance + stat_population')
    fis = results['12-fission']
    for name in ['enriched_t_U','natural_t_U','tails_t_U']:add(12,name,fis[name],'t U/(GW(e) full-power year)','model','wna_fuel')
    add(12,'Natural uranium thermal energy per kg in once-through model',fis['natural_specific_thermal_J_kg'],'J/kg U','model','wna_fuel')
    for kind in ['reactors_1GWe_at_90percent_CF','reactors_per_year_over_30_years']:
        for region,value in fis[kind].items():add(12,kind+' '+region,value,'reactor' if kind.startswith('reactors_1') else 'reactor/year','2025 / scenario','stat_balance + stat_population + wb_population + assumptions')
    add(12,'Maximum first grid connections in IAEA 1954–2024 table',33,'reactor/year','1984 / 1985','iaea_history')
    add(12,'Maximum construction starts in that table',43,'reactor/year',1976,'iaea_history')
    add(12,'Maximum annually grid-connected net capacity',fis['historical_benchmark']['grid_capacity_peak_GWe_per_year'],'GW(e)/year',1985,'iaea_history')
    add(12,'First grid connections 2024',fis['historical_benchmark']['grid_connections_2024'],'reactor/year',2024,'iaea_history')
    add(12,'Grid-connected net capacity 2024',fis['historical_benchmark']['grid_capacity_2024_GWe'],'GW(e)/year',2024,'iaea_history')
    add(12,'Gösgen net electric capacity',1010,'MW(e)',2026,'kkg')
    add(12,'World population for deployment scenario',fis['deployment_world_population_2025'],'person',2025,'wb_population')
    fus = results['13-fusion']
    for name,unit,key in [('Q_MeV','MeV/reaction','iaea_fusion'),('Q_J','J/reaction','iaea_fusion + nist_constants'),
        ('thermal_energy_GWh','GWh/(GW(fusion) year)','assumptions'),('reactions_per_GW_fusion_year','reaction','iaea_fusion + nist_constants'),
        ('fuel_thermal_energy_TJ_kg','TJ/kg D+T','iaea_fusion + nist_isotopes + nist_constants'),
        ('deuterium_kg','kg/(GW(fusion) year)','iaea_fusion + nist_constants + nist_isotopes'),
        ('tritium_kg','kg/(GW(fusion) year)','iaea_fusion + nist_constants + nist_isotopes'),
        ('fuel_kg','kg/(GW(fusion) year)','iaea_fusion + nist_constants + nist_isotopes'),('coal_kg','kg/(GW(thermal) year)','assumptions'),
        ('deuterium_g_m3','g/m³','nist_vsmow + nist_isotopes + assumptions'),('ocean_deuterium_kg','kg D','noaa_ocean + nist_vsmow + assumptions'),
        ('ocean_deuterium_kg_per_person','kg D/person','noaa_ocean + nist_vsmow + assumptions + wb_population'),
        ('lithium_kg_per_person','kg Li/person','usgs_lithium + wb_population')]:add(13,name,fus[name],unit,'physical constants / model; inventories 2024–2025',key)
    # Keep all substitution constants visible, including unit/year assumptions.
    input_pages = {7:['solar_noon','pv_efficiency','graz_latitude','obliquity'],
        6:['sustainable_horizon','legacy_world_population','legacy_daily_demand','world_population'],
        10:['hornsrev_area','hornsrev_peak','austria_wind_capacity'],
        11:['corn_yield','ethanol_yield','ethanol_lhv','btu_IT'],
        12:['nuclear_efficiency','nuclear_burnup','enrichment_product','enrichment_feed','enrichment_tails','nuclear_capacity_factor','deployment_horizon'],
        13:['world_population_2025','elementary_charge','atomic_mass','deuterium_atomic_mass','tritium_atomic_mass','coal_heat','ocean_volume',
            'seawater_density','seawater_water_fraction','water_molecular_mass','deuterium_hydrogen_ratio','lithium_reserves','lithium_production','seconds_per_year']}
    for page,keys in input_pages.items():
        for key in keys:
            r = INPUTS[key];add(page,'Input: '+key,r['value'],r['unit'],r['year'],r['source'],r['notes'])
    (DATA/'numbers.json').write_text(json.dumps(ledger,indent=2,ensure_ascii=False)+'\n')
    titles = ['Earth at night','Energy and GDP','Access and Dollar Street','Micro → macro','Austria balance flow',
              'Resource lifetimes','Solar chain','Park and Graz at equal scale','PV prices and capacity','Wind','Area budget','Fission','Fusion','Risk','Lifecycle emissions']
    with (ROOT/'NUMBERS.md').open('w') as f:
        f.write('# Chapter 0 numerical ledger\n\nAccessed 2026-10-06. Full precision is retained in JSON; displayed figures below are rounded to six significant digits. '
                'All years are 365-day engineering years. Source keys resolve in [data/ch00/sources.json](data/ch00/sources.json) and [data/README.md](data/README.md). '
                'Per-series reuse terms and attribution requirements are authoritative in each plot-data file and data/README.md. Noncommercial sources are excluded.\n\n'
                'Every country observation is in `derivations/build/plotdata/02-energy-gdp.json`; the table below selects likely labelled examples. '
                'Complete final carrier–sector values are in `05-austria-flow.json`; growth curves are in `06-resource-lifetimes.json`.\n')
        for page,title in enumerate(titles,1):
            f.write(f'\n## {page}. {title}\n\n| Quantity | Value | Unit | Year | Source key |\n|---|---:|---|---|---|\n')
            for r in ledger:
                if r['page']!=page:continue
                value = f"{r['value']:.6g}" if isinstance(r['value'],(float,int)) else str(r['value'])
                f.write(f"| {r['label']} | {value} | {r['unit']} | {r['year']} | {r['source_key']} |\n")
            for record in results.values():
                if record['page']==page and record.get('notes'):f.write('\n'+record['notes']+'\n')
            notes = [r['label']+': '+r['note'] for r in ledger if r['page']==page and r['note']]
            if notes:f.write('\n'+ '\n\n'.join(dict.fromkeys(notes))+'\n')
            if page==15:
                f.write('\nNREL data-use notice (required by source terms):\n\n'+(DATA/'nrel-lifecycle-notice.txt').read_text().strip()+'\n')


if __name__ == '__main__':
    build()
