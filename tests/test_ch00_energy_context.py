"""Independent behavioral oracles: SI dimensions, balance, measured totals.

No tests assert that files merely exist or that repository text matches a patch.
Published reference values are intentionally kept separate from loader inputs.
"""
import csv
import json
import sys
from pathlib import Path
import numpy as np
import pytest
import sympy as sp
from sympy.physics import units as u

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'derivations'))
from chapters import ch00_energy_context as c


@pytest.mark.parametrize('expression,expected',[
    (c.power_per_person,u.watt),(c.area_per_person,u.meter**2),
    (c.stock_years,u.second),(c.growth_lifetime,u.second),
    (c.delivered_module_density,u.watt/u.meter**2),
    (c.solar_factor_chain,u.watt/u.meter**2),
    (c.biofuel_density,u.watt/u.meter**2),
    (c.enriched_fuel,u.kilogram),(c.enrichment[c.F],u.kilogram),
    (c.fusion_fuel,u.kilogram),(c.deuterium_inventory,u.kilogram)])
def test_physical_dimensions(expression,expected):
    assert c.same_unit(c.si_unit(expression,c.DIMENSIONS),expected)


def test_one_person_one_kilowatt_year():
    # Independent SI energy budget of a 1 kW appliance, 24 h each day.
    assert c.daily(31.536/1000,1) == pytest.approx(24)


def test_economic_rate_preserves_year_dimension():
    assert c.same_unit(c.si_unit(c.economic_power,c.DIMENSIONS),u.watt)
    assert c.same_unit(c.si_unit(c.energy_intensity,c.DIMENSIONS),u.joule)
    power=c.economic_power.subs({c.GDP:60000/c.YEAR,c.intensity:c.KWH})
    assert c.number(power,c.KWH/u.day)==pytest.approx(60000/365)


def test_international_table_btu_energy_budget():
    # NIST conversion oracle, separately specified from the data-file input.
    energy=10**15*c.quantity('btu_IT')
    power=c.power_per_person.subs({c.E:energy,c.N:10**6,c.T:c.YEAR})
    expected=1.05505585262e18/(1e6*365*3.6e6)
    assert c.number(power,c.KWH/u.day)==pytest.approx(expected,rel=1e-12)


def test_published_austria_final_total_and_conservation():
    flow = c.austria_flow()
    # Statistics Austria preliminary 2025, published AL13 total in TJ.
    assert sum(flow['sectors_kWh_person_day'].values())*9_204_460.875*365*3.6e6/1e12 == pytest.approx(1_054_125.4093488748,abs=.001)
    for node in flow['nodes']:
        incoming = sum(l['value_TJ'] for l in flow['links'] if l['target']==node['id'])
        outgoing = sum(l['value_TJ'] for l in flow['links'] if l['source']==node['id'])
        if incoming and outgoing:assert incoming == pytest.approx(outgoing,abs=.001),node['id']
    assert sum(l['value_TJ'] for l in flow['links'] if l['target']=='gross') == pytest.approx(1_354_675.2350887195,abs=.001)
    assert all(l['value_TJ']>=0 for l in flow['links'])


def test_primary_balance_against_indigenous_trade_and_stocks():
    rows = c.load('austria-balance.json')['rows']
    # An independent upstream accounting route, before transformation.
    expected = sum(float(rows[str(r)][37]) for r in [3,4,5,6])-float(rows['7'][37])
    assert expected == pytest.approx(1_354_675.2350887195,abs=.001)


@pytest.mark.parametrize('stock_years,growth',[(100,.02),(50,.01),(146,.03)])
def test_growth_exhausts_stock_by_independent_quadrature(stock_years,growth):
    end = c.number(c.growth_lifetime.subs({c.R:stock_years,c.D:1,c.g:sp.Rational(str(growth))}))
    times = np.linspace(0,end,20001)
    assert np.trapezoid(np.exp(growth*times),times) == pytest.approx(stock_years,rel=1e-8)
    assert 0 < end < stock_years
    assert c.zero_growth_lifetime.subs({c.R:stock_years,c.D:1}) == stock_years


