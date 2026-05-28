import asyncio
import logging
from motedico.config import Settings
from motedico.agents.project_agent import ProjectAgent
from motedico.agents.advisor_agent import AdvisorAgent
from motedico.agents.social_agent import SocialAgent
from motedico.agents.storage_agent import StorageAgent

async def main():
    # Setup logging
    logging.basicConfig(level=logging.INFO)

    # Initialize Settings
    cfg = Settings()
    try:
        cfg.validate()
    except ValueError as e:
        logging.warning(f"Config validation failed (expected in PoC without .env): {e}")

    # Initialize Agents
    project_agent = ProjectAgent(cfg)
    advisor_agent = AdvisorAgent(cfg)
    social_agent = SocialAgent(cfg)
    storage_agent = StorageAgent(cfg)

    # Start Agents
    await project_agent.start()
    await advisor_agent.start()
    await social_agent.start()
    await storage_agent.start()

    print("\n--- BENVENUTI SU MOTEDICO ---\n")

    # 1. User creates a project
    title = "Vacanza in montagna"
    description = "Cerco consigli per una vacanza a luglio, budget 1000€, amo la montagna."
    owner = "User123"

    print(f"[*] Creazione progetto: {title}...")
    project = await project_agent.create_project(title, description, owner)

    # 2. Storage Agent 'uploads' content
    cid = await storage_agent.upload_content(description)
    project.ipfs_cid = cid

    # 3. Community reacts
    await social_agent.react_to_project(project.id)

    # 4. AI Advisor analyzes and submits a proposal (PR)
    print(f"[*] Advisor AI sta analizzando il progetto...")
    proposal = await advisor_agent.analyze_and_propose(project)

    if proposal:
        print(f"[*] Ricevuta proposta da {proposal.author}: {proposal.content}")
        # Add proposal to project tracking
        await project_agent.add_proposal(project.id, proposal.author, proposal.content)

        # 5. Social reaction to proposal
        await social_agent.react_to_proposal("pr_1")

        # 6. User accepts the proposal
        print(f"[*] Accettazione della proposta pr_1...")
        await project_agent.accept_proposal(project.id, "pr_1")

    print("\n--- FLUSSO COMPLETATO CON SUCCESSO ---\n")

    # Stop Agents
    await project_agent.stop()
    await advisor_agent.stop()
    await social_agent.stop()
    await storage_agent.stop()

if __name__ == "__main__":
    asyncio.run(main())
