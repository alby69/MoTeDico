# MoTeDico Roadmap

Stato avanzamento e sviluppi futuri della piattaforma agentica per il consiglio collaborativo.

## Stato Attuale: Fase 1 - Fondamenta (Completato)
In questa fase abbiamo stabilito l'architettura base e i protocolli di comunicazione.

- [x] **Architettura Agent-Centric**: Definizione di `BaseAgent`.
- [x] **Data Models**: Implementazione di `Project` e `Proposal` (modello Pull Request).
- [x] **Network Layer (Nostr)**: Integrazione base con `nostr-sdk` per identità e broadcast P2P.
- [x] **Storage Layer (IPFS)**: Astrazione `StorageAgent` per l'archiviazione a indirizzamento per contenuto.
- [x] **Specialized Agents**:
    - [x] `ProjectAgent`: Gestione ciclo di vita progetto.
    - [x] `AdvisorAgent`: Generazione consigli via LLM (mocked PoC).
    - [x] `SocialAgent`: Gestione reazioni e community feed.
- [x] **CLI PoC**: Entry point `main.py` funzionante.

---

## Prossimi Sviluppi

### Fase 2: Integrazione Reale & Multimedia
- [ ] **IPFS Real integration**: Connessione a un nodo IPFS locale o servizio di pinning (es. Pinata).
- [ ] **LLM Real integration**: Wrapper per `GeminiProvider` e `OpenAIProvider` per generare consigli reali.
- [ ] **Multimedia Handling**: Supporto per immagini e video allegati ai progetti via IPFS.
- [ ] **NIP-94 Implementation**: Uso dei metadati standard su Nostr per i file multimediali.

### Fase 3: Protocollo Avanzato & Identity
- [ ] **Nostr Multi-Relay handling**: Logica avanzata di riconnessione e selezione relay.
- [ ] **Key Management**: Sistema sicuro per gestire le seed phrase degli utenti/agenti.
- [ ] **Encrypted DMs**: Proposte private tra advisor e utente tramite NIP-04/NIP-44.

### Fase 4: Interfaccia Utente (Web UI)
- [ ] **Decentralized Web App**: Dashboard FastAPI + HTMX per gestire progetti e PR.
- [ ] **Real-time Notifications**: Aggiornamento UI tramite eventi Nostr.
- [ ] **Player Multimedia**: Visualizzazione dei contenuti multimediali recuperati direttamente da gateway IPFS.

---

## Visione a Lungo Termine
Trasformare MoTeDico in un ecosistema globale dove la saggezza umana e l'intelligenza artificiale collaborano in modo decentralizzato per risolvere problemi concreti, senza dipendere da piattaforme proprietarie.
