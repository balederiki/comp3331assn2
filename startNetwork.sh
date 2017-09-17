#!/bin/bash
cd "${0%/*}"
xterm -hold -title "node A" -geometry 51x15+2040+915 -e python3 Lsr.py A 5100 Topology1/configA.txt &
xterm -hold -title "node B" -geometry 51x15+2360+915 -e python3 Lsr.py B 5101 Topology1/configB.txt &
xterm -hold -title "node C" -geometry 51x15+2680+915 -e python3 Lsr.py C 5102 Topology1/configC.txt &
xterm -hold -title "node D" -geometry 51x15+2040+1150 -e python3 Lsr.py D 5103 Topology1/configD.txt &
xterm -hold -title "node E" -geometry 51x15+2360+1150 -e python3 Lsr.py E 5104 Topology1/configE.txt &
xterm -hold -title "node F" -geometry 51x15+2680+1150 -e python3 Lsr.py F 5105 Topology1/configF.txt 