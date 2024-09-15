import os
import re
import sys
from typing import Callable

import pytest

from topshelfsoftware_logging import get_logger

from conftest import get_json_files, print_section_break

# ----------------------------------------------------------------------------#
#                               --- Globals ---                               #
# ----------------------------------------------------------------------------#
from __setup__ import TEST_EVENTS_PATH

MODULE = "polling"
MODULE_EVENTS_DIR = os.path.join(TEST_EVENTS_PATH, MODULE)

# ----------------------------------------------------------------------------#
#                               --- Logging ---                               #
# ----------------------------------------------------------------------------#
logger = get_logger(f"test_{MODULE}", stream=sys.stdout)

# ----------------------------------------------------------------------------#
#                           --- Module Imports ---                            #
# ----------------------------------------------------------------------------#
from topshelfsoftware_polling.polling import (  # noqa: E402
    PollAttemptLimitReached,
    PollTimeLimitReached,
    poll,
)
from topshelfsoftware_polling.step import (  # noqa: E402
    step_constant,  # noqa: F401, not used explicitly, evaluated at runtime
    step_exponential_backoff,  # noqa: F401, same as above
)


# ----------------------------------------------------------------------------#
#                                --- TESTS ---                                #
# ----------------------------------------------------------------------------#
@pytest.mark.happy
@pytest.mark.parametrize("event_dir", [MODULE_EVENTS_DIR])
@pytest.mark.parametrize(
    "event_file",
    get_json_files(MODULE_EVENTS_DIR, ["poll", "success", "truthy"]),
)
def test_01_poll_truthy(get_event_as_dict):
    print_section_break()
    logger.info(f"Test Description: {get_event_as_dict['description']}")
    _input: dict = get_event_as_dict["input"]
    lambda_fun: Callable = eval(_input["lambda_function"])
    poll_kwargs: dict = _input["poll_kwargs"]
    expected_output: dict = get_event_as_dict["expected_output"]

    res = poll(
        lambda_fun,
        **poll_kwargs,
    )
    assert res == expected_output["res"]


@pytest.mark.sad
@pytest.mark.parametrize("event_dir", [MODULE_EVENTS_DIR])
@pytest.mark.parametrize(
    "event_file",
    get_json_files(MODULE_EVENTS_DIR, ["poll", "error", "poll_exc"]),
)
def test_02_poll_poll_exception(get_event_as_dict):
    print_section_break()
    logger.info(f"Test Description: {get_event_as_dict['description']}")
    _input: dict = get_event_as_dict["input"]
    lambda_fun: Callable = eval(_input["lambda_function"])
    poll_kwargs: dict = _input["poll_kwargs"]
    poll_kwargs["step_fun"] = eval(poll_kwargs["step_fun"])
    expected_error: dict = get_event_as_dict["expected_output"]["error"]

    with pytest.raises(
        (PollAttemptLimitReached, PollTimeLimitReached),
        match=re.escape(expected_error["message"]),
    ):
        poll(
            lambda_fun,
            **poll_kwargs,
        )


@pytest.mark.sad
@pytest.mark.parametrize("event_dir", [MODULE_EVENTS_DIR])
@pytest.mark.parametrize(
    "event_file",
    get_json_files(MODULE_EVENTS_DIR, ["poll", "error", "ignore_exc"]),
)
def test_03_poll_ignore_exception(get_event_as_dict):
    print_section_break()
    logger.info(f"Test Description: {get_event_as_dict['description']}")
    _input: dict = get_event_as_dict["input"]
    lambda_fun: Callable = eval(_input["lambda_function"])
    poll_kwargs: dict = _input["poll_kwargs"]
    poll_kwargs["ignore_exceptions"] = tuple(
        eval(exc) for exc in poll_kwargs["ignore_exceptions"]
    )
    expected_error: dict = get_event_as_dict["expected_output"]["error"]

    with pytest.raises(
        eval(expected_error["type"]),
        match=re.escape(expected_error["message"]),
    ):
        poll(
            lambda_fun,
            **poll_kwargs,
        )


@pytest.mark.sad
@pytest.mark.parametrize("event_dir", [MODULE_EVENTS_DIR])
@pytest.mark.parametrize(
    "event_file",
    get_json_files(MODULE_EVENTS_DIR, ["poll", "error", "raise_exc"]),
)
def test_04_poll_raise_exception(get_event_as_dict):
    print_section_break()
    logger.info(f"Test Description: {get_event_as_dict['description']}")
    _input: dict = get_event_as_dict["input"]
    lambda_fun: Callable = eval(_input["lambda_function"])
    poll_kwargs: dict = _input["poll_kwargs"]
    expected_error: dict = get_event_as_dict["expected_output"]["error"]

    with pytest.raises(
        eval(expected_error["type"]),
        match=re.escape(expected_error["message"]),
    ):
        poll(
            lambda_fun,
            **poll_kwargs,
        )
