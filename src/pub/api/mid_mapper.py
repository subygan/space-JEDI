import execjs
import json

G = 6.67430e-11  # Gravitational constant (m^3/kg/s^2)
M = 5.972e24     # Mass of the Earth (kg)
R_earth = 6371e3 # Radius of the Earth (meters)

def execute_js_and_capture_logs(js_code):
    ctx = execjs.compile(js_code)
    logs = ctx.call("updateDebris")
    return logs

def get_all_points():
	with open('temp.js', 'r') as file:
	    js_code = file.read()
	console_logs = execute_js_and_capture_logs(js_code)
	data = []
	for i,log in enumerate(console_logs):
		try:
			dat = {"id": i, "name": log['name'], 'lat': log['lat'], 'lng': log['lng'], 'alt': log['alt'], 'color': log['color']}
		except:
			continue
		data.append(dat)
	return data

def optimize(data, distance_bound=1000, max_satellites_can_carry=100, starting_point='ISS (ZARYA)'):
	iss = [row for row in data if starting_point == row["name"]][0]
	total_distance = 0
	ids_in_path = []
	curr_path = [iss]
	while(total_distance<=distance_bound):
		distances_of_non_path_points = []
		closest_indices_of_non_path_points = []
		points = [row for row in data if row["id"] not in ids_in_path]
		points = [p for p in points if p['color']=='white']
		for point in points:
			d = [((point["lat"]-p["lat"])**2+(point["lng"]-p["lng"])**2+(point["alt"]-p["alt"])**2) for p in curr_path]
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
		if len(curr_path)>max_satellites_can_carry+1:
			break
	return curr_path, total_distance, len(curr_path)-1

import numpy as np

def add_intermediate_nodes(points, max_distance=1.0):
    interpolated_points = [points[0]]
    
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

def orbital_speed_at_altitude(altitude):
    R = R_earth + altitude
    v = math.sqrt(G * M / R)
    return v

def main_midder():
	with open("parameters.json", "r") as f:
		parameters = json.load(f) #404.347
	data = get_all_points()
	curr_path, d, n = optimize(data, distance_bound=parameters['max_dist'], max_satellites_can_carry=parameters['weight_constraint'], starting_point=parameters['starting_point'])
	output = {"time_taken": d/400, "num_debris_picked": n, "salvage_value": 44*n, "reduction_in_collision_rate": round((0.091 - 0.091*(27000-n)/27000)/0.091, 3)*100, "total_distance_navigated": d}
	with open("output.json", "w") as f:
		json.dump(output, f)
	proper_path = add_intermediate_nodes([[c['lat'], c['lng'], c['alt']] for c in curr_path], 0.5)
	path = [[str(p[0]), str(p[1]), str(p[2]), 'green'] for p in proper_path]
	return path, parameters['starting_point']

if __name__ == '__main__':
	paths, starting_point = main_midder()
	# print(paths)
	with open("latest.json", "r") as f:
		data = json.load(f)
	for i, item in enumerate(data['l']):
		if item[0] in ['ISS (ZARYA)', 'CSS (TIANHE)', 'AURORASAT']:
			item[3] = 'purple'
			item[4] = "1.5"
		if item[0] == starting_point:
			item[3] = 'yellow'
			item[4] = '3.5'
		data['l'][i] = item

	data['l'].extend(paths)
	with open("latest.json", "w") as f:
		json.dump(data, f)
