"""Poll for status."""

import datetime
import time
from typing import Any, Callable, Optional, Tuple

from topshelfsoftware_logging import get_logger

from .step import step_exponential_backoff
from .exceptions import PollAttemptLimitReached, PollTimeLimitReached

logger = get_logger(__name__, stream=None)


def is_truthy(value: Any) -> bool:
    """Tests if return value is truthy."""
    return bool(value)


def poll(
    fun: Callable,
    args: tuple = (),
    kwargs: Optional[dict] = None,
    step_fun: Callable = step_exponential_backoff,
    step_fun_kwargs: Optional[dict] = None,
    timeout: float = 60,
    max_attempts: Optional[int] = None,
    check_success: Callable = is_truthy,
    ignore_exceptions: Optional[Tuple[Exception, ...]] = None,
) -> Any:
    """Poll a target function until a certain condition is met.

    Parameters
    ----------
    fun: Callable
        Target function to poll.

    args: tuple
        Target function args.

    kwargs: dict, optional
        Target function kwargs.
        Default is `None`.

    step_fun: Callable, optional
        A callback function to compute the next step in seconds.
        See `topshelfsoftware_polling.step` for predefined step functions.
        Default is `topshelfsoftware_polling.step.step_constant`.

    step_fun_kwargs: dict, optional
        Step function kwargs.
        See `topshelfsoftware_polling.step` for predefined step functions
        and kwargs.
        Default is `{"step": 1}`.

    timeout: float, optional
        Length of poll in seconds.
        `PollTimeLimitReached` raised if this timeout is exceeded.
        Default is `60`.

    max_attempts: int, optional
        Maximum number of times the target function will be called
        before failing.
        `PollAttemptLimitReached` raised if attempts exceeds this value.
        Default of `None` means poll with no limit for number of attempts.

    check_success: Callable, optional
        A callback function that accepts the return value of the target
        function. It should return `True` if you want the polling function
        to stop and return the value of the target function.
        Default is `topshelfsoftware_polling.polling.is_truthy`.

    ignore_exceptions: tuple[Exception, ...], optional
        These exceptions are caught and ignored. Thus, the result is that
        a retry will be performed on the target function.
        Default is `None`.

    Returns
    -------
    Any
        Return value of target function.

    Inspired by the `polling2` module (https://polling2.readthedocs.io).
    Simplified and added flexibility for step function definition.

    >>> import requests
    >>> res = poll(
    >>>     requests.post,
    >>>     args=(url,),
    >>>     kwargs={"json": data},
    >>>     max_attempts=3,
    >>>     check_success=lambda r: r.status_code != 504,
    >>> )
    >>> try:
    >>>     res.raise_for_status()
    >>> except requests.HTTPError:
    >>>     logger.error(res.text)
    >>>     raise
    >>> print(f"Result: {res.json()}")
    """
    kwargs = kwargs or dict()
    step_fun_kwargs = step_fun_kwargs or dict()
    end = (
        datetime.datetime.now() + datetime.timedelta(seconds=timeout)
        if timeout
        else None
    )
    ignore_exceptions = ignore_exceptions or tuple()
    attempt = 0
    while True:
        attempt += 1
        step_fun_kwargs["attempt"] = attempt
        step = step_fun(**step_fun_kwargs)
        if max_attempts and attempt > max_attempts:
            raise PollAttemptLimitReached(
                f"Poll was not successful in attempt limit ({max_attempts})"
            )

        try:
            res = fun(*args, **kwargs)
        except Exception as e:
            if isinstance(e, ignore_exceptions):
                logger.warning(
                    f"Failed {fun.__name__} due to {type(e).__name__}. "
                    f"Attempt {attempt} / {max_attempts}, "
                    f"retrying in {step:.2f} seconds. [{e}]"
                )
            else:
                raise
        else:
            if check_success(res):
                return res
            else:
                logger.info(
                    f"Poll #{attempt} response: {res}, "
                    f"next poll in {step:.2f} seconds"
                )

        if end is not None and datetime.datetime.now() >= end:
            raise PollTimeLimitReached(
                f"Poll was not successful in time limit ({timeout} seconds)"
            )

        time.sleep(step)
