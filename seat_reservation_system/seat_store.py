class SeatStore:
    def __init__(self, seat_ids):
        self._seats = {seat_id: None for seat_id in seat_ids}

    def list_seats(self):
        return self._seats.items()

    def reserve(self, seat_id, name):
        current = self._get(seat_id)
        if current is not None:
            raise ValueError("Seat is already reserved.")
        self._seats[seat_id] = name
        return seat_id, name

    def cancel(self, seat_id, name=None):
        current = self._get(seat_id)
        if current is None:
            raise ValueError("Seat is not reserved.")
        if name and current != name:
            raise ValueError("Name does not match the reservation.")
        self._seats[seat_id] = None
        return seat_id, None

    def status(self, seat_id):
        return seat_id, self._get(seat_id)

    def stats(self):
        reserved = sum(1 for name in self._seats.values() if name)
        total = len(self._seats)
        return {"total": total, "reserved": reserved, "available": total - reserved}

    def _get(self, seat_id):
        if seat_id not in self._seats:
            raise ValueError("Seat does not exist.")
        return self._seats[seat_id]

    
def recommend_consecutive_seats(self, count):
        
        # Find consecutive available seats based on the requested count.
        
        # Sort seat IDs in ascending order
        all_seat_ids = sorted(self._seats.keys())
        
        # Check all seats from the beginning to find consecutive available ones
        for i in range(len(all_seat_ids) - count + 1):
            is_match = True
            current_group = []
            
            # Check if 'count' number of seats are consecutive starting from index i
            for j in range(count):
                seat_id = all_seat_ids[i + j]
                
                # Condition A: Fail if the seat is already reserved (not None)
                if self._seats[seat_id] is not None:
                    is_match = False
                    break
                
                # Condition B: Fail if seat numbers are not continuous (e.g., 10 then 21)
                if j > 0 and (seat_id - current_group[-1] != 1):
                    is_match = False
                    break
                    
                current_group.append(seat_id)
            
            # Return the seat list immediately if all conditions are met
            if is_match:
                return current_group
                
        # Return an empty list if no consecutive seats are found after checking all
        return []
