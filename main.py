import asyncio
import logging
from motedico.config import Settings
from motedico.agents.project_agent import ProjectAgent
from motedico.agents.advisor_agent import AdvisorAgent
from motedico.agents.social_agent import SocialAgent
from motedico.agents.storage_agent import StorageAgent

async def main():
    """
    Main entry point for MoTeDico.
    Bootstraps the agent network and demonstrates a full collaborative flow.
    """
    # Setup global logging
    logging.basicConfig(level=logging.INFO)

    # 1. Initialize Settings
    cfg = Settings()
    try:
        # Check for mandatory environment variables
        cfg.validate()
    except ValueError as e:
        # In PoC mode, we proceed with a warning if API keys are missing
        logging.warning(f"Config validation failed (expected in PoC without .env): {e}")

    # 2. Initialize Agents
    project_agent = ProjectAgent(cfg)
    advisor_agent = AdvisorAgent(cfg)
    social_agent = SocialAgent(cfg)
    storage_agent = StorageAgent(cfg)

    # 3. Start Agents (Connect to relays, etc.)
    await project_agent.start()
    await advisor_agent.start()
    await social_agent.start()
    await storage_agent.start()

    print("\n--- BENVENUTI SU MOTEDICO ---\n")

    # --- DEMO FLOW ---

    # A. User creates a project
    title = "Vacanza in montagna"
    description = "Cerco consigli per una vacanza a luglio, budget 1000€, amo la montagna."
    owner = "User123"

    print(f"[*] Creazione progetto: {title}...")
    project = await project_agent.create_project(title, description, owner)

    # B. Storage Agent 'uploads' content to decentralized storage
    cid = await storage_agent.upload_content(description)
    project.ipfs_cid = cid

    # C. Community reacts to the new project
    await social_agent.react_to_project(project.id)

    # D. AI Advisor analyzes the project and submits a proposal (Pull Request)
    print(f"[*] Advisor AI sta analizzando il progetto...")
    proposal = await advisor_agent.analyze_and_propose(project)

    if proposal:
        print(f"[*] Ricevuta proposta da {proposal.author}: {proposal.content}")
        # Register proposal in project state
        await project_agent.add_proposal(project.id, proposal.author, proposal.content)

        # E. Social reaction to the proposal
        await social_agent.react_to_proposal("pr_1")

        # F. User (project owner) accepts the proposal
        print(f"[*] Accettazione della proposta pr_1...")
        await project_agent.accept_proposal(project.id, "pr_1")

    print("\n--- FLUSSO COMPLETATO CON SUCCESSO ---\n")

    # 4. Stop Agents and cleanup
    await project_agent.stop()
    await advisor_agent.stop()
    await social_agent.stop()
    await storage_agent.stop()

if __name__ == "__main__":
    asyncio.run(main())
