#import "../theme.typ": *

#let chapter = [
#page-title(number: 3)[Fusion in stars] <fusion-in-stars>
#lead[Stars burn hydrogen through chains of reactions whose slowest step,
the weak p–p reaction, sets their lifetime.]

#section-title[Proton–proton chain] <fusion-pp-chain>
The Sun fuses hydrogen through the p–p chain. In its main branch the
reactions and the energy each releases are
#figure(table(columns: 2, align: (left, right), stroke: none,
  $"p" + "p" -> "D" + "e"^+ + nu_e$, $0.42 "MeV"$,
  $"D" + "p" -> ""^3"He" + gamma$, $5.49 "MeV"$,
  $""^3"He" + ""^3"He" -> ""^4"He" + 2 "p"$, $12.86 "MeV"$,
), caption: [Main branch of the p–p chain
#link("https://doi.org/10.1103/RevModPhys.83.195")[(Adelberger et al. 2011)].]) <fusion-pp-chain-table>
The first two steps run twice for each #super[3]He–#super[3]He reaction. In total
$ 4 "p" -> ""^4"He" + 2 "e"^+ + 2 nu_e, $ <ch03-pp-chain>
releasing 26.7 MeV including the annihilation of the two positrons with
electrons. The first step needs the weak interaction, which converts a proton
into a neutron; its tiny $S$ factor, $S_(p p)(0) = 4.01 times 10^(-22) "keV b"$,
makes it the slowest step and lets the Sun burn for billions of years.
#knowledge-check((
  (question: [Check the 26.7 MeV from the branch energies.], answer: [$2 times (0.42 + 5.49) + 12.86 = 24.68 "MeV"$, plus $2 times 1.022 "MeV"$ annihilation gives 26.7 MeV.]),
  (question: [Which step limits the rate of the chain?], answer: [The weak p–p reaction.]),
))
]
