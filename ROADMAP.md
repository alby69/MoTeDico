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
    - [x] `AdvisorAgent`: Generazione consigli via LLM.
    - [x] `SocialAgent`: Gestione reazioni e community feed.
- [x] **CLI PoC**: Entry point `main.py` funzionante.

---

## Fase 2: Integrazione Reale & Multimedia (Completato)
In questa fase abbiamo integrato servizi reali e supporto multimediale.

- [x] **IPFS Real integration**: Connessione via aiohttp per caricamento su gateway IPFS.
- [x] **LLM Real integration**: Implementazione provider Gemini e OpenAI per consigli intelligenti.
- [x] **Multimedia Handling**: Supporto per file multimediali (`Attachment`) nei modelli.
- [x] **NIP-94 Implementation**: Supporto per i metadati dei file su rete Nostr.

---

## Fase 3: Protocollo Avanzato & Identity (Completato)
In questa fase abbiamo potenziato la sicurezza e la gestione dell'identità.

- [x] **Nostr Advanced Management**: Migliorata la gestione del client e dei messaggi.
- [x] **Key Management (NIP-06)**: Supporto per mnemonic seed phrase per identità persistenti.
- [x] **Encrypted DMs (NIP-44)**: Implementazione di proposte private e comunicazioni sicure end-to-end.

---

## Prossimi Sviluppi

### Fase 4: Interfaccia Utente (Web UI)
- [ ] **Decentralized Web App**: Dashboard FastAPI + HTMX per gestire progetti e PR.
- [ ] **Real-time Notifications**: Aggiornamento UI tramite eventi Nostr.
- [ ] **Player Multimedia**: Visualizzazione dei contenuti multimediali recuperati direttamente da gateway IPFS.

---

## Visione a Lungo Termine
Trasformare MoTeDico in un ecosistema globale dove la saggezza umana e l'intelligenza artificiale collaborano in modo decentralizzato per risolvere problemi concreti, senza dipendere da piattaforme proprietarie.
