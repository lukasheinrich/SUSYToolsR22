# $Id: CMakeLists.txt 797759 2017-02-18 01:24:37Z zmarshal $
################################################################################
# Package: SUSYTools
################################################################################

 
# Declare the package name:
atlas_subdir( SUSYTools )

# Extra dependencies based on the build environment:
set( extra_deps )
set( extra_libs )
if( NOT XAOD_STANDALONE )
   set( extra_deps GaudiKernel PhysicsAnalysis/POOLRootAccess
      Control/AthAnalysisBaseComps Control/AthenaBaseComps
      Control/AthenaKernel )
   set( extra_libs GaudiKernel AthAnalysisBaseCompsLib )
endif()

# Declare the package's dependencies:
atlas_depends_on_subdirs(
   PUBLIC
   Control/AthToolSupport/AsgTools
   Event/xAOD/xAODCore
   Event/xAOD/xAODEgamma
   Event/xAOD/xAODEventInfo
   Event/xAOD/xAODJet
   Event/xAOD/xAODMissingET
   Event/xAOD/xAODTrigMissingET
   Event/xAOD/xAODMuon
   Event/xAOD/xAODTau
   Event/xAOD/xAODTracking
   Event/xAOD/xAODTruth
   Event/xAOD/xAODMetaData
   PhysicsAnalysis/AnalysisCommon/AssociationUtils
   PhysicsAnalysis/AnalysisCommon/PATInterfaces
   PhysicsAnalysis/Interfaces/PMGAnalysisInterfaces
   PhysicsAnalysis/MCTruthClassifier
   Reconstruction/Jet/JetJvtEfficiency
   Reconstruction/Jet/JetSubStructureUtils
   Trigger/TrigAnalysis/TrigDecisionTool
   PRIVATE
   AsgExternal/Asg_Test
   Control/xAODRootAccess
   Control/AthContainers
   DataQuality/GoodRunsLists
   Event/EventPrimitives
   Event/FourMomUtils
   Event/xAOD/xAODBTagging
   Event/xAOD/xAODBase
   Event/xAOD/xAODCaloEvent
   Event/xAOD/xAODCutFlow
   Event/xAOD/xAODPrimitives
   PhysicsAnalysis/AnalysisCommon/IsolationSelection
   PhysicsAnalysis/AnalysisCommon/ParticleJetTools
   PhysicsAnalysis/AnalysisCommon/PileupReweighting
   PhysicsAnalysis/ElectronPhotonID/IsolationCorrections
   PhysicsAnalysis/ElectronPhotonID/EgammaAnalysisHelpers
   PhysicsAnalysis/Interfaces/EgammaAnalysisInterfaces
   PhysicsAnalysis/Interfaces/AsgAnalysisInterfaces
   PhysicsAnalysis/Interfaces/FTagAnalysisInterfaces
   PhysicsAnalysis/Interfaces/JetAnalysisInterfaces
   PhysicsAnalysis/Interfaces/MuonAnalysisInterfaces
   PhysicsAnalysis/Interfaces/TriggerAnalysisInterfaces
   PhysicsAnalysis/JetMissingEtID/JetSelectorTools
   PhysicsAnalysis/TauID/TauAnalysisTools
   Reconstruction/Jet/BoostedJetTaggers
   Reconstruction/Jet/JetCPInterfaces
   Reconstruction/Jet/JetCalibTools
   Reconstruction/Jet/JetInterface
   Reconstruction/Jet/JetResolution
   Reconstruction/Jet/JetUncertainties
   Reconstruction/Jet/JetMomentTools
   Reconstruction/MET/METInterface
   Reconstruction/MET/METUtilities
   Reconstruction/tauRecTools
   Tools/PathResolver
   Trigger/TrigAnalysis/TriggerMatchingTool
   Trigger/TrigConfiguration/TrigConfInterfaces
   Trigger/TrigConfiguration/TrigConfxAOD
   ${extra_deps} )

# External dependencies:
find_package( Boost )
find_package( ROOT COMPONENTS Core Tree MathCore Hist RIO )
find_package( GTest )

