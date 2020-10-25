#! /usr/bin/env python

# Copyright (C) 2002-2019 CERN for the benefit of the ATLAS collaboration

import unittest
import ROOT
ROOT.gROOT.SetBatch()

import string, os, sys
import subprocess


class ConfigWP(object):
    def __init__(self, *settings, **kwargs):
        for dictionary in settings:
            for key in dictionary:
                setattr(self, key, dictionary[key])
        for key in kwargs:
            setattr(self, key, kwargs[key])

    def __str__(self):
       rs=''
       for k in sorted(self.__dict__): #, reverse=True):
          rs += '%s : %s\n' % (k, str(self.__dict__[k]))
       return rs


def writeConfig(myConfig):

    ConfigTemp = string.Template("""
##################################################
# SUSYTools configuration file
##################################################
EleBaseline.Pt: 10000.
EleBaseline.Eta: 2.47
EleBaseline.Id: ${ELE_ID_Base}
EleBaseline.CrackVeto: false
#
Ele.Et: 25000.
Ele.Eta: 2.47
Ele.CrackVeto: false
Ele.Iso: ${ELE_ISO}
Ele.IsoHighPt: FCHighPtCaloOnly # tight iso required for electrons pt > 400 GeV
Ele.Id: ${ELE_ID}
Ele.d0sig: 5.
Ele.z0: 0.5
# ChargeIDSelector WP
Ele.CFT: None
#
MuonBaseline.Pt: 10000.
MuonBaseline.Eta: 2.7
MuonBaseline.Id: ${MU_ID_Base} # Medium
#
Muon.Pt: 25000.
Muon.Eta: 2.7
Muon.Id: ${MU_ID_Base} # Medium
Muon.Iso: ${MU_ISO}
Muon.d0sig: 3.
Muon.z0: 0.5
#
MuonCosmic.z0: 1.
MuonCosmic.d0: 0.2
#
BadMuon.qoverp: 0.2
#
PhotonBaseline.Pt: 25000.
PhotonBaseline.Eta: 2.37
PhotonBaseline.Id: ${PH_ID_Base}
#
Photon.Pt: 130000.
Photon.Eta: 2.37
Photon.Id: ${PH_ID}
Photon.Iso: ${PH_ISO}
#
Tau.Pt: 20000.
Tau.Eta: 2.5
Tau.Id: Medium
#
Jet.Pt: 20000.
Jet.Eta: 2.8
Jet.InputType: 9 # EMPFlow
Jet.JvtWP: Default
Jet.JvtPtMax: 60.0
#
FwdJet.doJVT: false
FwdJet.JvtPtMax: 120e3
FwdJet.JvtEtaMin: 2.5
FwdJet.JvtWP: Tight
#
Jet.LargeRcollection: AntiKt10LCTopoTrimmedPtFrac5SmallR20Jets
Jet.LargeRuncConfig: rel21/Spring2019/R10_GlobalReduction.config
# 80% efficiency working points
Jet.WtaggerConfig: SmoothedContainedWTagger_AntiKt10TrackCaloClusterTrimmed_MaxSignificance_3Var_MC16d_20190410.dat # set to None to turn this off
Jet.ZtaggerConfig: SmoothedContainedZTagger_AntiKt10TrackCaloClusterTrimmed_MaxSignificance_3Var_MC16d_20190410.dat # set to None to turn this off
Jet.ToptaggerConfig: JSSDNNTagger_AntiKt10LCTopoTrimmed_TopQuarkInclusive_MC16d_20190405_80Eff.dat # set to None to turn this off
# JMS Calibration (None, Extrap, Frozen)
Jet.JMSCalib: None
#
BadJet.Cut: LooseBad
#
#master switch for btagging use in ST. If false, btagging is not used neither for jets decorations nor for OR (regardless of the options below)
Btag.enable: true
#
Btag.Tagger: MV2c10
Btag.WP: ${BTAG_WP}
Btag.MinPt: 20000.
#
BtagTrkJet.MinPt: 10000.
#
# set the -999. to positive number to override default
OR.DoBoostedElectron: true
OR.BoostedElectronC1: -999.
OR.BoostedElectronC2: -999.
OR.BoostedElectronMaxConeSize: -999.
OR.DoBoostedMuon: true
OR.BoostedMuonC1: -999.
OR.BoostedMuonC2: -999.
OR.BoostedMuonMaxConeSize: -999.
OR.DoMuonJetGhostAssociation: true
OR.DoTau: false
OR.DoPhoton: false
OR.Bjet: true
OR.ElBjet: false
OR.MuBjet: false
OR.TauBjet: false
OR.MuJetApplyRelPt: false
OR.MuJetPtRatio: -999.
OR.MuJetTrkPtRatio: -999.
OR.RemoveCaloMuons: true
OR.MuJetInnerDR: -999.
OR.BtagWP: FixedCutBEff_85
#
OR.DoFatJets: false
OR.EleFatJetDR: 1.
OR.JetFatJetDR: 1.
#
SigLep.RequireIso: true
#
MET.EleTerm: RefEle
MET.GammaTerm: RefGamma
MET.TauTerm: RefTau
MET.JetTerm: RefJet
MET.MuonTerm: Muons
MET.OutputTerm: Final
MET.JetSelection: Tight
MET.RemoveOverlappingCaloTaggedMuons: 1
MET.DoRemoveMuonJets: 1
MET.UseGhostMuons: false
MET.DoMuonEloss: false
MET.DoTrkSyst: 1
MET.DoCaloSyst: 0
#
METSys.ConfigPrefix: METUtilities/data17_13TeV/prerec_Jan16
#
# Trigger SFs configuration
Ele.TriggerSFStringSingle: SINGLE_E_2015_e24_lhmedium_L1EM20VH_OR_e60_lhmedium_OR_e120_lhloose_2016_2018_e26_lhtight_nod0_ivarloose_OR_e60_lhmedium_nod0_OR_e140_lhloose_nod0
#
StrictConfigCheck: false
""")

    tr_dict = {'ELE_ID_Base' : myConfig.el_id_base,
               'ELE_ID'      : myConfig.el_id,
               'ELE_ISO'     : myConfig.el_iso,
               'MU_ID_Base'  : myConfig.mu_id_base,
               'MU_ID'       : myConfig.mu_id,
               'MU_ISO'      : myConfig.mu_iso,
               'PH_ID_Base'  : myConfig.ph_id_base,
               'PH_ID'       : myConfig.ph_id,
               'PH_ISO'      : myConfig.ph_iso,
               'BTAG_WP'     : myConfig.btag_wp}


    return ConfigTemp.substitute(tr_dict)


