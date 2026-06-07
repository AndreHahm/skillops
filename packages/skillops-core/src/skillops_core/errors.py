"""Custom exceptions for the SkillOps core library."""


class SkillOpsError(Exception):
    """Base exception for SkillOps core errors."""


class SkillOpsFileNotFoundError(SkillOpsError):
    """Raised when a required SkillOps file is missing."""


class SkillOpsValidationError(SkillOpsError):
    """Raised when validation cannot continue because of invalid input."""
