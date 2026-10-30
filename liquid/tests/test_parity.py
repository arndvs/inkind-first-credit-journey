"""The library's push must say exactly what 03-message.liquid says, in every case,
including the abort reasons. If either changes alone, this fails."""
import pytest
from harness import message, render_or_abort, single_file_message
from fixtures import CASES

LIBRARY_PUSH = message("first_reward.push.liquid")
SINGLE_FILE = single_file_message()


@pytest.mark.parametrize("case", CASES)
def test_library_push_matches_03(case):
    assert render_or_abort(LIBRARY_PUSH, CASES[case]).strip() == render_or_abort(SINGLE_FILE, CASES[case]).strip()
