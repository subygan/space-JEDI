import execjs

def execute_js_and_capture_logs(js_code):
    ctx = execjs.compile(js_code)
    logs = ctx.call("updateDebris")
    return logs

def get_all_points(filename):
	with open(filename, 'r') as file:
	    js_code = file.read()
	    print(js_code, filename)
	console_logs = execute_js_and_capture_logs(js_code)
	data = []
	for i,log in enumerate(console_logs):
		dat = {"id": i, "name": log['name'], 'lat': log['lat'], 'lng': log['lng'], 'alt': log['alt'], 'color': log['color']}
		data.append(dat)
	return data

import math

def haversine_distance(lat1, lon1, alt1, lat2, lon2, alt2):
    # Earth's radius in kilometers
    earth_radius = 6371

    # Convert latitude and longitude from degrees to radians
    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)

    # Differences in coordinates
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    dalt = alt2 - alt1

    # Haversine formula
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    # Calculate the distance
    distance = earth_radius * c

    # Add altitude difference to the distance (assuming altitude is in kilometers)
    distance_with_altitude = math.sqrt(distance ** 2 + dalt ** 2)

    return distance_with_altitude


def optimize(data, distance_bound=20000):
	iss = [row for row in data if "ZARYA" in row["name"]][0]
	total_distance = 0
	ids_in_path = []
	curr_path = [iss]
	while(total_distance<=distance_bound):
		distances_of_non_path_points = []
		closest_indices_of_non_path_points = []
		points = [row for row in data if row["id"] not in ids_in_path]
		points = [p for p in points if p['color']=='white']
		for point in points:
			d = [haversine_distance(point['lat'], point['lng'], point['alt'], p['lat'], p['lng'], p['alt']) for p in curr_path]
			minimal_distance_to_path = min(d)
			closest_index_in_current_path = d.index(minimal_distance_to_path)
			distances_of_non_path_points.append(minimal_distance_to_path)
			closest_indices_of_non_path_points.append(closest_index_in_current_path)
		to_add_point_idx = distances_of_non_path_points.index(min(distances_of_non_path_points))
		ids_in_path.append(points[to_add_point_idx]["id"])
		closest_index_in_current_path = closest_indices_of_non_path_points[to_add_point_idx]
		total_distance += min(distances_of_non_path_points)
		if closest_index_in_current_path==0:
			curr_path = [curr_path[0]] + [points[to_add_point_idx]] + curr_path[1:]
		else:
			curr_path = curr_path[:closest_index_in_current_path] + [points[to_add_point_idx]] + curr_path[closest_index_in_current_path:]
	return curr_path

import numpy as np

def add_intermediate_nodes(points, max_distance=1.0):
    interpolated_points = [points[0]]
    points.append(points[0])
    
    for i in range(len(points) - 1):
        start_point = np.array(points[i])
        end_point = np.array(points[i + 1])
        
        # Calculate the Euclidean distance between start and end points
        distance = np.linalg.norm(end_point - start_point)
        
        # Calculate the number of intermediate points needed
        num_intermediates = int(np.ceil(distance / max_distance))
        
        # Interpolate between start and end points
        if num_intermediates > 0:
            step = (end_point - start_point) / (num_intermediates + 1)
            for j in range(1, num_intermediates + 1):
                interpolated_point = start_point + j * step
                interpolated_points.append(interpolated_point.tolist())
        
        interpolated_points.append(end_point.tolist())
    
    return interpolated_points

def great_circle_interpolation_with_max_distance(points, max_distance=1.0):
    # Earth's radius in kilometers
    earth_radius = 6371

    interpolated_points = [points[0]]

    for i in range(len(points) - 1):
        lat0, lon0, alt0 = points[i]
        lat1, lon1, alt1 = points[i + 1]

        # Convert latitude and longitude from degrees to radians
        lat0 = math.radians(lat0)
        lon0 = math.radians(lon0)
        lat1 = math.radians(lat1)
        lon1 = math.radians(lon1)

        # Calculate the angular distance between the two points
        angular_distance = math.acos(
            math.sin(lat0) * math.sin(lat1) +
            math.cos(lat0) * math.cos(lat1) * math.cos(lon1 - lon0)
        )

        # Calculate the number of intermediate points needed
        num_intermediates = int(math.ceil(angular_distance * earth_radius / max_distance))

        if num_intermediates > 0:
            for j in range(1, num_intermediates + 1):
                alpha = j / (num_intermediates + 1)
                lat = math.asin(
                    math.sin((1 - alpha) * lat0) * math.cos(alpha * lat1) +
                    math.cos((1 - alpha) * lat0) * math.sin(alpha * lat1) * math.cos(angular_distance)
                )
                lon_diff = math.atan2(
                    math.sin(alpha * lon1 - (1 - alpha) * lon0) * math.sin(angular_distance),
                    math.cos((1 - alpha) * lat0) * math.cos(alpha * lat1) -
                    math.sin((1 - alpha) * lat0) * math.sin(alpha * lat1) * math.cos(angular_distance)
                )
                lon = lon0 + lon_diff

                # Calculate altitude (linear interpolation)
                alt = alt0 + alpha * (alt1 - alt0)

                # Convert latitude and longitude back to degrees
                lat = math.degrees(lat)
                lon = math.degrees(lon)

                interpolated_points.append((lat, lon, alt))

        interpolated_points.append((lat1, lon1, alt1))

    return interpolated_points

def main_midder(filename):
	data = get_all_points(filename)
	curr_path = optimize(data)
	proper_path = add_intermediate_nodes([[c['lat'], c['lng'], c['alt']] for c in curr_path], 0.5)
	path = [[str(p[0]), str(p[1]), str(p[2]), 'green'] for p in proper_path]
	return path