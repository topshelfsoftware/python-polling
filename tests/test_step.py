import os
import sys

import pytest

from topshelfsoftware_logging import get_logger

from conftest import get_json_files, print_section_break

# ----------------------------------------------------------------------------#
#                               --- Globals ---                               #
# ----------------------------------------------------------------------------#
from __setup__ import TEST_EVENTS_PATH

MODULE = "step"
MODULE_EVENTS_DIR = os.path.join(TEST_EVENTS_PATH, MODULE)

# ----------------------------------------------------------------------------#
#                               --- Logging ---                               #
# ----------------------------------------------------------------------------#
logger = get_logger(f"test_{MODULE}", stream=sys.stdout)

# ----------------------------------------------------------------------------#
#                           --- Module Imports ---                            #
# ----------------------------------------------------------------------------#
from topshelfsoftware_polling.step import (  # noqa: E402
    step_constant,
    step_exponential_backoff_with_jitter,
    step_linear_backoff,
)


# ----------------------------------------------------------------------------#
#                                --- TESTS ---                                #
# ----------------------------------------------------------------------------#
@pytest.mark.happy
@pytest.mark.parametrize("event_dir", [MODULE_EVENTS_DIR])
@pytest.mark.parametrize(
    "event_file",
    get_json_files(MODULE_EVENTS_DIR, ["step_constant", "success"]),
)
def test_01_step_constant(get_event_as_dict):
    print_section_break()
    logger.info(f"Test Description: {get_event_as_dict['description']}")
    kwargs: dict = get_event_as_dict["input"]
    expected_output: float = get_event_as_dict["expected_output"]

    step = step_constant(**kwargs)
    assert step == expected_output


@pytest.mark.happy
@pytest.mark.parametrize("event_dir", [MODULE_EVENTS_DIR])
@pytest.mark.parametrize(
    "event_file",
    get_json_files(MODULE_EVENTS_DIR, ["step_linear_backoff", "success"]),
)
def test_02_step_linear_backoff(get_event_as_dict):
    print_section_break()
    logger.info(f"Test Description: {get_event_as_dict['description']}")
    kwargs: dict = get_event_as_dict["input"]
    expected_output: float = get_event_as_dict["expected_output"]

    step = step_linear_backoff(**kwargs)
    assert step == expected_output


@pytest.mark.happy
@pytest.mark.parametrize("event_dir", [MODULE_EVENTS_DIR])
@pytest.mark.parametrize(
    "event_file",
    get_json_files(
        MODULE_EVENTS_DIR, ["step_exponential_backoff_with_jitter", "success"]
    ),
)
def test_03_step_exponential_backoff_with_jitter(get_event_as_dict):
    print_section_break()
    logger.info(f"Test Description: {get_event_as_dict['description']}")
    kwargs: dict = get_event_as_dict["input"]
    expected_output: dict = get_event_as_dict["expected_output"]

    step = step_exponential_backoff_with_jitter(**kwargs)
    assert step >= expected_output["min"] and step <= expected_output["max"]
