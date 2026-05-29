class MoTeDicoError(Exception):
    """Base class for MoTeDico exceptions."""
    pass

class LLMError(MoTeDicoError):
    """Raised when an LLM provider fails."""
    pass

class StorageError(MoTeDicoError):
    """Raised when storage operations fail."""
    pass

class NetworkError(MoTeDicoError):
    """Raised when network operations fail."""
    pass