def test_fuel_cycle_reproduces_rounded_published_benchmark():
    fuel = c.fission()
    # WNA's table is rounded (24.3 t product, 211 t feed); no exact match asserted.
    assert fuel['enriched_t_U'] == pytest.approx(24.3,rel=.02)
    assert fuel['natural_t_U'] == pytest.approx(211,rel=.02)
    assert fuel['natural_t_U'] == pytest.approx(fuel['enriched_t_U']+fuel['tails_t_U'])
    # Independent isotope conservation, separate from symbolic solution.
    assert .00711*fuel['natural_t_U'] == pytest.approx(.045*fuel['enriched_t_U']+.0022*fuel['tails_t_U'])


def test_pvgis_reproduces_published_yearly_tilted_total():
    raw=json.loads((ROOT/'data/ch00/raw/pvgis_graz.json').read_text())
    # Monthly irradiation must reproduce independently provided annual total.
    total=sum(r['H(i)_m'] for r in raw['outputs']['monthly']['fixed'])
    assert total == pytest.approx(1542.13,abs=.06)
    sol=c.solar()
    assert sol['horizontal_kWh_m2_year'] == pytest.approx(1286.6147368421052,rel=1e-12)
    chain=1000
    for factor in sol['factors'].values():chain*=factor
    assert chain == pytest.approx(sol['module_W_m2'],rel=1e-12)


def test_equinox_geometry_by_independent_midpoint_integration():
    # Integrate positive horizontal cosine over a full Earth rotation.
    angle=(np.arange(20000)+.5)*2*np.pi/20000-np.pi
    latitude=np.deg2rad(47.0707)
    average=np.maximum(np.cos(angle),0).mean()*np.cos(latitude)
    symbolic=c.number(c.daily_geometry.subs({c.phi:sp.Rational('47.0707')*sp.pi/180,c.delta:0}))
    assert average == pytest.approx(symbolic,rel=1e-8)


def test_dt_burned_fuel_uses_equal_particle_numbers():
    fuel=c.fusion()
    assert fuel['fuel_kg'] == pytest.approx(93.4144,rel=1e-6)
    assert fuel['deuterium_kg']/.00201410177812 == pytest.approx(fuel['tritium_kg']/.0030160492779)
    # Recover 1 GW-year independently from number of deuterium atoms and Q.
    avogadro=6.02214076e23
    recovered=(fuel['deuterium_kg']/.00201410177812)*avogadro*17.6e6*1.602176634e-19
    assert recovered == pytest.approx(31.536e15,rel=1e-8)
    assert fuel['coal_kg']*24e6 == pytest.approx(31.536e15)
    ocean_volume=1.335e9*1e9
    water_density=1025
    water_fraction=.965
    D_H=155.76e-6
    D_u=2.01410177812
    water_u=18.01528
    D_per_water=water_density*water_fraction*(2*D_u/water_u)*D_H/(1+D_H)
    expected_D_person=D_per_water*ocean_volume/8.21542e9
    assert fuel['ocean_deuterium_kg_per_person'] == pytest.approx(expected_D_person,rel=2e-6)
    assert fuel['lithium_kg_per_person'] == pytest.approx(37e9/8.21542e9,rel=2e-6)


def test_published_resource_ratios_keep_native_units():
    # BGR world row facts, independently divided here as an oracle.
    records={r['resource']:r for r in c.resources()}
    assert records['oil']['static_years'] == pytest.approx(252374/4553.5)
    assert records['gas']['static_years'] == pytest.approx(207714/4273.2)
    assert records['uranium_lowcost']['static_years'] == pytest.approx(1181/62.4)
    assert records['uranium_identified_below_260_USD_kg']['static_years'] == pytest.approx(7934500/54345)


def test_one_gigawatt_average_park_area_by_energy_accounting():
    # EnBW 180 GWh/year on 1.64 km²; one GW-year is 8760 GWh.
    expected=8760/180*1.64
    density=c.quantity('park_annual_energy')/c.quantity('park_area')
    area=c.number(c.area_per_person.subs({c.P:10**9*u.watt,c.q:density}),10**6*u.meter**2)
    assert area == pytest.approx(expected)
    assert c.number(density,u.watt/u.meter**2) == pytest.approx(180e9/(1.64e6*365*24))
    assert c.number(c.quantity('park_annual_energy')/c.quantity('park_peak')) == pytest.approx(180000/(187*8760))