# Libraries in the package:
atlas_add_library( SUSYToolsLib
   SUSYTools/*.h Root/*.cxx src/SUSYToolsAlg.cxx src/SUSYToolsAlg.h
   PUBLIC_HEADERS SUSYTools src
   PRIVATE_INCLUDE_DIRS ${ROOT_INCLUDE_DIRS} ${BOOST_INCLUDE_DIRS}
   LINK_LIBRARIES AsgTools xAODCore xAODEgamma xAODEventInfo
   xAODJet xAODMissingET xAODMuon xAODTau xAODTracking xAODTruth
   AssociationUtilsLib PATInterfaces TrigDecisionToolLib 
   MCTruthClassifierLib JetJvtEfficiencyLib JetSubStructureUtils
   ParticleJetToolsLib AnaAlgorithmLib
   PRIVATE_LINK_LIBRARIES ${ROOT_LIBRARIES} ${BOOST_LIBRARIES}
   AthContainers EventPrimitives FourMomUtils xAODBTagging xAODBase
   xAODPrimitives
   # BoostedJetTaggersLib
   EgammaAnalysisInterfacesLib
   EgammaAnalysisHelpersLib FTagAnalysisInterfacesLib IsolationSelectionLib
   IsolationCorrectionsLib JetAnalysisInterfacesLib JetSelectorToolsLib
   JetCPInterfaces JetCalibToolsLib JetInterface
   # JetResolutionLib
   JetUncertaintiesLib JetMomentToolsLib METInterface METUtilitiesLib
   PileupReweightingLib PathResolver TauAnalysisToolsLib
   # TriggerAnalysisInterfacesLib
   TriggerMatchingToolLib TrigConfInterfaces TrigConfxAODLib
   xAODTrigMissingET xAODMetaData xAODCutFlow ${extra_libs} )

if( NOT XAOD_STANDALONE )
   atlas_add_component( SUSYTools
      src/*.h src/*.cxx src/components/*.cxx
      NOCLID
      INCLUDE_DIRS ${ROOT_INCLUDE_DIRS}
      LINK_LIBRARIES ${ROOT_LIBRARIES} AthenaBaseComps GaudiKernel
      AthenaKernel AthAnalysisBaseCompsLib xAODEventInfo xAODMuon xAODPrimitives
      xAODJet xAODBTagging xAODEgamma xAODMissingET xAODTracking xAODTau
      TauAnalysisToolsLib xAODCore AthContainers AsgTools xAODBase xAODCutFlow
      PATInterfaces PathResolver SUSYToolsLib )
endif()

atlas_add_dictionary( SUSYToolsDict
   SUSYTools/SUSYToolsDict.h
   SUSYTools/selection.xml
   LINK_LIBRARIES SUSYToolsLib )

# Executable(s) in the package:
set( extra_libs )
if( NOT XAOD_STANDALONE )
   set( extra_libs POOLRootAccessLib )
endif()
atlas_add_executable( SUSYToolsTester
   util/SUSYToolsTester.cxx
   INCLUDE_DIRS ${ROOT_INCLUDE_DIRS}
   LINK_LIBRARIES ${ROOT_LIBRARIES} xAODRootAccess xAODEventInfo xAODMuon
   xAODEgamma xAODTau xAODTruth xAODJet xAODCaloEvent xAODCore xAODMissingET
   FTagAnalysisInterfacesLib xAODBase TauAnalysisToolsLib GoodRunsListsLib
   PileupReweightingLib PATInterfaces PathResolver METUtilitiesLib xAODCutFlow
   SUSYToolsLib ${extra_libs} )

atlas_add_executable( SUSYTruthTester
   util/SUSYTruthTester.cxx
   INCLUDE_DIRS ${ROOT_INCLUDE_DIRS}
   LINK_LIBRARIES ${ROOT_LIBRARIES} xAODRootAccess xAODEventInfo 
   xAODTruth xAODCore xAODBase PATInterfaces PathResolver xAODCutFlow
   SUSYToolsLib ${extra_libs} )

atlas_add_executable( SUSYTools_check_xsections
   util/check_xsections.cxx
   INCLUDE_DIRS ${ROOT_INCLUDE_DIRS}
   LINK_LIBRARIES ${ROOT_LIBRARIES} SUSYToolsLib )

if( XAOD_STANDALONE )
   atlas_add_executable( SUSYTools_check_syst
      util/check_syst.cxx
      INCLUDE_DIRS ${ROOT_INCLUDE_DIRS}
      LINK_LIBRARIES ${ROOT_LIBRARIES} xAODRootAccess PATInterfaces
      SUSYToolsLib )
endif()

# Test(s) in the package:
if( XAOD_STANDALONE )
   atlas_add_test( gt_SUSYTools_xs_loader
      SOURCES test/gt_SUSYTools_xs_loader.cxx
      INCLUDE_DIRS ${GTEST_INCLUDE_DIRS} ${ROOT_INCLUDE_DIRS}
      LINK_LIBRARIES ${GTEST_LIBRARIES} ${ROOT_LIBRARIES} SampleHandler
      # EXTRA_PATTERNS "\([0-9]+ ms\)|\([0-9]+ ms total\)"
   )
   atlas_add_test( ut_SUSYTools_test_xs_files
      SOURCES test/ut_SUSYTools_test_xs_files.cxx
      INCLUDE_DIRS ${ROOT_INCLUDE_DIRS}
      LINK_LIBRARIES ${ROOT_LIBRARIES} SampleHandler AsgTools)
   #  Veto lines:  Timing (can change night to night); cvmfs path (changes every night); local SUSYTools data directory (so local builds pass)
   #  build path (for nightlies and CI builds - note that CI has Analysis*/build/Analysis*, while NICOS has build/build/Analysis*...)
   atlas_add_test( ut_SUSYTools_config_checker
      SCRIPT test/ut_SUSYTools_config_checker.py
      PROPERTIES TIMEOUT 300
      # EXTRA_PATTERNS "^Ran [0-9]+ tests in [0-9.]+s|INFO|cvmfs/atlas-nightlies\.cern\.ch/repo|x86_64-slc6-gcc62-opt/data/SUSYTools|x86_64-centos7-gcc8-opt/data/SUSYTools|build/Analysis.*/x86_64-slc6-gcc62-opt|build/Analysis.*/x86_64-centos7-gcc8-opt|create data set info.*"
   )
   # Additional veto lines: more timing, local conf file this thing is writing
   atlas_add_test( ut_SUSYTools_wp_checker
      SCRIPT test/ut_SUSYTools_wp_checker.py
      PROPERTIES TIMEOUT 700
      # EXTRA_PATTERNS "^  Entire loop [ ]+- [0-9.]+ / [0-9.]+ ms|INFO|^  Excluding first event - [0-9.]+ / [0-9.]+ ms|INFO|^  First event [ ]+- [0-9.]+ / [0-9.]+ ms|INFO|cvmfs/atlas-nightlies\.cern\.ch/repo|x86_64-slc6-gcc62-opt/data/SUSYTools|x86_64-centos7-gcc8-opt/data/SUSYTools|build/Analysis.*/x86_64-slc6-gcc62-opt|build/Analysis.*/x86_64-centos7-gcc8-opt|mySTdefs_conf\.tmp|^Ran [0-9]+ tests in [0-9.]+s|create data set info.*"
   )
   atlas_add_test( ut_SUSYToolsTester_atlfast
      SOURCES test/ut_SUSYToolsTester_atlfast.cxx
      INCLUDE_DIRS ${ROOT_INCLUDE_DIRS}
      LINK_LIBRARIES ${ROOT_LIBRARIES} AsgTools
      PROPERTIES TIMEOUT 300
      # EXTRA_PATTERNS "^  Entire loop [ ]+- [0-9.]+ / [0-9.]+ ms|INFO|^  Excluding first event - [0-9.]+ / [0-9.]+ ms|INFO|^  First event [ ]+- [0-9.]+ / [0-9.]+ ms|INFO|cvmfs/atlas-nightlies\.cern\.ch/repo|x86_64-slc6-gcc62-opt/data/SUSYTools|x86_64-centos7-gcc8-opt/data/SUSYTools|build/Analysis.*/x86_64-slc6-gcc62-opt|build/Analysis.*/x86_64-centos7-gcc8-opt"
   )
   # Safety factor for tests
   atlas_add_test( ut_SUSYToolsTester_data
      SOURCES test/ut_SUSYToolsTester_data.cxx
      INCLUDE_DIRS ${ROOT_INCLUDE_DIRS}
      LINK_LIBRARIES ${ROOT_LIBRARIES} AsgTools
      PROPERTIES TIMEOUT 300
      # EXTRA_PATTERNS "^  Entire loop [ ]+- [0-9.]+ / [0-9.]+ ms|INFO|^  Excluding first event - [0-9.]+ / [0-9.]+ ms|INFO|^  First event [ ]+- [0-9.]+ / [0-9.]+ ms|INFO|cvmfs/atlas-nightlies\.cern\.ch/repo|x86_64-slc6-gcc62-opt/data/SUSYTools|x86_64-centos7-gcc8-opt/data/SUSYTools|build/Analysis.*/x86_64-slc6-gcc62-opt|build/Analysis.*/x86_64-centos7-gcc8-opt"
   )
   atlas_add_test( ut_SUSYToolsTester_mc
      SOURCES test/ut_SUSYToolsTester_mc.cxx
      INCLUDE_DIRS ${ROOT_INCLUDE_DIRS}
      LINK_LIBRARIES ${ROOT_LIBRARIES} AsgTools
      PROPERTIES TIMEOUT 300
      # EXTRA_PATTERNS "^  Entire loop [ ]+- [0-9.]+ / [0-9.]+ ms|INFO|^  Excluding first event - [0-9.]+ / [0-9.]+ ms|INFO|^  First event [ ]+- [0-9.]+ / [0-9.]+ ms|INFO|cvmfs/atlas-nightlies\.cern\.ch/repo|x86_64-slc6-gcc62-opt/data/SUSYTools|x86_64-centos7-gcc8-opt/data/SUSYTools|build/Analysis.*/x86_64-slc6-gcc62-opt|build/Analysis.*/x86_64-centos7-gcc8-opt"
   )
endif()

# Install files from the package:
atlas_install_python_modules( python/*.py )
atlas_install_joboptions( share/*.py )
atlas_install_data( data/* )
atlas_install_scripts( scripts/TestSUSYToolsAlg.py )
