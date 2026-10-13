"""Preserve the supplied cost tables and reproduce the daily-storage model.

Input prices: PV electricity in US cents/kWh, usable storage capacity in USD/kWh.
Output: constant-2025-dollar plotting data, with explicit evidence classifications.
"""
import csv
import json
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT/'data/ch00/raw/cost-sourcebook'
AUDIT = ROOT/'data/ch00/processed/electricity-cost-audit.json'
OUT = ROOT/'derivations/build/plotdata/09-electricity-cost-history.json'

# Cost per delivered kWh: direct PV + loss-adjusted PV charging + annualised battery.
c_pv, f, eta, B, r, T, m, cycles = sp.symbols('c_PV f eta B r T m u', positive=True)
crf = r/(1-(1+r)**(-T))
daily_cost = c_pv*((1-f)+f/eta) + 100*f*B*(crf+m)/(365*cycles)
zero_discount_crf = sp.limit(crf, r, 0)


def storage_cost(pv_cents, capex, efficiency=.85, lifetime=15, shifted=.60,
                 discount=.07, maintenance=.01, utilisation=.95):
    return float(daily_cost.subs({c_pv:pv_cents, B:capex, eta:efficiency,
        T:lifetime, f:shifted, r:discount, m:maintenance, cycles:utilisation}))


def read_table(name, value_key=None, series_key=None):
    with (RAW/name).open(newline='') as stream:
        rows = list(csv.DictReader(stream))
    keys = set()
    for row in rows:
        if 'year' in row:
            row['year'] = int(row['year'])
        if value_key:
            row[value_key] = float(row[value_key])
            if row[value_key] <= 0:
                raise ValueError(f'Non-positive log-chart value: {row}')
        if series_key:
            key = row['year'], row[series_key]
            if key in keys:
                raise ValueError(f'Duplicate cost record: {key}')
            keys.add(key)
    return rows



def cost_projections(annual):
    """Apply relative technology-cost scenarios to the 2025 benchmarks.

    ATB nuclear estimates start in 2030. The anchored nuclear scenario holds
    real cost constant until then and applies subsequent ATB relative changes.
    Gas and coal retain the explicitly labelled constant-real-cost reference.
    """
    with (ROOT/'data/ch00/raw/atb-2025-projections.csv').open(newline='') as stream:
        inputs = list(csv.DictReader(stream))
    technology = {'LandbasedWind':'onshore_wind', 'Nuclear':'nuclear_fission_new'}
    reference_years = {'LandbasedWind':2025, 'Nuclear':2030}
    reference_values = {tech:float(next(r for r in inputs
        if r['technology']==tech and int(r['core_metric_variable'])==year)['value'])
        for tech,year in reference_years.items()}
    benchmarks = {tech:next(r for r in annual
        if r['technology']==tech and r['year']==2025) for tech in technology.values()}
    rows = []
    for row in inputs:
        if row['units'] != '$/MWh' or row['scenario'] != 'Moderate' or row['core_metric_case'] != 'R&D':
            raise ValueError('Unexpected ATB projection assumptions')
        year = int(row['core_metric_variable'])
        if year == 2025:
            continue
        tech = row['technology']
        base = benchmarks[technology[tech]]
        rows.append({
            'year':year, 'technology':technology[tech],
            'us_cents_per_kWh_2025':base['us_cents_per_kWh_2025']*float(row['value'])/reference_values[tech],
            'source_ids':'ATB2025;'+base['source_ids'],
            'evidence_flag':'F', 'geography':base['geography'],
            'atb_recovery_years':int(row['crpyears']),
            'atb_reference_year':reference_years[tech],
            'scenario':'2025 benchmark multiplied by ATB relative cost change'
                + ('; assumed constant real cost to 2030' if tech=='Nuclear' else '')})
    for tech in ('natural_gas_CCGT','coal'):
        base = next(r for r in annual if r['technology']==tech and r['year']==2025)
        for year in (2030,2035):
            rows.append({**base, 'year':year, 'evidence_flag':'F',
                'scenario':'Constant 2025 real cost; no fuel/carbon-price forecast'})
    if {(r['technology'],r['year']) for r in rows} != {
            (tech,year) for tech in (*technology.values(),'natural_gas_CCGT','coal')
            for year in (2030,2035)} or len(rows) != 8:
        raise ValueError('Incomplete or duplicate projection inputs')
    return rows



def payload():
    annual = read_table('annual-electricity-costs.csv', 'us_cents_per_kWh_2025', 'technology')
    components = read_table('component-costs.csv', 'value', 'series')
    sources = read_table('sources.csv')
    annual.extend(cost_projections(annual))
    sources.append({'source_id':'ATB2025', 'title':'2025 Annual Technology Baseline',
        'coverage':'Moderate R&D relative cost changes, no tax credits, anchored at 2025 benchmarks; wind Class 4 / turbine 1, 30-year recovery; large nuclear, 60-year recovery, held flat to 2030 then ATB changes relative to 2030',
        'url':'https://atb.nlr.gov/electricity/2025/data'})
    audit = json.loads(AUDIT.read_text())
    for change in audit['corrections']:
        row = next(row for row in components if
            (row['year'], row['series']) == (change['year'], change['series']))
        if row['evidence_flag'] != change['reported_evidence_flag']:
            raise ValueError('Sourcebook classification changed; review audit correction')
        row['reported_evidence_flag'] = row['evidence_flag']
        row['evidence_flag'] = change['evidence_flag']
        row['audit_note'] = change['reason']

    pv = {row['year']:row['us_cents_per_kWh_2025'] for row in annual if row['technology']=='solar_PV'}
    costs = {(row['year'],row['series']):row['value'] for row in components}
    checks = []
    for row in annual:
        if row['technology'] != 'solar_daily_shift':
            continue
        year = row['year']
        if year <= 2025:
            lead = storage_cost(pv[year],costs[year,'lead_BESS_turnkey_usable_scenario'],.75,5)
            lithium = (storage_cost(pv[year],costs[year,'Li_BESS_turnkey_4h_global'])
                if year >= 2010 else float('inf'))
            computed = min(lead,lithium)
        else:
            # Sourcebook §3.1, IRENA scenario input ratios, not global LCOE forecasts.
            pv_capex, bess_capex = {2030:(412,132),2035:(359,114)}[year]
            future_pv = 4.4*(.35+.65*pv_capex/658)
            computed = storage_cost(future_pv,140*bess_capex/171)
        checks.append({'year':year,'reported':row['us_cents_per_kWh_2025'],
            'recomputed':computed,'difference':computed-row['us_cents_per_kWh_2025']})
    return {'sourcebook_date':'2026-10-09','annual':annual,'components':components,
        'regional_cases':read_table('regional-95pct.csv'),'sources':sources,
        'audit_notes':audit,'daily_shift_model':{
            'formula':str(daily_cost),'crf':str(crf),'zero_discount_crf':str(zero_discount_crf),
            'assumptions':json.loads((RAW/'manifest.json').read_text())['daily_shift_model'],
            'checks':checks,'maximum_absolute_difference':max(abs(row['difference']) for row in checks)}}


def build():
    data = payload()
    # Inputs and target costs are independently rounded to four decimals in the sourcebook.
    delta = data['daily_shift_model']['maximum_absolute_difference']
    if delta > .001:
        raise ValueError(f'Daily-storage model disagrees with sourcebook by {delta:g} cents/kWh')
    OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
    print(f'Cost sourcebook: {len(data["annual"])} annual and {len(data["components"])} component records; '
        f'daily-model rounding discrepancy ≤ {delta:.4g} cents/kWh.')


if __name__=='__main__':
    build()
