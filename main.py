import asyncio
import logging
from motedico.config import Settings
from motedico.agents.project_agent import ProjectAgent
from motedico.agents.advisor_agent import AdvisorAgent
from motedico.agents.social_agent import SocialAgent
from motedico.agents.storage_agent import StorageAgent
from motedico.agents.network_agent import NetworkAgent

async def main():
    """
    Main entry point for MoTeDico demonstration.
    """
    logging.basicConfig(level=logging.INFO)
    cfg = Settings()

    # Initialize Agents
    project_agent = ProjectAgent(cfg)
    advisor_agent = AdvisorAgent(cfg)
    social_agent = SocialAgent(cfg)
    storage_agent = StorageAgent(cfg)
    network_agent = NetworkAgent(cfg)

    # Start Agents
    await project_agent.start()
    await advisor_agent.start()
    await social_agent.start()
    await storage_agent.start()
    await network_agent.start()

    print("\n--- BENVENUTI SU MOTEDICO ---\n")

    # 1. Project Creation
    title = "Vacanza in montagna"
    description = "Cerco consigli per una vacanza a luglio, budget 1000€."
    owner = "User123"

    print(f"[*] Creazione progetto: {title}...")
    project = await project_agent.create_project(title, description, owner)

    # 2. Storage
    cid = await storage_agent.upload_content(description)
    project.ipfs_cid = cid

    # 3. Community Reaction
    await social_agent.react_to_project(project.id)

    # 4. AI Advisor
    print(f"[*] Advisor AI sta analizzando il progetto...")
    proposal = await advisor_agent.analyze_and_propose(project)

    if proposal:
        print(f"[*] Ricevuta proposta da {proposal.author}: {proposal.content}")
        await project_agent.add_proposal(project.id, proposal.author, proposal.content)
        await social_agent.react_to_proposal("pr_1")

        # 5. Acceptance
        print(f"[*] Accettazione della proposta pr_1...")
        await project_agent.accept_proposal(project.id, "pr_1")

    print("\n--- FLUSSO COMPLETATO CON SUCCESSO ---\n")

    # Stop Agents
    await project_agent.stop()
    await advisor_agent.stop()
    await social_agent.stop()
    await storage_agent.stop()
    await network_agent.stop()

if __name__ == "__main__":
    asyncio.run(main())