def test_wind_fleet_factors_and_site_density_scenarios_reproduce_inputs():
    wind=json.loads((ROOT/'derivations/build/plotdata/10-wind.json').read_text())
    assert wind['eu_onshore_cf']==pytest.approx(.23)
    assert wind['eu_offshore_cf']==pytest.approx(.35)
    assert wind['austria_actual_generation_TWh']==pytest.approx(8.577926627)
    expected_austria_proxy=8.577926627e12/(4221e6*365*24)
    assert wind['austria_cf_endyear_proxy']==pytest.approx(expected_austria_proxy)
    assert wind['offshore_HornsRev_W_m2_scenario']==pytest.approx(158e6*.35/(20e6))


def test_current_iaea_history_reproduces_published_benchmarks():
    history=c.historical_deployment()
    # IAEA RDS2/45 table 7, independently read in the published 2025 report.
    assert history['grid_peak_units_per_year']==33
    assert history['construction_peak_units_per_year']==43
    assert history['grid_capacity_peak_GWe_per_year']==pytest.approx(31.129)
    assert history['grid_connections_2024']==6
    assert history['grid_capacity_2024_GWe']==pytest.approx(6.803)


def test_2023_land_per_person_matches_published_series():
    rows={r['place']:r for r in csv.DictReader((ROOT/'data/ch00/processed/land-use.csv').open())}
    assert float(rows['World']['faostat_arable_ha_person']) == pytest.approx(0.17167939)
    assert float(rows['Austria']['faostat_arable_ha_person']) == pytest.approx(0.14474553)
    assert float(rows['World']['hyde_cropland_ha_person']) == pytest.approx(0.20268911)
    assert float(rows['Austria']['hyde_cropland_ha_person']) == pytest.approx(0.15801372)


def test_gapminder_2017_population_by_income_level_matches_published_facts():
    rows={int(r['level']):r for r in csv.DictReader((ROOT/'data/ch00/processed/income-levels-2017.csv').open())}
    expected={1:('<2',.75),2:('2–8',3.3),3:('8–32',2.5),4:('>32',.9)}
    assert set(rows)==set(expected)
    for level,(threshold,population) in expected.items():
        assert rows[level]['income_threshold']==threshold
        assert float(rows[level]['population_billions'])==pytest.approx(population)
        assert rows[level]['source']=='gapminder_income_levels'
        assert 'CC BY 4.0' in rows[level]['licence_status']


def test_corn_ethanol_density_and_land_demand_independently():
    # USDA 2024 yield, DOE dry-mill yield and pure-ethanol LHV, converted independently.
    energy_per_bushel=2.8*76330*1055.05585262
    expected_density=179.3*energy_per_bushel/(4046.8564224*365*24*3600)
    assert c.biofuel() == pytest.approx(expected_density,rel=1e-12)
    flow=c.austria_flow()
    watts_person=flow['final_kWh_person_day']*1000/24
    area_person=watts_person/expected_density
    assert area_person == pytest.approx(11463.116,rel=2e-6)
    assert area_person/1e6 < 0.012


def test_us_bird_mortality_ranges_and_european_rate_reproduce_sources():
    rows={r['source']:r for r in csv.DictReader((ROOT/'data/ch00/processed/wildlife-risk.csv').open())}
    assert float(rows['loss_cats']['low']) == pytest.approx(1.3e9)
    assert float(rows['loss_cats']['high']) == pytest.approx(4.0e9)
    assert float(rows['loss_buildings']['median']) == pytest.approx(599e6)
    assert float(rows['loss_vehicles']['low']) == pytest.approx(89e6)
    assert float(rows['loss_powerlines']['high']) == pytest.approx(64e6)
    assert float(rows['loss_wind']['median']) == pytest.approx(234012)
    assert float(rows['naturvardsverket_birds']['median']) == pytest.approx(6.5)
    assert rows['naturvardsverket_birds']['unit'] == 'birds/turbine/year'


def test_energy_death_rates_match_2021_owid_published_values():
    rows={r['source_type']:r for r in csv.DictReader((ROOT/'data/ch00/processed/energy-deaths-per-TWh.csv').open())}
    assert float(rows['Coal']['deaths_per_TWh']) == pytest.approx(24.62)
    assert float(rows['Gas']['deaths_per_TWh']) == pytest.approx(2.821)
    assert float(rows['Wind']['deaths_per_TWh']) == pytest.approx(.035)
    assert float(rows['Nuclear']['deaths_per_TWh']) == pytest.approx(.03)
    assert all(int(r['year']) == 2021 for r in rows.values())


