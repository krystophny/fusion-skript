"""Write source/asset records and append the Chapter 0 handoff provenance."""
import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT/'data/ch00'
ACCESS = '2026-10-06'
CC4 = 'https://creativecommons.org/licenses/by/4.0/'
sources = {}


def add(key, title, url, year, licence, terms, status, transform, files=()):
    sources[key] = dict(title=title,source_url=url,access_date=ACCESS,year=year,
        licence=licence,licence_url=terms,release_status=status,transformation=transform,
        snapshot_files=list(files))


add('nasa','Black Marble 2016','https://science.nasa.gov/earth/earth-observatory/earth-at-night/maps/',2016,
    'US government public domain','https://www.nasa.gov/nasa-brand-center/images-and-media/','cleared',
    'Unchanged full-resolution source; separate ≤2400 px JPEG. Composite, not a single instantaneous exposure.')
add('eia','EIA International primary energy consumption','https://api.eia.gov/v2/international/data/',2024,
    'Public domain; acknowledge EIA','https://www.eia.gov/about/copyrights_reuse.php','cleared',
    'Annual productId=44, activityId=2, unit=QBTU. Join ISO3 with WDI GDP/population; filter type c, positive/matching data. Convert IT Btu to J then kWh/person/day with 365-day year. No EI series used.', ['eia_2024.json','eia_2023.json','eia_2025.json'])
for key,indicator,title,files in [
    ('wb_gdp_ppp','NY.GDP.PCAP.PP.KD','GDP per capita PPP, constant 2021 international dollars',['wb_gdp_ppp.json','wb_NY.GDP.PCAP.PP.KD_licence.html']),
    ('wb_population','SP.POP.TOTL','Population, total',['wb_population.json','wb_SP.POP.TOTL_licence.html']),
    ('wb_gdp_austria','NY.GDP.PCAP.CN','Austria GDP per capita, current local currency (EUR)',['wb_austria_gdp_eur.json']),
    ('wb_electricity','EG.ELC.ACCS.ZS','Access to electricity, percent of population',['wb_electricity.json','wb_EG.ELC.ACCS.ZS_licence.html'])]:
    add(key,title,'https://data.worldbank.org/indicator/'+indicator,'2024 scatter; latest available otherwise',
        'CC BY 4.0 as explicitly served by WDI',CC4,'cleared',
        'Use matching 2024 for country plot; latest 2025 population for fusion inventories and deployment. World aggregate is WLD. GDP PPP is not market-exchange-rate GDP. Country/economy metadata excludes World Bank aggregates.',files)
add('wb_cooking','Clean cooking access, WDI EG.CFT.ACCS.ZS','https://data.worldbank.org/indicator/EG.CFT.ACCS.ZS',2023,
    'Specific WDI source note says CC BY-NC 3.0 IGO; excluded despite the blanket CC BY label',
    'https://creativecommons.org/licenses/by-nc/3.0/igo/','excluded-from-cleared-output',
    'No value or series is copied into processed data, plot payloads, the numerical ledger or the chapter. The local research snapshot is ignored by Git. Specific source terms override blanket OWID/WDI terms.', ['wb_cooking.json','wb_cooking_licence.html'])
add('dollarstreet','Four stoves across household living standards','https://www.gapminder.org/dollar-street/about','2014–2019',
    'CC BY 4.0, credit individual photographer',CC4,'cleared',
    'Extract first-party currentThing metadata; income is PPP-adjusted monthly per equivalent adult (modified OECD scale), NOT total monthly household income. Displayed income estimates approximate ±25%. Download images.original; uncropped URLs return 404.',
    ['dollarstreet-5d4bf44ccf0b3a0f3f35b67a.json','dollarstreet-5d4bec73cf0b3a0f3f34df4c.json','dollarstreet-5d4be196cf0b3a0f3f33b4c5.json','dollarstreet-5ec4f926f0611d7ddd7414e9.json'])
