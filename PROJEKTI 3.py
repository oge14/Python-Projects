"""
COMP.CS.100 Programming 1
Name: Oskari Kuisma
Student Id: 151237366
Email: oskari.kuisma@tuni.fi
Project 3: Travel route optimizer.
"""

def find_route(data, departure, destination):
    """
    This function tries to find a route between <departure>
    and <destination> cities. It assumes the existence of
    the two functions fetch_neighbours and distance_to_neighbour
    (see the assignment and the function templates below).
    They are used to get the relevant information from the data
    structure <data> for find_route to be able to do the search.
    The return value is a list of cities one must travel through
    to get from <departure> to <destination>. If for any
    reason the route does not exist, the return value is
    an empty list [].
    :param data: ?????, A data structure of an unspecified type (you decide)
           which contains the distance information between the cities.
    :param departure: str, the name of the departure city.
    :param destination: str, the name of the destination city.
    :return: list[str], a list of cities the route travels through, or
           an empty list if the route can not be found. If the departure
           and the destination cities are the same, the function returns
           a two element list where the departure city is stores twice.
    """
    if departure not in data:
        return []
    elif departure == destination:
        return [departure, destination]
    greens = {departure}
    deltas = {departure: 0}
    came_from = {departure: None}
    while True:
        if destination in greens:
            break
        red_neighbours = []
        for city in greens:
            for neighbour in fetch_neighbours(data, city):
                if neighbour not in greens:
                    delta = deltas[city] + distance_to_neighbour(data, city, neighbour)
                    red_neighbours.append((city, neighbour, delta))
        if not red_neighbours:
            return []
        current_city, next_city, delta = min(red_neighbours, key=lambda x: x[2])
        greens.add(next_city)
        deltas[next_city] = delta
        came_from[next_city] = current_city
    route = []
    while True:
        route.append(destination)
        if destination == departure:
            break
        destination = came_from.get(destination)
    return list(reversed(route))
def read_distance_file(file_name):
    """
    Reads the distance information from <file_name> and stores it
    in a suitable data structure (you decide what kind of data
    structure to use). This data structure is also the return value,
    unless an error happens during the file reading operation.
    :param file_name: str, The name of the file to be read.
    :return: A data structure containing the information
             read from the <file_name> or None if any kind of error happens.
             The data structure to be chosen is completely up to you as long
             as all the required operations can be implemented using it.
    """
    try:
        file = open(file_name, mode="r", encoding="utf-8")
        data = {}
        for line in file:
            distances = {}
            line = line.rstrip()
            members = line.split(";")
            departure_place = members[0]
            members.remove(members[0])
            distances.update({members[0]: members[1]})
            if departure_place not in data:
                data[departure_place] = distances
            else:
                data[departure_place].update(distances)
        return data
    except OSError:
        return


def fetch_neighbours(data, city):
    """
    Returns a list of all the cities that are directly
    connected to parameter <city>. In other words, a list
    of cities where there exist an arrow from <city> to
    each element of the returned list. Return value is
    an empty list [], if <city> is unknown or if there are no
    arrows leaving from <city>.
    :param data: ?????, A data structure containing the distance
           information between the known cities.
    :param city: str, the name of the city whose neighbours we
           are interested in.
    :return: list[str], the neighbouring city names in a list.
             Returns [], if <city> is unknown (i.e. not stored as
             a departure city in <data>) or if there are no
             arrows leaving from the <city>.
    """
    if city in data:
        list_of_cities = data[city].keys()
    else:
        list_of_cities = []
    return list(list_of_cities)


def distance_to_neighbour(data, departure, destination):
    """
    Returns the distance between two neighbouring cities.
    Returns None if there is no direct connection from
    <departure> city to <destination> city. In other words
    if there is no arrow leading from <departure> city to
    <destination> city.
    :param data: Nested dictionary of departure cities, destinations
                and distance between.
    :param departure: str, the name of the departure city.
    :param destination: str, the name of the destination city.
    :return: int | None, The distance between <departure> and
           <destination>. None if there is no direct connection
           between the two cities.
    """
    try:
        if departure in data:
            return int(data[departure][destination])
    except KeyError:
        return None


def display(data):
    """
    This function displays all the data in our nested dict: Departure cities,
    their destinations and distances between. Everything in alphabetical order.
    :param data: Nested dictionary of departure cities, destinations
    and distance between.
    :return: Prints every city stored to the nested dict.
    """
    for departure, destination in sorted(data.items()):
        for key in sorted(destination):
            print(f"{departure:<13} {key:<13} {destination[key]:>5}")


