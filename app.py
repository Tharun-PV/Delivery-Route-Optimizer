# from flask import Flask, render_template, request, jsonify
# import csv
# import os
# import networkx as nx
# from geopy.distance import geodesic

# app = Flask(__name__)

# def read_csv(file_path):
#     with open(file_path, 'r', encoding='utf-8-sig') as file:
#         csvreader = csv.DictReader(file)
#         return list(csvreader)

# def calculate_distances(locations):
#     G = nx.DiGraph()
#     for i, loc1 in enumerate(locations):
#         for j, loc2 in enumerate(locations):
#             if i != j:
#                 dist = geodesic((float(loc1['lat']), float(loc1['lon'])), (float(loc2['lat']), float(loc2['lon']))).kilometers
#                 G.add_edge(i, j, weight=dist)
#     return G

# def clarke_wright_savings(G, depot):
#     savings = []
#     for i in G.nodes:
#         if i == depot:
#             continue
#         for j in G.nodes:
#             if j == depot or i == j:
#                 continue
#             saving = G[depot][i]['weight'] + G[depot][j]['weight'] - G[i][j]['weight']
#             savings.append((saving, i, j))
#     savings.sort(reverse=True)

#     routes = {i: [depot, i, depot] for i in G.nodes if i != depot}
#     for saving, i, j in savings:
#         if routes[i][-2] == depot and routes[j][1] == depot:
#             new_route = routes[i][:-1] + routes[j][1:]
#             if len(new_route) <= len(G.nodes) - 1:
#                 routes[i] = new_route
#                 del routes[j]

#     return list(routes.values())

# def calculate_metrics(route, G):
#     distance = 0
#     for i in range(len(route) - 1):
#         distance += G[route[i]][route[i + 1]]['weight']
#     return distance, distance / 40 * 60

# @app.route('/', methods=['GET', 'POST'])
# def index():
#     if request.method == 'POST':
#         coordinates_data = []

#         if 'csv-upload' in request.files and request.files['csv-upload'].filename != '':
#             file = request.files['csv-upload']
#             if file.filename.endswith('.csv'):
#                 file_path = os.path.join('DATA.csv')
#                 file.save(file_path)

#                 data = read_csv(file_path)
#                 locations = [{'lat': row['Co-Ordinates'].split(',')[0], 'lon': row['Co-Ordinates'].split(',')[1]} for row in data]
#                 G = calculate_distances(locations)
#                 depot = 0
#                 routes = clarke_wright_savings(G, depot)
#                 metrics = [calculate_metrics(route, G) for route in routes]

#                 print("Routes:", routes)
#                 print("Metrics:", metrics)

#                 result = []
#                 for i, route in enumerate(routes):
#                     for j, node in enumerate(route[:-1]):
#                         result.append({'type': 'delivery', 'coords': locations[node], 'route': i, 'index': j})
#                     result.append({'type': 'hub', 'coords': locations[depot], 'route': i, 'index': -1})

#                 return jsonify({'routes': result, 'metrics': metrics})

#         hub_coordinates = request.form.get('hub-coordinates')
#         delivery_locations = [hub_coordinates]

#         for key in request.form.keys():
#             if key.startswith('location-'):
#                 delivery_locations.append(request.form.get(key))

#         with open('DATA.csv', 'w', newline='') as csvfile:
#             csvwriter = csv.writer(csvfile)
#             csvwriter.writerow(["S.No", "Co-Ordinates"])
#             csvwriter.writerow([1, hub_coordinates])
#             for i, location in enumerate(delivery_locations[1:], start=2):
#                 csvwriter.writerow([i, location])

#         coordinates_data.append({'type': 'hub', 'coords': {'lat': hub_coordinates.split(',')[0], 'lon': hub_coordinates.split(',')[1]}})
#         for i, location in enumerate(delivery_locations[1:], start=1):
#             coords = {'lat': location.split(',')[0], 'lon': location.split(',')[1]}
#             coordinates_data.append({'type': 'delivery', 'coords': coords, 'route': 0, 'index': i})

#         G = calculate_distances([{'lat': loc.split(',')[0], 'lon': loc.split(',')[1]} for loc in delivery_locations])
#         depot = 0
#         routes = clarke_wright_savings(G, depot)
#         metrics = [calculate_metrics(route, G) for route in routes]

