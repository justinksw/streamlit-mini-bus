import requests

REF = "https://data.etagmb.gov.hk"


class Route:

    def __init__(self, route_code, route_seq="1") -> None:
        self.region = "NT"
        self.route_code = route_code
        self.route_seq = route_seq  # 1 OR 2 (Direction)

    def get_response(self, url) -> None:
        response = requests.get(url)

        if response.status_code != 200:
            raise Exception("Error: " + str(response.status_code))

        data = response.json()

        if not data["data"]:
            raise Exception("Error: No data.")

        return data

    # Note: Route codes will be duplicated across regions.
    # def get_region(self):
    #     # https://data.etagmb.gov.hk/route

    #     url = f"{REF}/route"
    #     data = self.get_response(url)

    #     HKI = data["data"]["routes"]["HKI"]
    #     KLN = data["data"]["routes"]["KLN"]
    #     NT = data["data"]["routes"]["NT"]

    #     if self.route_code in HKI:
    #         return "HKI"
    #     elif self.route_code in KLN:
    #         return "KLN"
    #     elif self.route_code in NT:
    #         return "NT"
    # else:
    #     raise Exception("Error: Invalid route code.")

    def get_route_id(self):
        # https://data.etagmb.gov.hk/route/NT/27

        url = f"{REF}/route/{self.region}/{self.route_code}"
        data = self.get_response(url)

        return data["data"][0]["route_id"]

    def get_route_stops_id(self):
        # https://data.etagmb.gov.hk/route-stop/2007860/1

        route_id = self.get_route_id()

        url = f"{REF}/route-stop/{route_id}/{self.route_seq}"
        data = self.get_response(url)

        route_stops = data["data"]["route_stops"]
        stops_id = [i["stop_id"] for i in route_stops]

        # Return list of stop ids of the route (depends on direction)
        return stops_id

    def get_stop_coordinate(self, stop_id):
        # https://data.etagmb.gov.hk/stop/20015838

        url = f"{REF}/stop/{stop_id}"
        data = self.get_response(url)

        lat = data["data"]["coordinates"]["wgs84"]["latitude"]
        lon = data["data"]["coordinates"]["wgs84"]["longitude"]

        return (lat, lon)

    def get_route_stops_coordinates(self):

        stops_id = self.get_route_stops_id()

        coords = [self.get_stop_coordinate(i) for i in stops_id]

        lat, lon = zip(*coords)

        # Retuen two list of lat, lon of the stops in the route
        return lat, lon

    def get_eta(self):
        # https://data.etagmb.gov.hk/eta/route-stop/2007860/1/1

        route_id = self.get_route_id()
        stop_seq = "1"

        url = f"{REF}/eta/route-stop/{route_id}/{self.route_seq}/{stop_seq}"

        data = self.get_response(url)

        eta = data["data"]["eta"]  # List

        if not eta:
            raise Exception("Error: No ETA.")

        # return eta[0]["timestamp"]
        return eta


if __name__ == "__main__":
    route = Route("27")
    print(route.get_route_stops_coordinates())
