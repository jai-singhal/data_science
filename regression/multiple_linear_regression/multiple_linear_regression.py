import math
import googlemaps 
import xlrd
import csv


class CalculateDistance:
	def __init__(self, apiKey):
		self.API_KEY = apiKey

	# # Not in use
	# def haversineDistance(self, src, destination):
	# 	# https://en.wikipedia.org/wiki/Haversine_formula
	# 	lat1, lon1 = src
	# 	lat2, lon2 = destination
	# 	radius = 6371
	# 	dlat = math.radians(lat2 - lat1)
	# 	dlon = math.radians(lon2 - lon1)
	# 	result = (math.sin(dlat / 2) * math.sin(dlat / 2) +
	# 	     math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
	# 	     math.sin(dlon / 2) * math.sin(dlon / 2))
	# 	result = 2 * math.atan2(math.sqrt(result), math.sqrt(1 - result))
	# 	distance = radius * result
	# 	return distance


	def googleMapDistance(self, src, destination):
		gmaps = googlemaps.Client(key=self.API_KEY, timeout=3, retry_timeout=5)
		try:
			result = gmaps.distance_matrix(
						[str(src[0]) + " " + str(src[1])], 
						[str(destination[0]) + " " + str(destination[1])])
		except Exception as e:
			print("Something went wrong with making API Call")
			exit(1)

		try:
			distance = result['rows'][0]['elements'][0]["distance"] # in km
			#distance = "{} miles".format(0.621371*distance) 
			duration = result['rows'][0]['elements'][0]["duration"]
			return(distance, duration) 
		except:
			print("Google map api fails: {}, {} not reachable".format(src, destination))
			return False


	def read(self, path):
		workbook = xlrd.open_workbook(path)
		worksheet = workbook.sheet_by_index(0)
		first_row = []
		for col in range(worksheet.ncols):
		    first_row.append(worksheet.cell_value(0,col))
		data = []
		for row in range(1, worksheet.nrows):
		    elment = []
		    for col in range(worksheet.ncols):
		        elment.append(worksheet.cell_value(row, col))
		    data.append(elment)
		return data


	def write(self, data):
		keys = data[0].keys()
		with open('output.csv', 'w', newline='') as output_file:
		    dict_writer = csv.DictWriter(output_file, keys)
		    dict_writer.writeheader()
		    dict_writer.writerows(data)


	def calculateGMapDistance(self, path):
		input_data = self.read(path)
		distances = []
		for d in input_data:
			src = d[1], d[2]  #latitide longitude
			dest = d[3], d[4] #latitide longitude
			response = self.googleMapDistance(src, dest)
			if response: # if successful api response
				distance, duration = response
				distances.append({
					"lane": d[0],
					"distance": distance["text"],
					"duration": duration["text"]
				})
			else: # if failure api response
				distances.append({
					"lane": d[0],
					"distance": "",
					"duration": ""
				})
		self.write(distances)
		print("Successfully calculated Google Map Distances")


def main():
	apiKey = "AIzaSyBWxiVyKaCvJWLziWYuXrdY8s4LRUqFMIw"
	inputFileLoc = "input.xlsx"

	d = CalculateDistance(apiKey)
	d.calculateGMapDistance(inputFileLoc)


if __name__ == '__main__':
	main()
