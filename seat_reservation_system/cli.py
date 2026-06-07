from seat_reservation_system.seat_store import SeatStore
from seat_reservation_system.seats import SEAT_IDS

HELP_TEXT = """Commands:
list                      - List all seats
reserve <seat_id> <name>  - Reserve a seat
cancel <seat_id> [name]   - Cancel a reservation
status <seat_id>          - Show seat status
stats                     - Show summary stats
help                      - Show this help
recommend <count>         - Recommend consecutive seats and reserve
exit                      - Exit the program"""


def run_cli():
    store = SeatStore(SEAT_IDS)
    print("Seat Reservation System CLI")
    print("Type 'help' to see available commands.")
    while True:
        try:
            raw = input("seat> ").strip()
        except EOFError:
            print()
            break
        if not raw:
            continue

        parts = raw.split()
        command, args = parts[0].lower(), parts[1:]
        if command in {"exit", "quit"}:
            break
        if command == "help":
            print(HELP_TEXT)
            continue
        try:
            if command == "list":
                for seat_id, name in store.list_seats():
                    _print_seat(seat_id, name)
            elif command == "reserve":
                _require_args(command, args, 2)
                seat_id, name = store.reserve(int(args[0]), args[1])
                _print_seat(seat_id, name)
            elif command == "cancel":
                _require_args(command, args, 1)
                name = args[1] if len(args) > 1 else None
                seat_id, name = store.cancel(int(args[0]), name)
                _print_seat(seat_id, name)
            elif command == "status":
                _require_args(command, args, 1)
                seat_id, name = store.status(int(args[0]))
                _print_seat(seat_id, name)
            elif command == "recommend":
                _require_args(command, args, 1)
                count = int(args[0])
                
                if count <= 0:
                    raise ValueError("Count must be greater than 0.")
                
                # 연석 계산 함수를 호출
                recommended_seats = store.recommend_consecutive_seats(count)
                
                if recommended_seats:
                    # 추천 좌석 리스트를 문자열로 파싱 (예: [1, 2] -> "1, 2")
                    seats_str = ", ".join(map(str, recommended_seats))
                    print(f"Recommended seats: {seats_str}")
                    
                    # 예약을 진행할지 확인
                    choice = input("Do you want to reserve these seats? (y/n): ").strip().lower()
                    if choice == "y":
                        name = input("Enter your name: ").strip()
                        if not name:
                            raise ValueError("Name cannot be empty.")
                        
                        # 찾은 연석들을 하나의 이름으로 일괄 예약 처리
                        for seat_id in recommended_seats:
                            store.reserve(seat_id, name)
                            _print_seat(seat_id, name)
                        print("Reservation completed successfully!")
                    else:
                        print("Recommendation canceled.")
                else:
                    print(f"No consecutive seats found for {count} people.")
            elif command == "stats":
                stats = store.stats()
                print(
                    "Total: {total}, Reserved: {reserved}, Available: {available}".format(
                        **stats
                    )
                )
            else:
                print("Unknown command. Type 'help' for commands.")
        except ValueError as exc:
            print(f"Error: {exc}")


def _print_seat(seat_id, name):
    label = f"reserved by {name}" if name else "available"
    print(f"Seat {seat_id}: {label}")


def _require_args(command, args, count):
    if len(args) < count:
        raise ValueError(f"Usage: {command} requires {count} argument(s).")