def test_nrel_lifecycle_ranges_include_nonzero_low_carbon_sources():
    csv_lines=(ROOT/'data/ch00/processed/lifecycle-emissions.csv').read_text().splitlines()
    notice_lines=[]
    while csv_lines and csv_lines[0].startswith('# '):
        notice_lines.append(csv_lines.pop(0)[2:])
    notice='\n'.join(notice_lines)
    assert 'this entire notice appears in all copies of the Data' in notice
    assert 'credit DOE/NREL/ALLIANCE in any publication' in notice
    assert notice == (ROOT/'data/ch00/processed/nrel-lifecycle-notice.txt').read_text().strip()
    rows={r['technology']:r for r in csv.DictReader(csv_lines)}
    assert float(rows['Coal']['median_gCO2eq_kWh']) == 1001
    assert float(rows['Natural gas (NGCC)']['median_gCO2eq_kWh']) == 450
    assert float(rows['Solar PV']['median_gCO2eq_kWh']) == pytest.approx(43.4)
    assert float(rows['Wind']['median_gCO2eq_kWh']) == 13
    assert float(rows['Nuclear (LWR)']['median_gCO2eq_kWh']) == 13
    assert all(float(r['min_gCO2eq_kWh']) > 0 for r in rows.values())


def test_living_standards_global_counts_and_energy_boundaries():
    data=c.living_standards()
    # Global PIP counts at $3/day, September 2026 release; independently specified.
    expected={1981:(4518389266,2128547233,None),
              2000:(6161884811,2230903823,78.224965031972),
              2024:(8141808945,824298368,91.9264843853681)}
    for year,(population,below_three,electricity) in expected.items():
        rows=[r for r in data['observations'] if r['year']==year]
        assert sum(r['population'] for r in rows)==population
        assert rows[0]['population']==below_three
        assert sum(r['population_share_percent'] for r in rows)==pytest.approx(100)
        assert all(r['population']>=0 for r in rows)
        # Cross-check the two intermediate cutoffs against the retained cumulative series.
        for cutoff,count in [(12,sum(r['population'] for r in rows[:2])),
                             (48,sum(r['population'] for r in rows[:3]))]:
            records=json.loads((ROOT/f'data/ch00/raw/pip-income-{cutoff}.json').read_text())
            raw=next(r for r in records if r['region_code']=='WLD' and r['reporting_year']==year)
            assert count==raw['pop_in_poverty']
        comparison=next(r for r in data['comparisons'] if r['year']==year)
        if year==1981:
            assert comparison['electricity_access_percent'] is None
            assert comparison['austria_ethiopia_primary_energy_ratio'] is None
            continue
        assert comparison['electricity_access_percent']==pytest.approx(electricity)
        energy=json.loads((ROOT/f'data/ch00/raw/eia_{year}.json').read_text())['response']['data']
        pops=json.loads((ROOT/'data/ch00/raw/wb-population-comparison.json').read_text())[1]
        power={}
        for code in ('AUT','ETH'):
            q=float(next(r['value'] for r in energy if r['countryRegionId']==code))
            pop=next(r['value'] for r in pops if r['countryiso3code']==code and int(r['date'])==year)
            power[code]=q*1e15*1055.05585262/(pop*365*3.6e6)
            assert comparison['primary_energy_kWh_person_day'][code]==pytest.approx(power[code])
        assert comparison['austria_ethiopia_primary_energy_ratio']==pytest.approx(power['AUT']/power['ETH'])


def test_capacity_additions_preserve_retirements_and_units():
    # Independent published year-end stocks, EIA International, GW.
    power = 1_054_125.4093488748*10**12/(365*86400)*u.watt
    data = c.capacity_additions(power)
    series = {r['technology']:r for r in data['series']}
    for name, expected in [('Solar',1863.366126946-1414.371787284),
                           ('Nuclear',378.6512-382.362)]:
        assert series[name]['net_additions_GW_per_year'][-1]['value'] == pytest.approx(expected)
    assert series['Nuclear']['net_additions_GW_per_year'][-1]['value'] < 0
    # Net changes must telescope to the observed stock difference.
    for r in data['series']:
        assert sum(x['value'] for x in r['net_additions_GW_per_year']) == pytest.approx(
            r['stock_GW'][-1]['value']-r['stock_GW'][0]['value'])
    assert data['austria']['benchmark_GW_per_year'] == pytest.approx(
        1_054_125.4093488748*1000/(365*86400)/.9)


