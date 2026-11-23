# ============================================================================
#  helpers.py — GIVEN CODE. Don't change this file.
# ============================================================================
#  Small tools the notebooks use:
#    banner(title)                  prints a ##### separator with a title
#    check(call, got, expected)     prints ONE [PASS] or [FAIL] line,
#                                   and gives back True (pass) or False (fail)
#    summary(task, results)         prints how many tests passed
# ============================================================================


def banner(title):
    """Print a separator so each part of the output is easy to find."""
    print()
    print("#" * 72)
    print("#  " + title)
    print("#" * 72)


def check(call, got, expected):
    """Compare what a function gave (got) with what it should give (expected).
    call is the call written out as text, so the output can show it."""
    if got == expected:
        print("  [PASS]", call, "gave", repr(got))
        return True
    print("  [FAIL]", call)
    print("           gave    ", repr(got))
    print("           expected", repr(expected))
    if got is None:
        print("           (None usually means the function isn't written yet,")
        print("            or it's missing a return)")
    return False


def summary(task, results):
    """Print how many of the checks in results passed."""
    passed = results.count(True)
    print()
    print("  " + task + ":", passed, "of", len(results), "tests passed.")
    if passed == len(results):
        print("  Well done! Move on to the next task.")
    else:
        print("  Not yet: read the [FAIL] lines above, fix your function,")
        print("  run its cell again, then run this test cell again.")
