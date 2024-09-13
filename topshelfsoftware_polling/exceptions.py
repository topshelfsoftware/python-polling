"""Custom polling exceptions defined here."""


class PollAttemptLimitReached(Exception):
    """Raise to indicate max poll attempts exceeded."""

    ...


class PollTimeLimitReached(Exception):
    """Raise to indicate max poll time exceeded."""

    ...
