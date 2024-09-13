"""Custom polling exceptions defined here."""


class PollAttemptLimitReached(Exception): ...


class PollTimeLimitReached(Exception): ...