add('gapminder_income_levels','World population by four income levels, Factfulness notes p.32','https://www.gapminder.org/factfulness-book/notes/',2017,
    'CC BY 4.0; Factfulness notes version 3 and Gapminder estimates','https://www.gapminder.org/free-material/','cleared-attributed-data',
    'Transcribed the four rounded 2017 population estimates; thresholds are 2011 PPP USD/person/day. Counts derive from PovcalNet 2013 and Gapminder extensions/IMF forecasts, not a current survey.',
    ['gapminder_income_levels_2017.json'])
add('legacy_handwriting','Chris bottom-up estimate and stock scenarios',
    'local:instructor-provided-2025-lecture-material','2025, rendered pp.10/14/29',
    'Lecturer original handwritten calculations; original teaching content CC BY 4.0',CC4,'cleared-own-calculations-only',
    'Transcribe handwriting independently; do not reuse underlying legacy pages, book charts, maps or photographs. All 35 pages inspected via rendered contact sheets; pages 10/14/29 also full size. No legacy page/image copied to repo.')
stat_terms='https://www.statistik.at/en/about-us/responsibilities-and-principles/legal-basis/website-information'
add('stat_balance','Preliminary Austrian energy balance in TJ',
    'https://www.statistik.at/fileadmin/pages/99/preliminaryEnergyBalancesforAustriaInTerajoule.ods',2025,
    'Custom permission: accurate attributed reproduction/distribution/processing; not a named CC licence',stat_terms,'attributed-data-reuse',
    'Extract Balance rows 3–19; AL total column (37 zero-based). Sankey uses aggregate coal/oil/gas/renewables/waste plus net-electricity imports. Transformation input minus output is net loss; final carrier × sector cells retained. Mark partial/processed and preliminary. data.statistik.gv.at CC terms do not automatically cover this ODS.',
    ['austria_2025.ods','austria_2025_cells.json','statistik_reuse.html'])
add('stat_population','Austria annual-average population',
    'https://www.statistik.at/en/statistics/population-and-society/population/population-stock/annual-average-population',2025,
    'Same custom Statistics Austria attributed-reuse permission',stat_terms,'attributed-data-reuse',
    'Use pre-existing project-authoritative 9204460.875 annual-average value, compiled 2026-06-29; do not replace with year-end WDI population. Existing data/energy.json remains unchanged.')
add('bgr','BGR Energiedaten 2025, data 2024',
    'https://www.bgr.bund.de/DE/Themen/Rohstoffe/Downloads/Downloads_EN/Energiedaten/energiedaten_2025.xlsx?__blob=publicationFile&v=3',2024,
    'BGR workbook is free to download; BGR graphics carry a separate CC BY notice. Numerical data are re-plotted with attribution per lecturer data-reuse policy; no CC licence is asserted for the workbook.',
    'https://www.bgr.bund.de/DE/Themen/Rohstoffe/Produkte/Energiedaten/energiedaten_inhalt.html','attributed-data-reuse',
    'World rows of A-10/11 oil, A-17/18 gas, A-23 hard coal, A-30 lignite, A-35 uranium. Production 2024 is H, not C, in time-series sheets. Uranium reserves are low-cost RAR <USD80/kg; broad Red Book identified resources separate. Native mass/volume R/P; published rounded EJ for inventory-power scenarios.',
    ['bgr_2025.xlsx','bgr_2024.xlsx','bgr_figures.html'])
add('redbook','IAEA/NEA Uranium 2024 (2025 publication)',
    'https://www.oecd-nea.org/upload/docs/application/pdf/2025-04/7683_uranium_2024_-_resources_production_and_demand_2025-04-22_14-29-2_928.pdf',
    'Resources 2023-01-01 / production 2023','CC BY 4.0, explicit publication front matter',CC4,'cleared',
    'Identified recoverable RAR + inferred: 7,934,500 tU <USD260/kg and 5,925,700 tU <USD130/kg. Reported/provisional 2023 production 54,345 tU. Resource/P is not reserve/P. Apply independently derived once-through cycle energy per kg; no book figure reproduced.', ['uranium-redbook-2024.pdf'])
