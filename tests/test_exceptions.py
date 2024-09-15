import os
import sys

import pytest

from topshelfsoftware_logging import get_logger

from conftest import get_json_files, print_section_break

# ----------------------------------------------------------------------------#
#                               --- Globals ---                               #
# ----------------------------------------------------------------------------#
from __setup__ import TEST_EVENTS_PATH

MODULE = "exceptions"
MODULE_EVENTS_DIR = os.path.join(TEST_EVENTS_PATH, MODULE)

# ----------------------------------------------------------------------------#
#                               --- Logging ---                               #
# ----------------------------------------------------------------------------#
logger = get_logger(f"test_{MODULE}", stream=sys.stdout)

# ----------------------------------------------------------------------------#
#                           --- Module Imports ---                            #
# ----------------------------------------------------------------------------#
from topshelfsoftware_polling.exceptions import (  # noqa: E402
    PollAttemptLimitReached,
    PollTimeLimitReached,
)


# ----------------------------------------------------------------------------#
#                                --- TESTS ---                                #
# ----------------------------------------------------------------------------#
@pytest.mark.sad
@pytest.mark.parametrize("event_dir", [MODULE_EVENTS_DIR])
@pytest.mark.parametrize(
    "event_file",
    get_json_files(MODULE_EVENTS_DIR, ["poll_attempt_limit_reached", "error"]),
)
def test_01_poll_attempt_limit_reached(get_event_as_dict):
    print_section_break()
    logger.info(f"Test Description: {get_event_as_dict['description']}")
    exc_msg_input: str = get_event_as_dict["input"]["exc_msg"]
    expected_output: str = get_event_as_dict["expected_output"]["exc_msg"]

    with pytest.raises(PollAttemptLimitReached):
        try:
            raise PollAttemptLimitReached(exc_msg_input)
        except Exception as e:
            assert str(e) == expected_output
            logger.error(e)
            raise e


@pytest.mark.sad
@pytest.mark.parametrize("event_dir", [MODULE_EVENTS_DIR])
@pytest.mark.parametrize(
    "event_file",
    get_json_files(MODULE_EVENTS_DIR, ["poll_time_limit_reached"]),
)
def test_02_poll_time_limit_reached(get_event_as_dict):
    print_section_break()
    logger.info(f"Test Description: {get_event_as_dict['description']}")
    exc_msg_input: str = get_event_as_dict["input"]["exc_msg"]
    expected_output: str = get_event_as_dict["expected_output"]["exc_msg"]

    with pytest.raises(PollTimeLimitReached):
        try:
            raise PollTimeLimitReached(exc_msg_input)
        except Exception as e:
            assert str(e) == expected_output
            logger.error(e)
            raise e
