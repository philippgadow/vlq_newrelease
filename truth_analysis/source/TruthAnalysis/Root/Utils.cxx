#include <TruthAnalysis/Utils.h>


bool ptsorter(const xAOD::IParticle* j1, const xAOD::IParticle* j2) { return (j1->pt() > j2->pt()); }

float InvariantMass(const xAOD::IParticle* P1, const xAOD::IParticle* P2) {
    TLorentzVector DiPart = P1->p4() + P2->p4();
    return DiPart.M();
}
float InvariantMass(const xAOD::IParticle& P1, const xAOD::IParticle& P2) {
    return InvariantMass(&P1, &P2);
}

float InvariantMass(const xAOD::IParticle* P1, const xAOD::IParticle* P2, const xAOD::IParticle* P3) {
    TLorentzVector TriPart = P1->p4() + P2->p4() + P3->p4();
    return TriPart.M();
}
float InvariantMass(const xAOD::IParticle& P1, const xAOD::IParticle& P2, const xAOD::IParticle& P3) {
    return InvariantMass(&P1, &P2, &P3);
}

float InvariantMass(const xAOD::IParticle* P1, const xAOD::IParticle* P2, const xAOD::IParticle* P3, const xAOD::IParticle* P4) {
    TLorentzVector FourPart = P1->p4() + P2->p4() + P3->p4() + P4->p4();
    return FourPart.M();
}
float InvariantMass(const xAOD::IParticle& P1, const xAOD::IParticle& P2, const xAOD::IParticle& P3, const xAOD::IParticle& P4) {
    return InvariantMass(&P1, &P2, &P3, &P4);
}