add('pvgis','JRC PVGIS 5.3 SARAH3/ERA5 Graz',
    'https://re.jrc.ec.europa.eu/api/v5_3/PVcalc?lat=47.0707&lon=15.4395&peakpower=1&loss=14&angle=35&aspect=0&outputformat=json',
    '2005–2023','Free reuse with attribution, JRC PVGIS usage conditions',
    'https://joint-research-centre.ec.europa.eu/photovoltaic-geographical-information-system-pvgis/general-information/usage-conditions-data-protection_en',
    'attributed-data-reuse; not labelled CC',
    'MRcalc horirrad=1 optrad=1 selectrad=1 angle=35 d2g=1 avtemp=1. Sum 12 monthly horizontal means across 19 years. PVcalc 35° south, free-standing c-Si, 1 kWp, 14% system losses. Satellite-derived irradiation and modelled yield, not measured station/park output. Divide kWh/m²/year by 8760 h then ×1000.',
    ['pvgis_graz.json','pvgis_graz_horizontal.json'])
add('enbw_weesow','Weesow-Willmersdorf solar park operator commissioning facts',
    'https://www.enbw.com/press/enbw-inaugurates-germany-s-largest-solar-park.html',2021,
    'Operator publication copyright; numerical facts only, no press image', '', 'numeric-facts-only',
    '187 MWp, 164 ha, 180 million kWh/year expected. Derive site-boundary average and 1 GW area. Expected output is NOT a measured annual yield.')
add('graz_boundary','Graz municipal boundary OGD',
    'https://geodaten.graz.at/arcgis/rest/services/OGD/OGD_WFS/MapServer/12/query?where=1%3D1&outFields=*&outSR=4326&f=geojson',2026,
    'CC BY 4.0; Datenquelle: Stadt Graz – data.graz.gv.at','https://data.graz.gv.at/graz/nutzungsbedingungen/','cleared',
    'Project boundary to EPSG32633; subtract centroid in metres, never rescale. Geometry area 127.466 km²; published city area 127.58 km² (https://www.graz.at/cms/beitrag/10034466/7772565/Zahlen_Fakten_Bevoelkerung_Bezirke_Wirtschaft.html). No OSM/ODbL data used.', ['graz_boundary.geojson','graz_boundary_layer.json','graz_terms.html'])
add('sentinel','Sentinel-2A L2A true colour 2025-09-11',
    'https://earth-search.aws.element84.com/v1/search','2025-09-11',
    'Copernicus free/open Sentinel data policy','https://cds.climate.copernicus.eu/licences/ec-sentinel','compatible-custom-open; requested Copernicus credit',
    'POST STAC collection sentinel-2-l2a, bbox [13.66,52.62,13.73,52.69], June–September 2025. Chosen S2A_33UVU_20250911_0_L2A, cloud 1.469683%. Read public assets.visual COG without credentials; crop native 10 m 16 km and 5 km windows. No synthetic replacement. Credit: Contains modified Copernicus Sentinel data 2025.',
    ['sentinel_selected.json','sentinel_park_search_all.json'])
add('wikidata','Approximate park reference point','https://www.wikidata.org/wiki/Q71147169',2026,
    'CC0','https://creativecommons.org/publicdomain/zero/1.0/','cleared','52.650568°N, 13.686692°E; approximate centre for imagery window, not surveyed park polygon.')
add('owid_prices','Solar PV module price series','https://ourworldindata.org/grapher/solar-pv-prices','1975–2024',
    'OWID processing CC BY 4.0; Nemet/SFI CC BY 3.0, Farmer/Lafond CC BY 4.0; IRENA 2025 report permits free attributed reuse and bears © IRENA 2025; pvXchange benchmark credited',
    'https://www.irena.org/Publications/2025/Jun/Renewable-Power-Generation-Costs-in-2024','cleared-attributed-data',
    'Saved indicator 1305867 and metadata distinguish source licences. Prices constant 2025 USD/Wp. Global estimates through 2009; European pvXchange module benchmark thereafter. Module price, not installed cost.',
    ['solar-pv-prices.csv','solar-pv-prices.metadata.json','indicator-1305867.json'])
