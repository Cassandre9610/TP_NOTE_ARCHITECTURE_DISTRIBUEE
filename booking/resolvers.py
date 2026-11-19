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


def add_booking(_, info, _userid: str, _date: str, _movies_id: list): 
    with open(DATA_PATH, "r") as file:
        bookings: list = json.load(file)["bookings"]
        id_existing_booking = -1
        for i in range(len(bookings)):
            if bookings[i]["userid"] == _userid:
                id_existing_booking = i

        if id_existing_booking != -1:
            existing_booking = bookings[id_existing_booking]

            i_existing_date = -1
            for i in range(len(existing_booking["dates"])):
                if existing_booking["dates"][i]["date"] == _date:
                    i_existing_date = i
                    break

            if i_existing_date != -1:
                existing_date: list = existing_booking["dates"][i_existing_date]
                for id in _movies_id:
                    if id not in existing_date["movies"]:
                        existing_date["movies"].append(id)
            else:
                existing_booking["dates"].append({"date":_date, "movies": _movies_id})

            _write({"bookings" : bookings})
            return existing_booking
        else :
            return create_new_booking(bookings, _userid, _date, _movies_id)


def create_new_booking(bookings:list, _userid, _date, _movies_id):
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
