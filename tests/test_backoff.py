import os
import sys

import pytest

from topshelfsoftware_util.log import get_logger

from conftest import get_json_files, print_section_break

# ----------------------------------------------------------------------------#
#                               --- Globals ---                               #
# ----------------------------------------------------------------------------#
from __setup__ import TEST_EVENTS_PATH

MODULE = "backoff"
MODULE_EVENTS_DIR = os.path.join(TEST_EVENTS_PATH, MODULE)

# ----------------------------------------------------------------------------#
#                               --- Logging ---                               #
# ----------------------------------------------------------------------------#
logger = get_logger(f"test_{MODULE}", stream=sys.stdout)

# ----------------------------------------------------------------------------#
#                           --- Module Imports ---                            #
# ----------------------------------------------------------------------------#
from topshelfsoftware_polling.backoff import (  # noqa: E402
    backoff_exponential_with_full_jitter,
    backoff_linear,
)


# ----------------------------------------------------------------------------#
#                                --- TESTS ---                                #
# ----------------------------------------------------------------------------#
@pytest.mark.happy
@pytest.mark.parametrize("event_dir", [MODULE_EVENTS_DIR])
@pytest.mark.parametrize(
    "event_file",
    get_json_files(MODULE_EVENTS_DIR, ["backoff_linear", "success"]),
)
def test_01_backoff_linear(get_event_as_dict):
    print_section_break()
    logger.info(f"Test Description: {get_event_as_dict['description']}")
    kwargs: dict = get_event_as_dict["input"]
    expected_output: float = get_event_as_dict["expected_output"]

    step = backoff_linear(**kwargs)
    assert step == expected_output


@pytest.mark.happy
@pytest.mark.parametrize("event_dir", [MODULE_EVENTS_DIR])
@pytest.mark.parametrize(
    "event_file",
    get_json_files(
        MODULE_EVENTS_DIR, ["backoff_exponential_with_full_jitter", "success"]
    ),
)
def test_02_backoff_exponential_with_full_jitter(get_event_as_dict):
    print_section_break()
    logger.info(f"Test Description: {get_event_as_dict['description']}")
    kwargs: dict = get_event_as_dict["input"]
    expected_output: dict = get_event_as_dict["expected_output"]

    step = backoff_exponential_with_full_jitter(**kwargs)
    assert step >= expected_output["min"] and step <= expected_output["max"]