def test_cost_scenarios_anchor_relative_changes_and_constant_real_reference():
    from chapters import ch00_electricity_costs as costs
    data = costs.payload()
    future = {(r['technology'],r['year']):r for r in data['annual'] if r['year']>2025}
    # Nuclear: explicit flat-to-2030 assumption, then ATB 2035 / 2030 change.
    for year, value in [(2030,18.05),(2035,18.05*76.20901655481597/78.24154508909304)]:
        nuclear = future['nuclear_fission_new',year]
        assert nuclear['us_cents_per_kWh_2025'] == pytest.approx(value)
        assert nuclear.get('series_basis') is None
        assert nuclear['atb_reference_year'] == 2030
        assert 'constant real cost to 2030' in nuclear['scenario']
    for year, atb_value in [(2030,30.887314198316133),(2035,25.207053154674952)]:
        wind = future['onshore_wind',year]
        assert wind['us_cents_per_kWh_2025'] == pytest.approx(3.3*atb_value/37.008271306759816)
        assert wind.get('series_basis') is None  # Same anchored sample: connect at 2025.
    for tech, value in [('coal',12.2),('natural_gas_CCGT',7.85)]:
        for year in (2030,2035):
            row = future[tech,year]
            assert row['us_cents_per_kWh_2025'] == value
            assert 'Constant' in row['scenario']
            assert row['evidence_flag'] == 'F'


def test_fusion_resource_budget_uses_world_demand_and_distinguishes_blanket_stocks():
    result = c.fusion_resources()
    # Independent EIA QBTU conversion and MacKay natural-Li yield.
    annual_J = 606.037013293999 * 1e15 * 1055.05585262
    li_kg_year = annual_J / (2300 * 1000 * 3.6e6)
    fuels = {row['resource']: row for row in result['fuel']}
    assert result['world_primary_EJ_year'] == pytest.approx(annual_J/1e18)
    assert fuels['lithium_reserves']['static_years'] == pytest.approx(37e9/li_kg_year)
    assert fuels['lithium_seawater']['static_years'] == pytest.approx(.00017*1.335e18/li_kg_year)
    assert result['extraction_fraction'] == pytest.approx(2.5/2300)
    assert result['seawater_minimum_km3_year'] == pytest.approx(li_kg_year/.00017/1e9)
    # D-T consumes one D nucleus per 17.6 MeV; it still needs lithium.
    d_rate = annual_J/(.4*17.6e6*1.602176634e-19)*.00201410177812/6.02214076e23
    assert fuels['deuterium_seawater']['static_years'] == pytest.approx(
        c.fusion()['ocean_deuterium_kg']/d_rate,rel=1e-8)
    # Same net-electric output; initial inventories use installed power at 90% CF.
    average_GW = annual_J/(365*86400)/1e9
    installed = average_GW/.9
    materials = {r['material']:r for r in result['blanket_materials']}
    assert materials['lead']['fleet_initial_t'] == pytest.approx(installed*4092)
    assert materials['lead']['fleet_burnup_t_year'] == pytest.approx(average_GW*3.1)
    assert materials['beryllium']['fleet_initial_t'] == pytest.approx(installed*120)
    assert materials['beryllium']['fleet_burnup_t_year'] == pytest.approx(average_GW*.19)
    budgets = {r['resource']:r for r in result['blanket_lifetimes']}
    for key,stock in [('lead_reserves',95e6),('lead_resource_reference',2e9)]:
        row = budgets[key]
        expected = (stock-installed*4092)/(average_GW*3.1)
        assert row['static_years'] == pytest.approx(expected)
        assert row['fleet_initial_t']+row['static_years']*row['fleet_burnup_t_year'] == pytest.approx(stock)
        assert row['reference_covers_startup']
    assert budgets['lead_resource_reference']['stock_qualifier'] == '>'
    be = budgets['beryllium_resource_reference']
    assert not be['reference_covers_startup']
    assert be['static_years'] is None  # Never plot negative years or fake a feasible fleet.
    assert be['stock_kind'] == 'resource reference'