## Main test class
class TestSUSYTools(unittest.TestCase):

    #Files and commands
    theConfig = 'mySTdefs_conf.tmp'

    theSample = '/cvmfs/atlas-nightlies.cern.ch/repo/data/data-art/SUSYTools/DAOD_PHYSVAL.mc16_13TeV.410470.FS_mc16e_p4237.PHYSVAL.pool.root'

    theTest = 'SUSYToolsTester %s maxEvents=10 isData=0 isAtlfast=0 Debug=0 NoSyst=0 ConfigFile=%s ' % (theSample, theConfig)

    # The prw file
    theTest += ' PRWFile=/cvmfs/atlas.cern.ch/repo/sw/database/GroupData/dev/PileupReweighting/mc16_13TeV/pileup_mc16e_dsid410470_FS.root'

    # The lumicalc file
    theTest += ' ilumicalcFile=/cvmfs/atlas.cern.ch/repo/sw/database/GroupData/GoodRunsLists/data18_13TeV/20190318/ilumicalc_histograms_None_348885-364292_OflLumi-13TeV-010.root'

    #Working points
    EL_ID_WP  = ['LooseAndBLayerLLH', 'MediumLLH', 'TightLLH']
    EL_ISO_WP = ['FCHighPtCaloOnly','FCLoose','FCTight']
    MU_ID_WP  = ['1']
    MU_ISO_WP = ['Loose_VarRad']
    PH_ID_WP  = ['Loose','Tight']
    PH_ISO_WP = ['FixedCutTight','FixedCutLoose']
    BTAG_WP   = ['FixedCutBEff_77']
    #...

    #default settings
    defaults_dict = {'el_id_base' : 'LooseAndBLayerLLH',
                     'el_id'      : 'TightLLH',
                     'el_iso'     : 'FCLoose',
                     'mu_id_base' : '1',
                     'mu_id'      : '1',
                     'mu_iso'     : 'Loose_VarRad',
                     'ph_id_base' : 'Tight',
                     'ph_id'      : 'Tight',
                     'ph_iso'     : 'FixedCutTight',
                     'btag_wp'    : 'FixedCutBEff_77'}


    #default configuration
    myConf = ConfigWP(defaults_dict)

    #save unsupported confs
    failConfs = []

    @classmethod
    def setUpClass(cls):
        cls.event = ROOT.xAOD.TEvent()
        #cls.tool_st = ROOT.ST.SUSYObjDef_xAOD('ST_what')

    #Default Initialization
