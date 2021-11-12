# The name of the package:
atlas_subdir (TruthAnalysis)

# Add the shared library:
atlas_add_library (TruthAnalysisLib
  TruthAnalysis/*.h Root/*.cxx
  PUBLIC_HEADERS TruthAnalysis
  LINK_LIBRARIES AnaAlgorithmLib xAODCore xAODEventInfo xAODParticleEvent xAODJet xAODTruth)

if (XAOD_STANDALONE)
 # Add the dictionary (for AnalysisBase only):
 atlas_add_dictionary (TruthAnalysisDict
  TruthAnalysis/TruthAnalysisDict.h
  TruthAnalysis/selection.xml
  LINK_LIBRARIES TruthAnalysisLib)
endif ()

if (NOT XAOD_STANDALONE)
  # Add a component library for AthAnalysis only:
  atlas_add_component (TruthAnalysis
    src/components/*.cxx
    LINK_LIBRARIES TruthAnalysisLib)
endif ()

# Install files from the package:
atlas_install_joboptions(share/*_jobOptions.py)
atlas_install_scripts(share/*_eljob.py)