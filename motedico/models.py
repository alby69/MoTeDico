from datetime import datetime
from enum import Enum
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field

class ProjectStatus(str, Enum):
    """Enumeration for Project lifecycle states."""
    OPEN = "open"
    CLOSED = "closed"
    COMPLETED = "completed"

class ProposalStatus(str, Enum):
    """Enumeration for Proposal (Pull Request) states."""
    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"

class Attachment(BaseModel):
    """Represents a multimedia attachment (image, video, etc.) stored on IPFS."""
    cid: str
    filename: str
    mimetype: str
    size: Optional[int] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)

class Proposal(BaseModel):
    """
    Represents a suggestion or advice for a project.
    In the MoTeDico ecosystem, this acts like a Pull Request.
    """
    id: Optional[str] = None
    project_id: str
    author: str
    content: str
    status: ProposalStatus = ProposalStatus.PENDING
    attachments: List[Attachment] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.now)

class Project(BaseModel):
    """
    Represents a real-life project or request for advice.
    Examples: "Planning a vacation", "Building a PC", etc.
    """
    id: Optional[str] = None
    title: str
    description: str
    owner: str
    status: ProjectStatus = ProjectStatus.OPEN
    created_at: datetime = Field(default_factory=datetime.now)
    proposals: List[Proposal] = Field(default_factory=list)
    attachments: List[Attachment] = Field(default_factory=list)
    ipfs_cid: Optional[str] = None