add('irena_capacity','Explicit photovoltaic capacity, IRENA 2026',
    'https://www.irena.org/Publications/2026/Mar/Renewable-capacity-statistics-2026','2016–2025',
    '© IRENA 2026; publication explicitly permits free reuse with attribution; no named CC asserted',
    'https://www.irena.org/-/media/Files/IRENA/Agency/Publication/2026/Mar/IRENA_DAT_RE_capacity_statistics_2026.pdf','cleared-attributed-data',
    'Explicit Solar photovoltaic world/Austria table, years 2016–2025, MW at year end. March table differs from later July OWID dataset. OWID installed-solar-pv-capacity slug now includes CSP; not used as PV-only. Notice: © IRENA 2026.', ['irena_capacity_2026.pdf','installed-solar-pv-capacity.csv','installed-solar-pv-capacity.metadata.json','indicator-1305908.json'])
add('miller_corrigendum','Corrected empirical US wind/solar power densities',
    'https://doi.org/10.1088/1748-9326/aaf9cf',2016,'CC BY 3.0 (2019 publication)',
    'https://creativecommons.org/licenses/by/3.0/','cleared',
    'Corrected capacity-weighted means: wind 0.90 W/m² (430 plants), solar 5.7 W/m² (1047 plants). Original 0.50 / 5.4 values superseded. Wind Voronoi area and solar assumed capacity-density methodology differ; preserve boundary caveat.', ['wind_corrigendum.pdf'])
add('windeurope','Wind energy in Europe, 2024 statistics',
    'https://windeurope.org/intelligence-platform/product/wind-energy-in-europe-2024-statistics-and-the-outlook-for-2025-2030/',2024,
    'Copyright WindEurope; no explicit CC verified','', 'numeric-facts-only',
    'Page 20 EU fleet annual CF: onshore 23%, offshore 35%, all 24%. New-farm estimates onshore 30–35%, offshore 42–55%. Facts quoted, no provider chart copied.', ['windeurope-2024.pdf'])
add('igwind','Austria wind year-end 2025','https://www.igwindkraft.at/',2025,
    'Copyright IG Windkraft; numerical facts only','', 'numeric-facts-only',
    'Actual year-end homepage: 1447 turbines, 4221 MW. Do not use older forecast brochure 1516 turbines / 4392 MW or potential annual output 9.7 TWh as measured generation.', ['igwind_2025.html'])
add('vattenfall_hornsrev','Horns Rev 1 current operator facts',
    'https://powerplants.vattenfall.com/de/horns-rev/',2026,
    'Operator copyright; numerical facts only','', 'numeric-facts-only',
    '20 km², current 158 MW, 80 turbines. Multiplying by EU fleet 35% gives a scenario 2.765 W/m², not a measured Horns Rev yield.', ['hornsrev_operator.html'])
add('bml_area','Austria Facts & Figures 2024',
    'https://www.bmluk.gv.at/dam/jcr%3A1e1f491f-bbfb-4387-9c3f-061a38578b94/BML_Broschuere_Zahlen_und_Fakten_EN_2024_BF_V02.pdf',2024,
    'Government publication; numerical geographical fact only','', 'numeric-facts-only','Use published Austria area 83,884 km²; no map/page reproduced.')
add('wna_fuel','Nuclear fuel-cycle benchmark','https://world-nuclear.org/information-library/nuclear-fuel-cycle/introduction/nuclear-fuel-cycle-overview',2026,
    'WNA copyright; numerical facts/assumptions only','', 'numeric-facts-only',
    'Independently solve mass and isotope balances using 45 GWd/t heavy-metal burnup, 33% efficiency, 4.5% product, 0.711% natural feed, 0.22% tails. Full power year, not initial core. Compare rounded WNA 24.3 t enriched / 211 t natural U within rounding.')
add('iaea_history','Nuclear Power Reactors in the World 2025, table 7',
    'https://www-pub.iaea.org/MTCD/Publications/PDF/RDS-2-45_web.pdf','1954–2024',
    'No explicit CC licence found in report; numerical facts only','', 'numeric-facts-only',
    'Extract latest available 2025 table 7, covering 1954–2024; compute maxima with SymPy. First grid connections 33 in both 1984/1985; construction starts 43 in 1976; max connected capacity 31,129 MWe in 1985. 2024 connections 6 / 6803 MWe. Historical MW values were revised since 2014; use current edition.', ['iaea-reactors-2025.pdf','iaea-history-1954-2024.json','iaea-reactors-2014.pdf'])
