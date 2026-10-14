"""Manage movie theater seat reservations and ticket codes."""

import hashlib
import json


shows = {
    "SHOW-1": {"title": "Interstellar", "seats": 20, "booked": []},
    "SHOW-2": {"title": "Dangal", "seats": 10, "booked": []},
}


def reserve_seat(show_id, seat_number, system_logs=None):
    """Reserve a valid, available seat for a show."""
    if system_logs is None:
        system_logs = []

    if show_id not in shows:
        system_logs.append(f"Show {show_id} does not exist.")
        return False

    show = shows[show_id]

    try:
        seat_number = int(seat_number)
    except (TypeError, ValueError):
        system_logs.append("Seat number must be an integer.")
        return False

    if not 1 <= seat_number <= show["seats"]:
        system_logs.append(
            f"Seat {seat_number} is outside the valid range for {show_id}."
        )
        return False

    if seat_number in show["booked"]:
        system_logs.append(
            f"Seat {seat_number} already taken for {show_id}"
        )
        return False

    show["booked"].append(seat_number)
    system_logs.append(f"Reserved seat {seat_number} for {show_id}")
    return True


def release_seat(show_id, seat_number):
    """Release a previously reserved seat."""
    if show_id not in shows:
        return False

    try:
        seat_number = int(seat_number)
    except (TypeError, ValueError):
        return False

    try:
        shows[show_id]["booked"].remove(seat_number)
    except ValueError:
        return False

    return True


def ticket_code(show_id, seat_number):
    """Generate a short ticket code."""
    return hashlib.sha256(
        f"{show_id}{seat_number}".encode("utf-8")
    ).hexdigest()[:8]


def dump_reservations(file="seats.json"):
    """Save all reservations to a JSON file."""
    with open(file, "w", encoding="utf-8") as reservation_file:
        json.dump(shows, reservation_file, indent=4)


def load_reservations(file="seats.json"):
    """Load reservations from a JSON file."""
    try:
        with open(file, "r", encoding="utf-8") as reservation_file:
            data = json.load(reservation_file)
    except (OSError, json.JSONDecodeError):
        return False

    if not isinstance(data, dict):
        return False

    shows.clear()
    shows.update(data)
    return True


def print_seating_summary():
    """Print the number of free seats for each show."""
    for show_id, show in shows.items():
        free_seats = show["seats"] - len(show["booked"])
        print(
            f"{show['title']}: {free_seats} seats free, "
            f"booked = {show['booked']}"
        )


def main():
    """Run the sample reservation workflow."""
    reserve_seat("SHOW-1", 5)
    reserve_seat("SHOW-1", 5)
    reserve_seat("SHOW-1", 25)
    reserve_seat("SHOW-2", -1)
    reserve_seat("SHOW-2", "A7")
    release_seat("SHOW-2", 3)

    print("Ticket code:", ticket_code("SHOW-1", 5))

    seat = input(
        "Seat number to book for SHOW-2 (Enter for 4): "
    ) or "4"

    logs = []
    reserve_seat("SHOW-2", seat, logs)

    for log in logs:
        print(log)

    dump_reservations()
    load_reservations()
    print_seating_summary()

    


if __name__ == "__main__":
    main()
