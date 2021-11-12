#ifndef TruthAnalysis_TruthAnalysis_H
#define TruthAnalysis_TruthAnalysis_H

#include <AnaAlgorithm/AnaAlgorithm.h>
// #include <AsgTools/ToolHandle.h>

#include <xAODEventInfo/EventInfo.h>
#include "xAODTruth/TruthParticleContainer.h"



class TruthAnalysis : public EL::AnaAlgorithm
{
public:
  // this is a standard algorithm constructor
  TruthAnalysis (const std::string& name, ISvcLocator* pSvcLocator);

  // these are the functions inherited from Algorithm
  virtual StatusCode initialize () override;
  virtual StatusCode execute () override;
  virtual StatusCode finalize () override;

private:
  // Configuration, and any other types of variables go here.
  const xAOD::EventInfo *m_eventInfo;
  const xAOD::TruthParticleContainer* m_truthParticles;

  // output variables
  float m_VLQ;

};

#endif