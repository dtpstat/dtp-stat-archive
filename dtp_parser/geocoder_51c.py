from urllib.request import urlopen
from urllib.parse import urlencode


# временное решение - словарик
true=True
false=False
null=None

class Geocoder_51c:
	url = 'http://138.68.85.118/api/'

	def __init__(self):
		pass

	def test(self, **values):
		data = self.url + 'test'
		if values:
			data += '?' + urlencode(values)
		with urlopen(data) as response:
			return response.read()

	def get_address_point(self, n_p, street, house):
		address = n_p + ' ' + street + ' ' + house
		data = self.url + 'get_address_point' + '?' + urlencode({'address': address})
		with urlopen(data) as response:
			result = eval(response.read())
			result['n_p'] = n_p
			result['street'] = street
			result['house'] = house
			return result

	def get_diapason(self, point_1, point_2):
		values = {'point_1': 'Point({} {})'.format(point_1[1], point_1[0]), 'point_2': 'Point({} {})'.format(point_2[1], point_2[0])}
		data = self.url + 'distance' + '?' + urlencode(values)
		with urlopen(data) as response:
			result = response.read()
			return(result)

	def get_closest_point_on_road(self, n_p, street, house):
		address = n_p + ' ' + street + ' ' + house
		road = n_p + ' ' + street
		data = self.url + 'closest_point_on_road' + '?' + urlencode({'address': address, 'road': road})
		with urlopen(data) as response:
			return response.read()

	def get_correct_point(self, n_p, street, house, dtp_point):
		address = n_p + ' ' + street + ' ' + house
		road = n_p + ' ' + street
		point = 'POINT({} {})'.format(dtp_point[1], dtp_point[0])
		data = self.url + 'correct_point' + '?' + urlencode({'address': address, 'road': road, 'point': point})
		with urlopen(data) as response:
			return response.read()
