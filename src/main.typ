#import "theme.typ": page-shell, frame-style, styles
#import "chapters/00-energy-context.typ": chapter
#show: frame-style(styles.boxy)
#set text(font: "STIX Two Text")
#show math.equation: set text(font: "STIX Two Math")
#document("index.html", title: [Fusion Physics])[
  #page-shell(root: true)[
    #html.h1[Fusion Physics]
    #html.p[Christopher Albert, TU Graz. Incremental draft, 5 October 2026.]
    #html.section(id: "contents")[
      #html.h2[Contents]
      #link("chapters/00-energy-context.html")[0. Energy context]
      #html.p[Further chapters follow the established lecture sequence and are added after checking.]
      #link("fusion-physics.pdf")[PDF] #h(1em)
      #link("slides/00-energy-context.pdf")[Live deck]
    ]
    #html.section(id: "glossary")[
      #html.h2[Notation]
      #html.p[SI units; E energy in J, P power in W, N people, q_A delivered power density in W/m².]
    ]
    #html.section(id: "bibliography")[
      #html.h2[Sources]
      #html.p[Method: David MacKay, #link("https://www.withouthotair.com/")[Sustainable Energy—Without the Hot Air] (2009), conceptual reference only; no figures or pages reproduced.]
      #html.p[Income, energy and land: #link("https://www.eia.gov/opendata/browser/international/total-energy/data")[U.S. EIA International Energy Data]; World Bank #link("https://data.worldbank.org/indicator/NY.GDP.PCAP.PP.KD")[GDP PPP], #link("https://data.worldbank.org/indicator/SP.POP.TOTL")[population] and #link("https://data.worldbank.org/indicator/EG.ELC.ACCS.ZS")[electricity access]; #link("https://www.gapminder.org/fw/income-levels/")[Gapminder four income levels] and #link("https://www.gapminder.org/factfulness-book/notes/")[Factfulness notes, p. 32, CC BY 4.0]; #link("https://www.fao.org/contact-us/terms/db-terms-of-use/en")[FAO database terms]; #link("https://ourworldindata.org/grapher/cropland-per-person-over-the-long-term")[PBL HYDE cropland via OWID]; #link("https://www.gapminder.org/dollar-street/about")[Gapminder Dollar Street].]
      #html.p[Austrian energy and area: #link("https://www.statistik.at/fileadmin/pages/99/preliminaryEnergyBalancesforAustriaInTerajoule.ods")[Statistics Austria preliminary 2025 balance]; #link("https://www.statistik.at/en/about-us/responsibilities-and-principles/legal-basis/website-information")[Statistics Austria reuse terms]; #link("https://www.bgr.bund.de/DE/Themen/Rohstoffe/Produkte/Energiedaten/energiedaten_inhalt.html")[BGR Energiedaten]; #link("https://www.oecd-nea.org/upload/docs/application/pdf/2025-04/7683_uranium_2024_-_resources_production_and_demand_2025-04-22_14-29-2_928.pdf")[IAEA/NEA Uranium 2024].]
      #html.p[Solar and wind: #link("https://joint-research-centre.ec.europa.eu/photovoltaic-geographical-information-system-pvgis/general-information/usage-conditions-data-protection_en")[EU JRC PVGIS terms]; #link("https://www.enbw.com/press/enbw-inaugurates-germany-s-largest-solar-park.html")[EnBW Weesow-Willmersdorf]; #link("https://cds.climate.copernicus.eu/licences/ec-sentinel")[Copernicus Sentinel data terms]; #link("https://data.graz.gv.at/graz/nutzungsbedingungen/")[Stadt Graz OGD terms]; #link("https://windeurope.org/intelligence-platform/product/wind-energy-in-europe-2024-statistics-and-the-outlook-for-2025-2030/")[WindEurope 2024]; #link("https://doi.org/10.1088/1748-9326/aaf9cf")[Miller and Keith, corrected wind/solar densities].]
      #html.p[Prices and lifecycle emissions: #link("https://ourworldindata.org/grapher/solar-pv-prices")[OWID solar module price series]; #link("https://www.irena.org/Publications/2025/Jun/Renewable-Power-Generation-Costs-in-2024")[IRENA Renewable Power Generation Costs 2024]; #link("https://www.irena.org/Publications/2026/Mar/Renewable-capacity-statistics-2026")[IRENA Renewable Capacity Statistics 2026]; #link("https://data.nlr.gov/submissions/171")[DOE/NREL/ALLIANCE lifecycle emissions dataset] and its #link("https://data.nlr.gov/node/171/license")[reuse terms].]
      #html.p[Wildlife and health: Loss et al., #link("https://doi.org/10.1038/ncomms2380")[free-ranging cats] and #link("https://www.nature.com/articles/ncomms3961")[correction]; Loss et al., #link("https://doi.org/10.1650/CONDOR-13-090.1")[building collisions], #link("https://doi.org/10.1002/jwmg.721")[vehicle collisions] and #link("https://doi.org/10.1371/journal.pone.0101565")[power lines]; Loss et al., #link("https://doi.org/10.1016/j.biocon.2013.10.007")[wind facilities]; #link("https://www.naturvardsverket.se/4ac35d/globalassets/media/publikationer-pdf/ovriga-pub/vindval/978-91-620-6511-9.pdf")[Naturvårdsverket Vindval 6511]; #link("https://ourworldindata.org/grapher/death-rates-from-energy-production-per-twh")[Our World in Data deaths per TWh].]
      #html.p[Fission and fusion: #link("https://world-nuclear.org/information-library/nuclear-fuel-cycle/introduction/nuclear-fuel-cycle-overview")[World Nuclear Association fuel-cycle overview]; #link("https://www-pub.iaea.org/MTCD/Publications/PDF/RDS-2-45_web.pdf")[IAEA reactor history]; #link("https://www.kkg.ch/de/technik/technische-hauptdaten.html")[Gösgen technical data]; #link("https://www.iaea.org/topics/energy/fusion/faqs")[IAEA fusion FAQ]; #link("https://physics.nist.gov/cuu/Constants/")[NIST constants]; #link("https://pubs.usgs.gov/periodicals/mcs2026/mcs2026-lithium.pdf")[USGS lithium].]
    ]
    #html.p[Original content CC BY 4.0; code MIT; fonts SIL OFL. AI tools assisted drafting and layout; scientific review: Christopher Albert.]
  ]
]
#document("chapters/00-energy-context.html", title: [Energy context])[
  #page-shell(stylesheet: "../styles.css")[#chapter]
]
#asset("styles.css", read("styles.css"))
#for name in ("STIXTwoMath-Regular", "STIXTwoText-Regular", "STIXTwoText-Italic", "STIXTwoText-Bold", "STIXTwoText-BoldItalic") {
  asset("fonts/" + name + ".otf", read("../fonts/" + name + ".otf", encoding: none))
}
#asset("fonts/OFL.txt", read("../fonts/OFL.txt"))
