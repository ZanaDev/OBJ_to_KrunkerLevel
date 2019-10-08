import json
import sys
import time

def load_config(configuration_file):
	try:
		data = open(configuration_file, "r")
		config = json.loads(data.read())
	except:
		print("woops")
		print(str(configuration_file))
		config = "JSON IMPORT FAILED, FILE MISSING/INACCESSIBLE"

	return config

def calculate_size(bounds):
	min_bounds = bounds[0]
	max_bounds = bounds[1]

	size_x = abs(round(max_bounds[0] - min_bounds[0]))
	size_y = abs(round(max_bounds[1] - min_bounds[1]))
	size_z = abs(round(max_bounds[2] - min_bounds[2]))

	print(str([size_x, size_y, size_z]))
	return [size_x, size_y, size_z]

def calculate_cube_origin(bounds):
	min_bounds = bounds[0]
	max_bounds = bounds[1]

	#Organizational nightmare, I really need to learn how to program :/
	half_height = (max_bounds[1] - min_bounds[1]) / 2

	mid_x = round((min_bounds[0] + max_bounds[0]) / 2)
	mid_y = round(((min_bounds[1] + max_bounds[1]) / 2) - half_height)
	mid_z = round((min_bounds[2] + max_bounds[2]) / 2)

	return [mid_x, mid_y, mid_z]

def calculate_bounds(brush, vertlist):
	x_vals = []
	y_vals = []
	z_vals = []

	#XYZ = Krunker YZX
	for vertlink in brush:
		for vert in vertlink:
			x_vals.append(vertlist[vert - 1][0])
			y_vals.append(vertlist[vert - 1][1])
			z_vals.append(vertlist[vert - 1][2])

	min_bounds = [min(x_vals), min(y_vals), min(z_vals)]
	max_bounds = [max(x_vals), max(y_vals), max(z_vals)]

	bounds = [min_bounds, max_bounds]

	return bounds

def parse_map(mapfile):
	mapdata = open(mapfile, "r")

	vertlist = []
	brush_face_list = []
	brushes = []

	for line in mapdata:
		if line.startswith("v "):
			vert_str = line.split()
			vert = [int(vert_str[1]), int(vert_str[2]), int(vert_str[3])]
			vertlist.append(vert)

		if line.startswith("o "):
			if len(brush_face_list) > 0:
				brushes.append(brush_face_list)

			brush_face_list = []

		if line.startswith("f "):
			brush_face = []

			face_str = line.split()
			vert_one = int(face_str[1].split("/")[0])
			vert_two = int(face_str[2].split("/")[0])
			vert_three = int(face_str[3].split("/")[0])
			vert_four = int(face_str[4].split("/")[0])

			brush_face = [vert_one, vert_two, vert_three, vert_four]
			brush_face_list.append(brush_face)

	#We need special handling for the last cube as there's 
	#no indication it's the end of the file
	#And this is a poor script
	if len(brush_face_list) > 0:
		brushes.append(brush_face_list)

	mapdata.close()
	return [brushes, vertlist]
			
def convert_to_krunkerlevel(mapfile):
	#Retrieves brush vertices per brush
	brush_package = parse_map(mapfile)
	brushes = brush_package[0]
	vertlist = brush_package[1]

	#Get the default map settings
	settings = load_config("KrunkerMapSettingsConfig.json")

	#Generate the list of cube objects for krunker's json format
	cubes = []
	count = 1
	for brush in brushes:
		bounds = calculate_bounds(brush, vertlist)

		cube = {
			#Position/Location
			"p": calculate_cube_origin(bounds),
			#Size
			"s": calculate_size(bounds),
			"t": 4
		}

		print("Cube: #" + str(count))
		print("Position: " + str(cube["p"]))
		print("Size: " + str(cube["s"]))

		count += 1

		cubes.append(cube)

	#Package it all together
	settings["objects"] = cubes

	#write
	f = open("Krunker_Level.txt", 'w', encoding='utf-8')
	f.write(json.dumps(settings, separators=(",", ":"))) 
	f.close()

	#Indicate to Trenchbroom that we're done here
	#Nevermind it's irrelevant as this is no longer an tool-exe step in the compiling process
	return 0

if __name__ == "__main__":
	#Flags
	f_skip_exit_input = False
	#End Flags

	try:
		config = open("CompilerConfig.cfg", "r")

		for line in config:
			if line.startswith("skip_exit_input: "):
				if line.split()[1] == "True":
					f_skip_exit_input = True

		config.close()
	except:
		print("Missing CompilerConfig.cfg file...")

	time_start = time.time()
	convert_to_krunkerlevel(sys.argv[1])
	time_end = time.time() - time_start



	print("")
	print("===============")
	print("The Krunker_Level.txt file should be in the same directory as this script")
	print("Copy and paste the resultant data into the Krunker editor as normal")
	print("")
	print("Conversion completed in", round(time_end, 5), "seconds")
	print("===============")
	print("")
	if not f_skip_exit_input:
		input("Press the ENTER key to close...")



"""
texlist = {
"0_WALL":0,
"1_DIRT":1,
"2_FLOOR":2,
"3_GRID":3,
"4_GREY":4,
#Notice that 5 is missing, read below
"6_ROOF":6,
"7_FLAG":7,
"8_GRASS":8,
"9_CHECK":9,
"10_LINES":10,
"11_BRICK":11,
"12_LINK":12,
}"""