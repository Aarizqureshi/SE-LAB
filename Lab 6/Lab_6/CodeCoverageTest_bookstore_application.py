
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


def test_invalid_batches():
    with pytest.raises(ValueError):
        process_book_buybacks("invalid", 5.0)


def test_negative_bonus():
    with pytest.raises(ValueError):
        process_book_buybacks([], -1.0)


def test_unapproved_batch():
    result = process_book_buybacks(
        [make_batch(approved=False)], 5.0
    )
    assert result["status"] == "ZERO_CREDIT"


@pytest.mark.parametrize(
    "format,expected",
    [
        ("paperback", 8.0),
        ("hardcover", 15.0),
        ("textbook", 40.0),
    ],
)
def test_valid_formats(format, expected):
    result = process_book_buybacks(
        [make_batch(format=format)], 5.0
    )
    assert result["total_payout"] == expected
    assert result["status"] == "COMPLETED"


def test_unknown_format():
    result = process_book_buybacks(
        [make_batch(format="magazine")], 5.0
    )
    assert result["status"] == "ZERO_CREDIT"


@pytest.mark.parametrize(
    "condition,multiplier",
    [
        ("mint", 1.25),
        ("poor", 0.40),
        ("good", 1.0),
    ],
)
def test_conditions(condition, multiplier):
    result = process_book_buybacks(
        [make_batch(condition=condition)], 5.0
    )
    assert result["total_payout"] == round(8.0 * multiplier, 2)


def test_missing_pages():
    result = process_book_buybacks(
        [make_batch(missing_pages=2)], 5.0
    )
    assert result["status"] == "ZERO_CREDIT"


def test_counterfeit_paperback():
    result = process_book_buybacks(
        [make_batch(counterfeit=True)], 5.0
    )
    assert result["status"] == "ZERO_CREDIT"


def test_counterfeit_textbook_resets_batch():
    result = process_book_buybacks(
        [make_batch(
            format="textbook",
            books=[
                {"missing_pages": 0, "condition": "good",
                 "counterfeit": False},
                {"missing_pages": 0, "condition": "good",
                 "counterfeit": True},
            ],
        )],
        5.0,
    )
    assert result["total_payout"] == 0.0
    assert result["status"] == "ZERO_CREDIT"


def test_store_credit_bonus():
    result = process_book_buybacks(
        [make_batch(credit=True)], 5.0
    )
    assert result["total_payout"] == 13.0


def test_more_than_four_rejections():
    batches = [
        make_batch(missing_pages=1)
        for _ in range(5)
    ]
    result = process_book_buybacks(batches, 5.0)
    assert result["status"] == "AUDIT_REJECTED"


def test_multiple_books():
    result = process_book_buybacks(
        [make_batch(
            books=[
                {"missing_pages": 0, "condition": "mint",
                 "counterfeit": False},
                {"missing_pages": 0, "condition": "poor",
                 "counterfeit": False},
            ],
        )],
        5.0,
    )
    assert result["total_payout"] == 13.2


def test_scanner_no_data():
    assert inspect_scanner_calibration([]) == "NO_DATA"


def test_scanner_calibrated():
    assert inspect_scanner_calibration(
        [[1, 6, 2, 7]]
    ) == "CALIBRATED"


def test_scanner_recalibrate():
    assert inspect_scanner_calibration(
        [[6, 7]]
    ) == "RECALIBRATE"


def test_scanner_threshold_resets_streak():
    assert inspect_scanner_calibration(
        [[6, 5, 7]]
    ) == "CALIBRATED"


def test_scanner_recalibrates_after_two_errors():
    assert inspect_scanner_calibration(
        [[1, 6, 6]]
    ) == "RECALIBRATE"


def test_scanner_multiple_devices():
    assert inspect_scanner_calibration(
        [[6], [7, 7]]
    ) == "RECALIBRATE"


def test_scanner_empty_device():
    assert inspect_scanner_calibration([[]]) == "CALIBRATED"