add('kkg','Gösgen technical main data','https://www.kkg.ch/de/technik/technische-hauptdaten.html',2026,
    'Operator copyright; numerical facts only','', 'numeric-facts-only','Net 1010 MWe, gross 1060 MWe, thermal 3002 MW; use CC-licensed Commons photo, not operator press photo.')
add('iaea_fusion','IAEA fusion physics FAQ','https://www.iaea.org/topics/energy/fusion/faqs','physical value',
    'Numerical physical fact; no illustration reused','', 'numeric-facts-only','D–T Q=17.6 MeV, rounded total neutron+alpha kinetic energy.')
add('nist_constants','NIST CODATA 2022','https://physics.nist.gov/cuu/Constants/','2022 / exact SI 2019',
    'US government public domain','https://www.nist.gov/open/license','cleared','Atomic mass 1.66053906892e-27 kg; e=1.602176634e-19 C exact, used for eV→J.')
add('nist_isotopes','NIST atomic weights / hydrogen isotopes',
    'https://physics.nist.gov/cgi-bin/Compositions/stand_alone.pl?ele=H','NIST tabulation',
    'US government public domain','https://www.nist.gov/open/license','cleared','D 2.01410177812 u; T 3.0160492779 u; molecular water model 18.01528 u. Atomic rather than bare-nucleus masses change fuel mass negligibly at teaching precision.')
add('nist_units','NIST SP811 unit conversion','https://www.nist.gov/pml/special-publication-811','definition',
    'US government public domain','https://www.nist.gov/open/license','cleared','International Table Btu=1055.05585262 J, not thermochemical Btu.')
add('nist_vsmow','NIST TN1900 VSMOW isotope reference','https://tsapps.nist.gov/publication/get_pdf.cfm?pub_id=919610','VSMOW reference',
    'US government public domain','https://www.nist.gov/open/license','cleared','D/H atomic ratio 155.76e-6; D fraction is r/(1+r), with two H sites per water molecule. Seawater variation neglected in inventory estimate.')
add('noaa_ocean','NOAA ocean volume','https://oceanservice.noaa.gov/facts/oceanwater.html',2026,
    'US government public domain','https://www.noaa.gov/disclaimer','cleared','Ocean volume 1.335 billion km³; multiply model D concentration, not an extraction reserve.')
add('usgs_lithium','USGS MCS 2026 lithium','https://pubs.usgs.gov/periodicals/mcs2026/mcs2026-lithium.pdf',2025,
    'US government public domain','https://www.usgs.gov/information-policies-and-instructions/copyrights-and-credits','cleared',
    'World Li reserves 37 Mt elemental Li; production 290 kt excludes withheld US value. Reserve is not all Li-6, nor recoverable tritium fuel.', ['usgs-lithium-2026.pdf'])
add('assumptions','Explicit lecturer/model assumptions','repo:derivations/chapters/ch00_energy_context.py','model',
    'Original teaching derivations CC BY 4.0; code MIT',CC4,'cleared-own',
    '365-day year; PV efficiency 20%; densities 0.5/2/10/20 W/m²; coal LHV 24 MJ/kg; seawater 1025 kg/m³, water fraction 0.965; 30-year deployment, 90% nuclear CF. These are scenario assumptions, not observed universal constants.')
add('faostat_arable','Arable land per person, FAO via World Bank WDI','https://ourworldindata.org/grapher/arable-land-use-per-person','2023',
    'FAO database default CC BY 4.0; WDI and OWID processing CC BY 4.0',
    'https://www.fao.org/contact-us/terms/db-terms-of-use/en','cleared-attributed-data',
    'World and Austria 2023, hectares per person. Values are replotted independently; credit FAO, World Bank and OWID processing.',
    ['arable-land-use-per-person.csv','arable-land-use-per-person.metadata.json'])
