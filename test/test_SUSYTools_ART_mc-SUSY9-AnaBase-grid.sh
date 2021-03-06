#!/bin/sh

# art-description: SUSYTools ART test - TestSUSYToolsAlg.py
# art-type: grid
# art-include: 21.2/AnalysisBase
# art-output: hist-MC_DAOD_SUSY9.root
# art-output: dcube

# Create empty pool file
art.py createpoolfile

echo "Running SUSYTools test: \'TestSUSYToolsAlg.py -t mc16e -m 5000 -d 9\'"
TestSUSYToolsAlg.py -t mc16e -m 5000 -d 9
echo  "art-result: $? TEST"

mv submitDir/hist-ARTInput.root ./hist-MC_DAOD_SUSY9.root

echo "Running DCube post-processing"

tName="MCe-SUSY9"
dcubeRef=/cvmfs/atlas.cern.ch/repo/sw/database/GroupData/dev/SUSYTools/ART/References/hist-MC_DAOD_SUSY9.root
dcubeXml=/cvmfs/atlas.cern.ch/repo/sw/database/GroupData/dev/SUSYTools/ART/xml/dcube_config_master.xml

/cvmfs/atlas.cern.ch/repo/sw/art/dcube/bin/art-dcube ${tName} hist-MC_DAOD_SUSY9.root ${dcubeXml} ${dcubeRef}

echo "art-result: $? DCUBE"

echo "Done."
