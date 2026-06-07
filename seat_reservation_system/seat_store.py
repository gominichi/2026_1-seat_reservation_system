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
        """
        원하는 인원수(count)만큼 연속된 빈 자리가 있는지 찾아주는 함수
        """
        # 먼저 좌석 번호(ID)들을 정수형으로 순서대로 정렬
        all_seat_ids = sorted(self._seats.keys())
        
        # 전체 좌석을 처음부터 끝까지 검사 후 연속된 빈 자리 탐색
        for i in range(len(all_seat_ids) - count + 1):
            is_match = True
            current_group = []
            
            # i번째 좌석부터 시작해서 count 개수만큼 연속되어 있는지 확인
            for j in range(count):
                seat_id = all_seat_ids[i + j]
                
                # 조건 A: 좌석이 이미 예약되어 있으면( = None이 아니면 ) 탈락!
                if self._seats[seat_id] is not None:
                    is_match = False
                    break
                
                # 조건 B: 앞 자리와 번호가 연속되지 않고 끊겨 있다면( ex: 10번 다음 21번 ) 탈락!
                if j > 0 and (seat_id - current_group[-1] != 1):
                    is_match = False
                    break
                    
                current_group.append(seat_id)
            
            # 모든 조건을 통과해 원하는 개수만큼 연속된 빈 자리를 찾았다면 즉시 반환
            if is_match:
                return current_group
                
        # 끝까지 다 돌았는데도 연속된 자리가 없다면 빈 리스트를 반환
        return []
