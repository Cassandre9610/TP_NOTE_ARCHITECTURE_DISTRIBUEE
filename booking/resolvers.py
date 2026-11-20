import json
from graphql import GraphQLError

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


#TODO refactor
#TODO appels à schedule pour vérifier si le film est diffusé dans la date
def add_booking(_, info, _userid: str, _date: str, _movie_id: str): 
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
                
                if _movie_id not in existing_date["movies"]:
                    existing_date["movies"].append(_movie_id)
                #TODO else throw error
            else:
                existing_booking["dates"].append({"date":_date, "movies": _movie_id})

            _write({"bookings" : bookings})
            return existing_booking
        else :
            return create_new_booking(bookings, _userid, _date, _movie_id)


def delete_booking(_, info, _userid: str, _date: str, _movie_id: str):
    with open(DATA_PATH, "r") as file:
        bookings: list = json.load(file)["bookings"]
        for booking in bookings:
            if booking["userid"] == _userid:
                for date in booking["dates"]:
                    if date["date"] == _date:
                        date["movies"] = [movie for movie in date["movies"] if movie != _movie_id]
                        #TODO check si la liste des films a changée
                        _write({"bookings": bookings})
                        return booking
            
    raise GraphQLError("aucune donnée à supprimer")

def create_new_booking(bookings:list, _userid, _date, _movie_id):
    new_booking = {
        "userid": _userid,
        "dates": [{
            "date": _date,
            "movies": [_movie_id]
        }]
    }

    bookings.append(new_booking)
    _write({"bookings" : bookings})
    return new_booking
