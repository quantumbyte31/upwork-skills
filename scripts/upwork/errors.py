"""Upwork automation exception hierarchy."""


class UpworkError(Exception):
    """Base exception for Upwork automation."""


class BridgeError(UpworkError):
    """Bridge communication error."""


class NotLoggedInError(UpworkError):
    def __init__(self) -> None:
        super().__init__(
            "Not logged in. Please log in to Upwork in your browser first."
        )


class ElementNotFoundError(UpworkError):
    def __init__(self, selector: str) -> None:
        self.selector = selector
        super().__init__(f"Element not found: {selector}")


class ProposalError(UpworkError):
    """Proposal submission failed."""


class SearchError(UpworkError):
    """Job search failed."""