add('hyde_cropland','Cropland per person, PBL HYDE 3.5 via OWID','https://ourworldindata.org/grapher/cropland-per-person-over-the-long-term','2023',
    'OWID processing CC BY 4.0; source PBL HYDE 3.5 has no separate licence identified in available metadata',
    'https://ourworldindata.org/how-to-use-our-world-in-data','attributed-data-with-source-terms-recorded',
    'World and Austria 2023, hectares per person. Cropland comprises arable plus permanent crops; credit PBL/HYDE and OWID processing. No standalone CC licence asserted for HYDE.',
    ['cropland-per-person-over-the-long-term.csv','cropland-per-person-over-the-long-term.metadata.json'])
add('usda_corn','US corn yield, USDA NASS Crop Production 2024 Summary','https://www.nass.usda.gov/Publications/Todays_Reports/reports/cropan26.pdf',2024,
    'US federal government public domain','https://www.usda.gov/policies-and-links','cleared-numeric-data',
    'National corn average yield 179.3 bushels/acre. Used only as an illustrative gross energy-per-cropland-area factor.', ['usda-corn-yield-2024.pdf'])
add('doe_ethanol','Ethanol output and lower heating value, US DOE AFDC','https://afdc.energy.gov/files/u/publication/ethanol_basics.pdf','reference',
    'US federal government public domain','https://www.energy.gov/copyright-and-license','cleared-numeric-data',
    'Dry-mill ethanol output 2.8 gal/bushel and pure ethanol LHV 76,330 Btu/gal. Farm/distillery energy and coproduct credit are excluded.',
    ['doe-us-ethanol-industry.pdf','doe-ethanol-basics.pdf'])
add('loss_cats','Free-ranging domestic cat bird mortality, Loss et al. 2013 corrected','https://doi.org/10.1038/ncomms2380','2013 corrected 2014',
    'Only factual estimates re-plotted; source article rights remain separate','https://www.nature.com/articles/ncomms3961','numeric-facts-only',
    'Corrected estimate 1.3–4.0 billion birds/year in contiguous US from free-ranging cats; a model estimate, not a count.')
add('loss_buildings','Bird-building collisions, Loss et al. 2014','https://doi.org/10.1650/CONDOR-13-090.1',2014,
    'Only numerical facts re-plotted; source article rights remain separate','https://academic.oup.com/journals/pages/open_access/funder_policies/chorus/standard_publication_model','numeric-facts-only',
    'United States annual estimate 365–988 million, median 599 million.')
add('loss_vehicles','Bird-vehicle collisions, Loss et al. 2014','https://doi.org/10.1002/jwmg.721',2014,
    'Only numerical facts re-plotted; source article rights remain separate','https://onlinelibrary.wiley.com/terms-and-conditions','numeric-facts-only',
    'United States road estimate 89–340 million birds/year.')
add('loss_powerlines','Power-line bird mortality, Loss et al. 2014','https://doi.org/10.1371/journal.pone.0101565',2014,
    'CC0','https://creativecommons.org/publicdomain/zero/1.0/','cleared-numeric-data',
    'United States collision plus electrocution estimate 12–64 million birds/year; no source figure reproduced.')
add('loss_wind','Bird mortality at US wind facilities, Loss et al. 2013','https://doi.org/10.1016/j.biocon.2013.10.007',2013,
    'Only numerical facts re-plotted; source article rights remain separate','https://www.elsevier.com/about/policies-and-standards/copyright','numeric-facts-only',
    'Contiguous US monopole turbine estimate 140,438–327,586 deaths/year; mean 234,012.')
add('naturvardsverket_birds','European wind-farm mortality synthesis, Vindval Report 6511','https://www.naturvardsverket.se/4ac35d/globalassets/media/publikationer-pdf/ovriga-pub/vindval/978-91-620-6511-9.pdf',2012,
    'Swedish Environmental Protection Agency review; numerical fact only','https://www.naturvardsverket.se/publikationer/','numeric-facts-only',
    'Median 6.5 birds/turbine/year across reviewed European wind farms; site estimates are heterogeneous and skewed, not a Europe-wide total.')
