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