#         print("Routes:", routes)
#         print("Metrics:", metrics)

#         return jsonify({'routes': coordinates_data, 'metrics': metrics})

#     return render_template('index.html')

# if __name__ == '__main__':
#     app.run(debug=True)

###############################################################################################################################################

from flask import Flask, render_template, request, jsonify
import csv
import os
import networkx as nx
from geopy.distance import geodesic

app = Flask(__name__)


def read_csv(file_path):
    with open(file_path, 'r', encoding='utf-8-sig') as file:
        csvreader = csv.DictReader(file)
        return list(csvreader)


def calculate_distances(locations):
    G = nx.DiGraph()
    for i, loc1 in enumerate(locations):
        for j, loc2 in enumerate(locations):
            if i != j:
                dist = geodesic((float(loc1['lat']), float(loc1['lon'])), (float(
                    loc2['lat']), float(loc2['lon']))).kilometers
                G.add_edge(i, j, weight=dist)
    return G


def clarke_wright_savings(G, depot):
    savings = []
    for i in G.nodes:
        if i == depot:
            continue
        for j in G.nodes:
            if j == depot or i == j:
                continue
            saving = G[depot][i]['weight'] + \
                G[depot][j]['weight'] - G[i][j]['weight']
            savings.append((saving, i, j))
    savings.sort(reverse=True)

    routes = {i: [depot, i, depot] for i in G.nodes if i != depot}
    for saving, i, j in savings:
        if routes[i][-2] == depot and routes[j][1] == depot:
            new_route = routes[i][:-1] + routes[j][1:]
            if len(new_route) <= len(G.nodes) - 1:
                routes[i] = new_route
                del routes[j]

    return list(routes.values())


def calculate_metrics(route, G):
    distance = 0
    for i in range(len(route) - 1):
        distance += G[route[i]][route[i + 1]]['weight']
    return distance, distance / 40 * 60


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        coordinates_data = []

        if 'csv-upload' in request.files and request.files['csv-upload'].filename != '':
            file = request.files['csv-upload']
            if file.filename.endswith('.csv'):
                file_path = os.path.join('DATA.csv')
                file.save(file_path)

                data = read_csv(file_path)
                locations = [{'lat': row['Co-Ordinates'].split(
                    ',')[0], 'lon': row['Co-Ordinates'].split(',')[1]} for row in data]
                G = calculate_distances(locations)
                depot = 0
                routes = clarke_wright_savings(G, depot)
                metrics = [calculate_metrics(route, G) for route in routes]

                print("Routes:", routes)
                print("Metrics:", metrics)

                result = []
                # Dispatch Hub at Row 2 (index 1)
                result.append(
                    {'type': 'hub', 'coords': locations[0], 'route': 0, 'index': -1})

                # Delivery Locations from Row 3 onwards (index 2+)
                for i, location in enumerate(locations[1:], start=1):
                    result.append(
                        {'type': 'delivery', 'coords': location, 'route': 0, 'index': i})

                return jsonify({'routes': result, 'metrics': metrics})

        hub_coordinates = request.form.get('hub-coordinates')
        delivery_locations = [hub_coordinates]

        for key in request.form.keys():
            if key.startswith('location-'):
                delivery_locations.append(request.form.get(key))

        with open('DATA.csv', 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(["S.No", "Co-Ordinates"])
            csvwriter.writerow([1, hub_coordinates])
            for i, location in enumerate(delivery_locations[1:], start=2):
                csvwriter.writerow([i, location])

        coordinates_data.append({'type': 'hub', 'coords': {
                                'lat': hub_coordinates.split(',')[0], 'lon': hub_coordinates.split(',')[1]}})
        for i, location in enumerate(delivery_locations[1:], start=1):
            coords = {'lat': location.split(
                ',')[0], 'lon': location.split(',')[1]}
            coordinates_data.append(
                {'type': 'delivery', 'coords': coords, 'route': 0, 'index': i})

        G = calculate_distances([{'lat': loc.split(',')[0], 'lon': loc.split(',')[
                                1]} for loc in delivery_locations])
        depot = 0
        routes = clarke_wright_savings(G, depot)
        metrics = [calculate_metrics(route, G) for route in routes]

        print("Routes:", routes)
        print("Metrics:", metrics)

        return jsonify({'routes': coordinates_data, 'metrics': metrics})

    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)

###############################################################################################################################