add('owid_deaths','Deaths per TWh electricity, OWID compilation','https://ourworldindata.org/grapher/death-rates-from-energy-production-per-twh',2021,
    'OWID processing CC BY 4.0; cited underlying evidence has varied boundaries','https://ourworldindata.org/how-to-use-our-world-in-data','cleared-attributed-data-with-method-caveat',
    'Markandya & Wilkinson (2007), Sovacool et al. (2016), UNSCEAR (2008/2018); air-pollution and accident estimates combined. Original plot only.',
    ['death-rates-from-energy-production-per-twh.csv','death-rates-from-energy-production-per-twh.metadata.json'])
add('ipcc_candidate','IPCC AR5 WGIII Annex III lifecycle emissions candidate','https://www.ipcc.ch/site/assets/uploads/2018/02/ipcc_wg3_ar5_annex-iii.pdf',2014,
    'IPCC default terms limit reuse to personal non-commercial use; excluded under course rule','https://www.ipcc.ch/copyright/','excluded-from-cleared-output',
    'Checked Table A.III.2 values and then excluded the series because published reuse terms are non-commercial; no IPCC numbers or figure are in processed outputs.')
add('nrel_lifecycle','Life Cycle Emissions Factors for Electricity Generation Technologies','https://data.nlr.gov/submissions/171','dataset updated 2026-05-22; source report 2021',
    'DOE/NREL/ALLIANCE custom terms permit free use/copy with the full notice attached and require publication credit; no CC licence asserted',
    'https://data.nlr.gov/node/171/license','attributed-data-reuse',
    'Subset of total lifecycle min/median/max columns W/Y/AA for nine technology groups. Own plot; no source figure reproduced. Credit DOE/NREL/ALLIANCE. The full source notice is embedded in the processed CSV and each plot-data output.',
    ['nrel-lifecycle-emissions-2026.xlsx','nrel-lifecycle-license.html'])
sources['nrel_lifecycle']['data_use_notice_file'] = 'data/ch00/processed/nrel-lifecycle-notice.txt'
add('who_cooking_candidate','OWID WHO clean-cooking grapher',
    'https://ourworldindata.org/grapher/access-to-clean-fuels-and-technologies-for-cooking',2023,
    'WHO CC BY-NC-SA 4.0; OWID processing CC BY 4.0 does not override it',
    'https://creativecommons.org/licenses/by-nc-sa/4.0/','excluded-from-cleared-output',
    'Research candidate only. Original WHO indicator licence verified in OWID source metadata; do not relabel CC BY.',
    ['access-to-clean-fuels-and-technologies-for-cooking.csv','access-to-clean-fuels-and-technologies-for-cooking.metadata.json','indicator-1255654.json'])
add('ei_candidate','OWID energy/GDP original candidate','https://ourworldindata.org/grapher/energy-use-per-person-vs-gdp-per-capita','2026 edition',
    'OWID own processing CC BY 4.0; underlying Energy Institute copyright',
    'https://www.energyinst.org/statistical-review','excluded-from-cleared-output',
    'Saved for comparison only. EIA public-domain alternative used instead. OWID licensing cannot override EI source terms.', ['owid_energy.csv','owid_energy_codebook.csv','energy-use-per-person-vs-gdp-per-capita.csv','energy-use-per-person-vs-gdp-per-capita.metadata.json','indicator-1295475.json'])

if __name__ == '__main__':
    (BASE/'sources.json').write_text(json.dumps(sources,indent=2,ensure_ascii=False)+'\n')
    manifest = []
    for p in sorted((BASE/'raw').iterdir()):
        rel=str(p.relative_to(ROOT))
        ignored=subprocess.run(['git','check-ignore','-q',rel],cwd=ROOT,
            stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL).returncode==0
        if p.is_file() and not ignored:manifest.append({'file':rel,'bytes':p.stat().st_size,
            'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),
            'source_keys':[k for k,r in sources.items() if p.name in r['snapshot_files']],
            'release_status':'RESEARCH EVIDENCE ONLY: not automatically cleared for public distribution'})
    (BASE/'raw-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print(f'Wrote {len(sources)} source records and {len(manifest)} evidence hashes.')
