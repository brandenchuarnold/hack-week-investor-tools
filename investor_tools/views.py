from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.base import View
from django.shortcuts import render
import json
import requests
import math

def alias_sproc_output(sproc_output):
	output = {}
	output['price'] = sproc_output['selling_price_dollar_cnt']
	output['yearly_taxes'] = sproc_output['tax_paid_amt']
	output['restimate'] = sproc_output['zestimate_dollar_cnt']
	output['zpid'] = sproc_output['property_id']
	output['bedrooms'] = sproc_output['bedrooms']
	output['bathrooms'] = sproc_output['bathrooms']
	output['latitude'] = sproc_output['latitude'] * math.pow(10, -6)
	output['longitude'] = sproc_output['longitude'] * math.pow(10, -6)

	return output

def get_fake_data():
	downtown_properties = [{'address' : 'fake address', 'latitude' : 47.6062, 'longitude' : -122.3321, 'price' : 150000, 'yearly_taxes' : 3000, 'restimate' : 1400, 'zpid' : 48725241}]
	south_lake_properties = [{'address' : 'fake address 2', 'latitude' : 47.6222, 'longitude' : -122.3371,'price' : 200000, 'yearly_taxes' : 4000, 'restimate' : 2200, 'zpid' : 92570232}, 
	{'address' : 'fake address 3', 'latitude' : 47.6252, 'longitude' : -122.3311, 'price' : 100000, 'yearly_taxes' : 1500, 'restimate' : 900, 'zpid' : 88877172}]
	neighborhood_list = [
		{'name' : 'South Lake Union', 'id' : 'south_lake_union', 'properties' : south_lake_properties, 'neighborhood_attributes' : {}}, 
		{'name' : 'Capitol Hill', 'id' : 'capitol_hill', 'properties' : [], 'neighborhood_attributes' : {}}, 
		{'name' : 'Beacon Hill', 'id' : 'beacon_hill','properties' : [], 'neighborhood_attributes' : {}},
		{'name' : 'University District', 'id' : 'university_district','properties' : [], 'neighborhood_attributes' : {}},
		{'name' : 'Queen Anne', 'id' : 'queen_anne','properties' : [], 'neighborhood_attributes' : {}},
		{'name' : 'Downtown', 'id' : 'downtown','properties' : downtown_properties, 'neighborhood_attributes' : {}},
		{'name' : 'West Seattle', 'id' : 'west_seattle','properties' : [], 'neighborhood_attributes' : {}},
		{'name' : 'Magnolia', 'id' : 'magnolia','properties' : [], 'neighborhood_attributes' : {}}
	]

	neighborhood_dict = {}
	for neighborhood in neighborhood_list:
		neighborhood_dict[neighborhood['id']] = neighborhood

	return neighborhood_dict

def get_real_data(neighborhoods):
	neighborhood_dict = {}
	for _id, name in neighborhoods.items():
		neighborhood_attributes = json.loads(requests.get('http://localhost:5000/neighborhood_data/' + str(_id)).content)

		for key, val in neighborhood_attributes['neighborhood_data'].items():
			if key.startswith('percent'):
				neighborhood_attributes['neighborhood_data'][key] = int(float(val) * 100)

		neighborhood = {'name' : name, 'id' : name.lower().replace(' ', '_'), 'neighborhood_attributes' : neighborhood_attributes['neighborhood_data']}

		property_list = json.loads(requests.get('http://localhost:5000/property_region/' + str(_id)).content)
		formatted_properties = []

		for _property in property_list['property_regions']:
			formatted_property = alias_sproc_output(_property)
			formatted_properties.append(formatted_property)
		
		neighborhood.update({'properties' : formatted_properties})
		neighborhood_dict[name.lower().replace(' ', '_')] = neighborhood

	return neighborhood_dict
		


def get_mortgage_rate():
	try:
		mortgageQuery = 'https://mortgageapi.develop.zillow.net/getCurrentRates?partnerId=RD-QNNRMHN'
		response = requests.get(mortgageQuery).content
		mortgage_rate = json.loads(response)['rates']['default'].get('rate')

		return mortgage_rate

	except KeyError:
		return '4.5'

def home(request, *args, **kwargs):
	neighborhoods = {250206 : 'Capitol Hill', 250017 : 'Ballard', 250692 : 'Freemont', 252248 : 'Wallingford', 
	250780 : 'Green Lake', 250788 : 'Greenwood', 272001 : 'University District', 271808 : 'Belltown', 251709 : 'Ravenna', 250050 : 'Beacon Hill'}

	neighborhood_dict = get_real_data(neighborhoods)
	mortgage_rate = get_mortgage_rate()
	neighborhood_dict['mortgage_rate'] = mortgage_rate


	context = {'neighborhood_dict' : neighborhood_dict, 'neighborhood_json' : json.dumps(neighborhood_dict)}

	return render(request, "index2.html", context)

