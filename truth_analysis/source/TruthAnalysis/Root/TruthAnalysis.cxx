#include <AsgTools/MessageCheck.h>
#include <TruthAnalysis/TruthAnalysis.h>
#include <TruthAnalysis/Utils.h>
#include <AthContainers/ConstDataVector.h>
#include "xAODBase/IParticleContainer.h"
#include <xAODTruth/TruthParticle.h>

typedef SG::AuxElement::Accessor<int> IntAccessor;
typedef SG::AuxElement::Decorator<int> IntDecorator;

static IntDecorator dec_pdgId("pdgId");
static IntDecorator dec_parentId("parentId");
static IntAccessor acc_parentId("parentId");


TruthAnalysis :: TruthAnalysis (const std::string& name,
                                  ISvcLocator *pSvcLocator)
    : EL::AnaAlgorithm (name, pSvcLocator)
{
  // Here you put any code for the base initialization of variables,
  // e.g. initialize all pointers to 0.  This is also where you
  // declare all properties for your algorithm.  Note that things like
  // resetting statistics variables or booking histograms should
  // rather go into the initialize() function.
}


StatusCode TruthAnalysis :: initialize ()
{
  // Here you do everything that needs to be done at the very
  // beginning on each worker node, e.g. create histograms and output
  // trees.  This method gets called before any input files are
  // connected.

  return StatusCode::SUCCESS;
}



StatusCode TruthAnalysis :: execute ()
{
  // Here you do everything that needs to be done on every single
  // events, e.g. read input variables, apply cuts, and fill
  // histograms and trees.  This is where most of your actual analysis
  // code will go.

  // retrieve objects from event store
  ANA_CHECK(evtStore()->retrieve(m_eventInfo, "EventInfo"));
  ANA_CHECK(evtStore()->retrieve(m_truthParticles, "TruthParticles"));


 // create container with truth particles: VLB and other particles
  auto TruthVLB = std::make_unique<ConstDataVector<xAOD::IParticleContainer>> (SG::VIEW_ELEMENTS);
  auto TruthHiggsBosons = std::make_unique<ConstDataVector<xAOD::IParticleContainer>> (SG::VIEW_ELEMENTS);
  auto TruthWeakBosons = std::make_unique<ConstDataVector<xAOD::IParticleContainer>> (SG::VIEW_ELEMENTS);
  auto TruthTopQuarks = std::make_unique<ConstDataVector<xAOD::IParticleContainer>> (SG::VIEW_ELEMENTS);
  auto TruthBQuarks = std::make_unique<ConstDataVector<xAOD::IParticleContainer>> (SG::VIEW_ELEMENTS);

  // get truth particles
  for (const auto& particle : *m_truthParticles) {
    // search for VLB resonance (from hard process)
    if (particle->absPdgId() == 6000007 && particle->status() == 22) {
      TruthVLB->push_back(particle);
    } 
    // also store Higgs boson (from hard process)
    if (particle->absPdgId() == 25 && particle->status() == 22) {
      TruthHiggsBosons->push_back(particle);
    }
    // also store top quarks (from hard process)
    if (particle->absPdgId() == 6 && particle->status() == 22) {
      int parentId = 0;
      for (size_t p = 0; p < particle->nParents(); ++p) {
        const xAOD::TruthParticle* P = particle->parent(p);
        if (!P) continue;
        if (P->absPdgId() == 6) parentId = 6;
        if (P->absPdgId() == 23) parentId = 23;
        if (P->absPdgId() == 24) parentId = 24;
        if (P->absPdgId() == 25) parentId = 25;
      }
      dec_parentId(*particle) = parentId;
      TruthTopQuarks->push_back(particle);
    }
    // also store bottom quarks (from hard process)
    if (particle->absPdgId() == 5 && particle->status() == 23) {
      int parentId = 0;
      for (size_t p = 0; p < particle->nParents(); ++p) {
        const xAOD::TruthParticle* P = particle->parent(p);
        if (!P) continue;
        if (P->absPdgId() == 6) parentId = 6;
        if (P->absPdgId() == 23) parentId = 23;
        if (P->absPdgId() == 24) parentId = 24;
        if (P->absPdgId() == 25) parentId = 25;
      }
      dec_parentId(*particle) = parentId;
      TruthBQuarks->push_back(particle);
    }
  }

  // sort by pt
  TruthVLB->sort(ptsorter);
  TruthHiggsBosons->sort(ptsorter);
  TruthWeakBosons->sort(ptsorter);
  TruthTopQuarks->sort(ptsorter);
  TruthBQuarks->sort(ptsorter);

  // compute invariant mass of Higgs and b-quark
  float m_Hb_max = 0.;
  for (const auto& pBQuark : *TruthBQuarks) {
      if (TruthHiggsBosons->size() == 0) continue;
      if (acc_parentId(*pBQuark) == 25) continue;
      float m_Hb = InvariantMass(pBQuark, TruthHiggsBosons->at(0));
      if (m_Hb > m_Hb_max) m_Hb_max = m_Hb;
  }

  float m_Hb_highpt = 0;
  for (const auto& pBQuark : *TruthBQuarks) {
      if (TruthHiggsBosons->size() == 0) continue;
      if (acc_parentId(*pBQuark) == 25) continue;
      m_Hb_highpt = InvariantMass(pBQuark, TruthHiggsBosons->at(0));
      break;
  }

  // decorate event info with output variable
  m_eventInfo->auxdecor<float>("ev_m_Hb_max") = m_Hb_max;
  m_eventInfo->auxdecor<float>("ev_m_Hb_highpt") = m_Hb_highpt;
  
  return StatusCode::SUCCESS;
}



StatusCode TruthAnalysis :: finalize ()
{
  // This method is the mirror image of initialize(), meaning it gets
  // called after the last event has been processed on the worker node
  // and allows you to finish up any objects you created in
  // initialize() before they are written to disk.  This is actually
  // fairly rare, since this happens separately for each worker node.
  // Most of the time you want to do your post-processing on the
  // submission node after all your histogram outputs have been
  // merged.
  return StatusCode::SUCCESS;
}