def add(data, departure_city, destination_city, distance):
    """
    This function adds a new departure city and its destination and distance
    between to the nested dict.
    :param data: Nested dictionary of departure cities, destinations
            and distance between.
    :param departure_city: Departure city of the route.
    :param destination_city: Destination of the route.
    :param distance: Distance between those cities.
    :return: Does not return anything itself, but updates current data structure.
    """
    try:
        distance = int(distance)
        if departure_city in data:
            data[departure_city].update({destination_city: distance})
        else:
            data[departure_city] = {destination_city: distance}
    except ValueError:
        print(f"Error: '{distance}' is not an integer.")


def check_departure(data, departure):
    """
    This function checks if the departure city exists in our nested dict.
    :param data: Nested dictionary of departure cities, destinations
            and distance between.
    :param departure: Departure city of the route.
    :return: Bool value (True if city exists and False if it does not).
    """
    for departures, destinations in sorted(data.items()):
        for city in sorted(destinations):
            if city == departure:
                return True
    if departure not in data:
        return False


def total_distance(data, route):
    """
    This function calculates total distance of the given route. From departure
    city to nearest neighbour city etc. until the destination. Collects distance
    data from those neighbour cities and returns total distance.
    :param data: Nested dictionary of departure cities, destinations
                and distance between.
    :param route: Wanted route (From departure to destination with cities
                between.)
    :return: Total distance of the route.
    """
    total = 0
    if route[0] == route[1]:
        return total
    for i in range(len(route)):
        try:
            total += int(data[route[i]][route[i+1]])
        except IndexError:
            pass
        except KeyError:
            pass
    return total


def neighbours(data, city):
    """
    This function searches neighbour cities of the given city and prints them
    to the screen in alphabetical order with distances included.
    :param data: Nested dictionary of departure cities, destinations
    and distance between.
    :param city: Name of the city which neighbours the user wants to know.
    :return: Prints neighbour cities below another in alphabetical order.
    """
    try:
        if city not in data:
            print(f"Error: '{city}' is unknown.")
        for i in sorted(data[city]):
            print(f"{city:<13} {i:<13} {data[city][i]:>5}")
    except KeyError:
        return


def remove(data, departure_city, destination_city):
    """
    This function removes data from our nested dict.
    :param data: Nested dictionary of departure cities, destinations
    and distance between.
    :param departure_city: The name of the city to be removed.
    :param destination_city: The name of the destination city to be removed.
    :return: Updated dict without those routes we just removed.
    """
    try:
        del data[departure_city][destination_city]
    except KeyError:
        print(f"Error: missing road segment between \
'{departure_city}' and '{destination_city}'.")


def main():
    input_file = input("Enter input file name: ")
    distance_data = read_distance_file(input_file)
    if distance_data is None:
        print(f"Error: '{input_file}' can not be read.")
        return
    while True:
        action = input("Enter action> ")
        if action == "":
            print("Done and done!")
            return
        elif "display".startswith(action):
            display(distance_data)
        elif "add".startswith(action):
            departure = input("Enter departure city: ")
            destination = input("Enter destination city: ")
            distance = input("Distance: ")
            add(distance_data, departure, destination, distance)
        elif "remove".startswith(action):
            departure = input("Enter departure city: ")
            if departure not in distance_data:
                print(f"Error: '{departure}' is unknown.")
            else:
                destination = input("Enter destination city: ")
                remove(distance_data, departure, destination)
        elif "neighbours".startswith(action):
            city = input("Enter departure city: ")
            departure_city = check_departure(distance_data, city)
            if city not in distance_data.keys() and departure_city == True:
                continue
            neighbours(distance_data, city)
        elif "route".startswith(action):
            departure = input("Enter departure city: ")
            city = check_departure(distance_data, departure)
            if city == False:
                print(f"Error: '{departure}' is unknown.")
                continue
            destination = input("Enter destination city: ")
            route = find_route(distance_data, departure, destination)
            if route == []:
                print(f"No route found between '{departure}' and '{destination}'.")
                continue
            print(f'{"-".join(route)} ({total_distance(distance_data, route)} km)')
        else:
            print(f"Error: unknown action '{action}'.")
if __name__ == "__main__":
    main()