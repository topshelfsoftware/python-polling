"""Functions for calculating the interval (step) between
consecutive polling attempts."""

import random


def step_constant(step: float, **kwargs) -> float:
    """Maintain constant delay between polling attempts.

    Parameters
    ----------
    step: float
        Number (in sec).

    Returns
    -------
    float
        Step (in sec).
    """
    return step


def step_exponential_backoff(
    attempt: int,
    backoff_rate: int = 2,
    base_interval: float = 1,
    max_interval: float = 60,
    jitter: bool = False,
    **kwargs,
):
    """Increase the interval exponentially using
    `backoff_rate`^(`attempt` - 1).
    Optionally introduce random jitter to avoid synchronized retries
    from multiple clients.

    For example, let's assume `base_interval=3`:
    For the first attempt `attempt=1`, the result is three (3) seconds.
    For the second attempt `attempt=2`, the result is six (6) seconds.
    For the third attempt `attempt=3`, the result is twelve (12) seconds...

    See https://aws.amazon.com/blogs/architecture/exponential-backoff-and-jitter

    Parameters
    ----------
    attempt: int
        Current polling attempt count.

    backoff_rate: int, optional
        Multiplier by which the interval denoted by `base_interval` increases
        after each attempt.
        Default is `2`.

    base_interval: float, optional
        A positive integer that represents the interval
        for the first attempt (in sec).
        Default is `1.0`.

    max_interval: float, optional
        Maximum interval (in sec) for each step.
        Default is `60.0`.

    jitter: bool, optional
        Determines whether or not to include jitter in the step calculation.
        Jitter reduces simultaneous retry attempts using a randomized delay
        interval. The random interval is always [0, {step_calculation}].
        Default is `False`.

    Returns
    -------
    float
        Step (in sec).
    """
    backoff = base_interval * pow(backoff_rate, attempt - 1)
    step = min(max_interval, backoff)
    return step if not jitter else random.uniform(0, step)