#    def test_initialization_data(self):
#        st = ROOT.ST.SUSYObjDef_xAOD('ST_data')
#        st.setDataSource(0)
#        self.assertTrue(st.initialize().isSuccess())
#
#    def test_initialization_mc_full(self):
#        st = ROOT.ST.SUSYObjDef_xAOD('ST_full')
#        st.setDataSource(1)
#       self.assertTrue(st.initialize().isSuccess())
#
#    def test_initialization_mc_fast(self):
#        st = ROOT.ST.SUSYObjDef_xAOD('ST_fast')
#        st.setDataSource(2)
#        self.assertTrue(st.initialize().isSuccess())


    #Test WPs
    def run_WPs(self, att='',  WPlist=[]):

        def_dict = self.myConf.__dict__

        for wp in WPlist:

            #write new config
            self.myConf.__dict__[att] = wp

            OFile = open(self.theConfig, 'w')
            OFile.write( writeConfig(self.myConf) )
            OFile.close()

            ## run the test
            print '   Testing ',wp
            print self.myConf
            output = subprocess.Popen(self.theTest, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, env=os.environ.copy())
            out,err = output.communicate()
            print out

            ## bookkeep failing settings
            if 'ERROR' in out:
                #self.failConfs.append( type('ConfCopy', self.myConf.__bases__, dict(self.myConf.__dict__)) )
                self.failConfs.append('%s : %s' % (att, wp))

            ## reset global to default dict
            self.myConf.__dict__[att] = def_dict[att]

            ## check for errors in output
            self.assertFalse('ERROR' in out)

        # Make sure the output doesn't get stepped on by something else
        sys.stdout.flush()
        #os.remove(self.theConfig)

    #Test Electron WPs
    def test_EL_WPs(self):
        self.run_WPs('el_id_base', self.EL_ID_WP)
        self.run_WPs('el_id', self.EL_ID_WP)
        self.run_WPs('el_iso', self.EL_ISO_WP)

    #Test Muon WPs
    def test_MU_WPs(self):
        self.run_WPs('mu_id_base', self.MU_ID_WP)
        self.run_WPs('mu_id', self.MU_ID_WP)
        self.run_WPs('mu_iso', self.MU_ISO_WP)

    #Test Photon WPs
    def test_PH_WPs(self):
        self.run_WPs('ph_id_base', self.PH_ID_WP)
        self.run_WPs('ph_id', self.PH_ID_WP)
        self.run_WPs('ph_iso', self.PH_ISO_WP)

    #Test Btagging WPs
    def test_BTAG_WPs(self):
        self.run_WPs('btag_wp', self.BTAG_WP)

    #Print non-supported configurations
    def test_printNS(self):
        if len(self.failConfs)>0:
            print 'Non-supported configurations'
            for fc in self.failConfs:
                print '-'*80
                print fc



if __name__ == '__main__':

    ## it is a slow test, so...
    if os.getenv ("ROOTCORE_AUTO_UT") == "1" and os.getenv ("ROOTCORE_SLOW_UT") != "1" :
        sys.exit (0)

    ## Load pkgs
    ROOT.gROOT.ProcessLine(".x $ROOTCOREDIR/scripts/load_packages.C")
    #ROOT.xAOD.TReturnCode.enableFailure()


    ## Call the tests
    #unittest.main()
    suite = unittest.TestLoader().loadTestsFromTestCase(TestSUSYTools)
    result = unittest.TextTestRunner(verbosity=0).run(suite).wasSuccessful()
    sys.exit( not result ) #convert True -> 0