def test_energy_scenario_published_fusion_timelines_and_si_scaling():
    outlook = c.energy_scenarios()
    base = next(case for case in outlook['fusion_mit']['cases']
                if case['cost_2050_USD_kW'] == 8000)
    # Text values on MIT report p.42, independent of curve digitization.
    assert base['output_EJ_year'][base['years'].index(2035)] == pytest.approx(2*.0036)
    assert base['output_EJ_year'][base['years'].index(2050)] == pytest.approx(375*.0036)
    assert base['output_EJ_year'][-1] == pytest.approx(24_000*.0036)
    assert outlook['fusion']['output_EJ_year'] == pytest.approx(.21*140*3.6)
    assert outlook['fusion']['scaled_primary_share_percent'] == pytest.approx(
        100*.21*140*3.6/outlook['total_EJ_year']['median'][-1])
    # The independently published 22% × approximately 132 PWh S02 endpoint.
    assert outlook['fusion_etm_timeline']['output_EJ_year'][-1] == pytest.approx(
        .22*132*3.6, abs=.6*3.6)
    for series in outlook['shares_percent'].values():
        assert np.all(np.array(series['p10']) <= np.array(series['median']))
        assert np.all(np.array(series['median']) <= np.array(series['p90']))
    assert sum(outlook['observed']['values'].values()) == 646


def test_energy_ensemble_takes_percentiles_of_shares_before_aggregation(monkeypatch):
    def case(total, coal, bio, nuclear, wind, solar):
        return {'model':'example', 'scenario':str(total), 'category':'C1', 'values':{
            'Primary Energy':[total]*9, 'Primary Energy|Coal':[coal]*9,
            'Primary Energy|Oil':[0]*9, 'Primary Energy|Gas':[0]*9,
            'Primary Energy|Biomass':[bio]*9, 'Primary Energy|Nuclear':[nuclear]*9,
            'Primary Energy|Wind':[wind]*9, 'Primary Energy|Solar':[solar]*9}}
    cases = [case(100,30,20,10,10,20), case(1000,300,100,100,100,100)]
    original = Path.read_text
    def read(path, *args, **kwargs):
        if path.name == 'ar6-primary-energy.jsonl':
            return '\n'.join(json.dumps(case) for case in cases)
        return original(path, *args, **kwargs)
    monkeypatch.setattr(Path, 'read_text', read)
    result = c.energy_scenarios()
    assert result['total_EJ_year']['median'] == pytest.approx([550]*9)
    # Source shares are 30% and 20%, whose median is 25%, not 115/550.
    assert result['shares_percent']['Wind + solar']['median'] == pytest.approx([25]*9)
    assert result['shares_percent']['Wind + solar']['p10'] == pytest.approx([21]*9)
    assert result['shares_percent']['Wind + solar']['p90'] == pytest.approx([29]*9)


def test_energy_scenario_rejects_nonclosing_components(monkeypatch):
    original = json.loads
    def corrupt(source):
        value = original(source)
        if 'values' in value and 'Primary Energy' in value['values']:
            value['values']['Primary Energy|Coal'][0] = 2*value['values']['Primary Energy'][0]
        return value
    monkeypatch.setattr(c.json, 'loads', corrupt)
    with pytest.raises(ValueError, match='do not close'):
        c.energy_scenarios()


def test_solar_current_build_rate_guide():
    solar = c.energy_scenarios()['solar']
    assert solar['added_GW_year'] == pytest.approx(510.349)
    # Independent SI oracle: 1 GW running at 15% for 365 days.
    assert solar['annual_output_increment_EJ_year'] == pytest.approx(
        510.349*1e9*.15*365*24*3600/1e18)
    assert solar['observed_shares_percent'] == pytest.approx(
        [100*2100*.0036/646,100*2700*.0036/655])
    assert solar['guide_years'][0] == 2025
    assert solar['guide_years'][-1] == 2035
    assert solar['guide_shares_percent'][0] == pytest.approx(
        solar['observed_shares_percent'][-1])
    assert solar['guide_output_EJ_year'][-1] == pytest.approx(
        2700*.0036+10*510.349*1e9*.15*31536000/1e18)
