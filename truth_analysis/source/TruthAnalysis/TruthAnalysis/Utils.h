#include <xAODParticleEvent/Particle.h>

// Helper function to sort a container by pt of its objects
bool ptsorter(const xAOD::IParticle* j1, const xAOD::IParticle* j2);

// Computes the invariant mass of two to four particles
float InvariantMass(const xAOD::IParticle& P1, const xAOD::IParticle& P2);
float InvariantMass(const xAOD::IParticle* P1, const xAOD::IParticle* P2);
float InvariantMass(const xAOD::IParticle& P1, const xAOD::IParticle& P2, const xAOD::IParticle& P3);
float InvariantMass(const xAOD::IParticle* P1, const xAOD::IParticle* P2, const xAOD::IParticle* P3);
float InvariantMass(const xAOD::IParticle& P1, const xAOD::IParticle& P2, const xAOD::IParticle& P3, const xAOD::IParticle& P4);
float InvariantMass(const xAOD::IParticle* P1, const xAOD::IParticle* P2, const xAOD::IParticle* P3, const xAOD::IParticle* P4);
