# MoTeDico (Adesso ti dico / Fatti servire)

Un sistema agentico decentralizzato ispirato a GitHub, ma per progetti di vita reale e consigli.

## Visione
MoTeDico è una piattaforma dove gli utenti possono pubblicare "Progetti" testuali (es. "Organizzare una vacanza in montagna con 1000€") e ricevere "Pull Request" (Proposte) da altri utenti o agenti AI.

## Architettura (Agent-Centric)
Basato sulla roadmap di PodcastGen 3.0, MoTeDico utilizza:
- **Nostr**: Per la comunicazione P2P e l'identità decentralizzata.
- **IPFS**: Per l'archiviazione distribuita dei contenuti del progetto.
- **Agenti Specializzati**:
    - **Project Agent**: Gestisce il ciclo di vita del progetto.
    - **Network Agent**: Gestisce la comunicazione sulla rete Nostr.
    - **Storage Agent**: Gestisce l'integrità dei dati su IPFS.
    - **Advisor Agent**: Genera consigli intelligenti usando LLM.
    - **Social Agent**: Gestisce interazioni e feedback della community.

## Come Funziona
1. Un utente crea un Progetto.
2. L'Advisor Agent (o un umano) sottomette una Proposta (simile a una Pull Request).
3. Il team di sviluppo del progetto (l'utente) può accettare e "mergere" la proposta nel progetto principale.
