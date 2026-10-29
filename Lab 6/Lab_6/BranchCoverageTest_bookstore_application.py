
import pytest
from bookstore_trade_in import (
    process_book_buybacks,
    inspect_scanner_calibration,
)


def make_batch(
    format="paperback",
    condition="good",
    missing_pages=0,
    counterfeit=False,
    approved=True,
    credit=False,
    books=None,
):
    return {
        "intake_approved": approved,
        "format": format,
        "payout_in_credit": credit,
        "books": books if books is not None else [
            {
                "missing_pages": missing_pages,
                "condition": condition,
                "counterfeit": counterfeit,
            }
        ],
    }


# Input validation branches

def test_invalid_batches_type():
    with pytest.raises(ValueError):
        process_book_buybacks(None, 5.0)


def test_negative_store_credit_bonus():
    with pytest.raises(ValueError):
        process_book_buybacks([], -1.0)


# Intake approval branches

def test_intake_approved():
    result = process_book_buybacks([make_batch()], 5.0)
    assert result["status"] == "COMPLETED"


def test_intake_not_approved():
    result = process_book_buybacks(
        [make_batch(approved=False)], 5.0
    )
    assert result["status"] == "ZERO_CREDIT"


# Format selection branches

@pytest.mark.parametrize(
    "format,expected",
    [
        ("textbook", 40.0),
        ("hardcover", 15.0),
        ("paperback", 8.0),
    ],
)
def test_each_supported_format(format, expected):
    result = process_book_buybacks(
        [make_batch(format=format)], 5.0
    )
    assert result["total_payout"] == expected


def test_unsupported_format():
    result = process_book_buybacks(
        [make_batch(format="magazine")], 5.0
    )
    assert result["status"] == "ZERO_CREDIT"


def test_missing_format_defaults_to_paperback():
    batch = {
        "intake_approved": True,
        "payout_in_credit": False,
        "books": [
            {"missing_pages": 0, "condition": "good",
             "counterfeit": False}
        ],
    }
    result = process_book_buybacks([batch], 5.0)
    assert result["total_payout"] == 8.0


# Missing pages and counterfeit branches

def test_book_with_missing_pages():
    result = process_book_buybacks(
        [make_batch(missing_pages=1)], 5.0
    )
    assert result["status"] == "ZERO_CREDIT"


def test_book_without_missing_pages():
    result = process_book_buybacks(
        [make_batch(missing_pages=0)], 5.0
    )
    assert result["total_payout"] == 8.0


def test_counterfeit_non_textbook():
    result = process_book_buybacks(
        [make_batch(counterfeit=True)], 5.0
    )
    assert result["status"] == "ZERO_CREDIT"


def test_non_counterfeit_book():
    result = process_book_buybacks(
        [make_batch(counterfeit=False)], 5.0
    )
    assert result["total_payout"] == 8.0


def test_counterfeit_textbook_breaks_loop():
    batch = make_batch(
        format="textbook",
        books=[
            {"missing_pages": 0, "condition": "good",
             "counterfeit": False},
            {"missing_pages": 0, "condition": "good",
             "counterfeit": True},
            {"missing_pages": 0, "condition": "mint",
             "counterfeit": False},
        ],
    )
    result = process_book_buybacks([batch], 5.0)
    assert result["total_payout"] == 0.0


# Condition branches

@pytest.mark.parametrize(
    "condition,expected",
    [
        ("mint", 10.0),
        ("poor", 3.2),
        ("good", 8.0),
        ("fair", 8.0),
    ],
)
def test_condition_branches(condition, expected):
    result = process_book_buybacks(
        [make_batch(condition=condition)], 5.0
    )
    assert result["total_payout"] == expected


def test_missing_condition_defaults_to_good():
    batch = {
        "intake_approved": True,
        "format": "paperback",
        "payout_in_credit": False,
        "books": [
            {"missing_pages": 0, "counterfeit": False}
        ],
    }
    result = process_book_buybacks([batch], 5.0)
    assert result["total_payout"] == 8.0


# Store credit, rejection count, and return status branches

def test_credit_bonus_enabled():
    result = process_book_buybacks(
        [make_batch(credit=True)], 5.0
    )
    assert result["total_payout"] == 13.0


def test_credit_bonus_disabled():
    result = process_book_buybacks(
        [make_batch(credit=False)], 5.0
    )
    assert result["total_payout"] == 8.0


def test_exactly_four_rejections():
    batches = [
        make_batch(missing_pages=1)
        for _ in range(4)
    ]
    result = process_book_buybacks(batches, 5.0)
    assert result["status"] == "ZERO_CREDIT"


def test_more_than_four_rejections():
    batches = [
        make_batch(missing_pages=1)
        for _ in range(5)
    ]
    result = process_book_buybacks(batches, 5.0)
    assert result["status"] == "AUDIT_REJECTED"


def test_zero_credit():
    result = process_book_buybacks([], 5.0)
    assert result["status"] == "ZERO_CREDIT"


def test_completed_payout():
    result = process_book_buybacks(
        [make_batch()], 5.0
    )
    assert result["status"] == "COMPLETED"


# Scanner calibration branches

def test_empty_scanner_matrix():
    assert inspect_scanner_calibration([]) == "NO_DATA"


def test_error_rate_above_five():
    assert inspect_scanner_calibration([[6]]) == "CALIBRATED"


def test_error_rate_equal_to_five_resets_streak():
    assert inspect_scanner_calibration([[6, 5, 7]]) == "CALIBRATED"


def test_error_rate_below_five_resets_streak():
    assert inspect_scanner_calibration([[6, 4, 7]]) == "CALIBRATED"


def test_two_consecutive_errors_trigger_recalibration():
    assert inspect_scanner_calibration([[6, 7]]) == "RECALIBRATE"


def test_single_error_does_not_trigger_recalibration():
    assert inspect_scanner_calibration([[6, 2, 7]]) == "CALIBRATED"


def test_recalibration_across_device_iteration():
    assert inspect_scanner_calibration([[6], [7, 7]]) == "RECALIBRATE"


def test_empty_device_readings():
    assert inspect_scanner_calibration([[]]) == "CALIBRATED"
