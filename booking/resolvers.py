import json

DATA_PATH = '{}/data/bookings.json'.format(".")


def _write(new_file):
    with open(DATA_PATH, "w") as wfile:
        json.dump(new_file, wfile)


def get_booking_with_userid(_, info, _userid):
    with open(DATA_PATH, "r") as file:
        bookings = json.load(file)["bookings"]
        for booking in bookings:
            if booking["userid"] == _userid:
                return booking


# TODO changer movies_id pour ne pas prendre une liste (plus coherent)
def add_booking(_, info, _userid: str, _date: str, _movies_id: list): 
    with open(DATA_PATH, "r") as file:
        bookings: list = json.load(file)["bookings"]
        id_existing_booking = -1
        for i in range(len(bookings)):
            if bookings[i]["userid"] == _userid:
                id_existing_booking = i

        if id_existing_booking != -1:
            existing_booking = bookings[id_existing_booking]["userid"]

            i_existing_date = -1
            for i in range(existing_booking["dates"]):
                if existing_booking["dates"][i]["date"] == _date:
                    i_existing_date = i

            if i_existing_date != -1:
                pass
            else:
                existing_booking["dates"].append({"date":_date, "movies": _movies_id})

            _write({"bookings" : bookings})
            return existing_booking
        else :
            # TODO extraire, creation tt court
            new_booking = {
                "userid": _userid,
                "dates": [{
                    "date": _date,
                    "movies": _movies_id
                }]
            }

            bookings.append(new_booking)
            _write({"bookings" : bookings})
            return new_booking
