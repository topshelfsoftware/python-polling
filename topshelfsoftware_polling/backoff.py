"""Gradually increase interval between consecutive polling attempts."""

import random


def backoff_linear(step: float, factor: float = 2.0) -> float:
    """Linearly change the interval between polling attempts.

    Parameters
    ----------
    step: float
        Number (in sec) to scale linearly.

    factor: float, optional
        Scaling factor.
        Default is `2.0`.

    Returns
    -------
    float
        Step (in sec).
    """
    return step * factor


def backoff_exponential_with_full_jitter(
    attempt: int,
    base_interval: float = 1,
    max_interval: float = 60,
):
    """Grow delay exponentially with random jitter added to avoid synchronized
    retries from multiple clients.

    See https://aws.amazon.com/blogs/architecture/exponential-backoff-and-jitter

    Parameters
    ----------
    attempt: int
        Current polling attempt count.

    base_interval: float, optional
        Initial value (attempt=0) will be a random number between
        0 and the base interval.
        Default is `1.0`.

    max_interval: float, optional
        Maximum interval between attempts.
        Default is `60.0`.

    Returns
    -------
    float
        Step (in sec).
    """
    return random.uniform(
        0, min(max_interval, pow(2, attempt) * base_interval)
    )
