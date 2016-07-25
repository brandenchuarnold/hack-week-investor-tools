 // assumes 30 year fixed mortgage with 20% down at the current prevailing rate (pulled from pogo)
	 function getMonthlyMortgage(price) {
	 	var monthly_rate = parseFloat(neighborhood_dict['mortgage_rate']) / (12.0 * 100.0);
	 	var monthly_mortgage = .8 * price * ((monthly_rate * Math.pow((1 + monthly_rate), 30 * 12)) / (Math.pow((1 + monthly_rate), 30 * 12) - 1));
	 	return monthly_mortgage;
	 };


	// check whether a given property satisifes the user's filter metrics
	function filter(property) {
		if ($('#price').val() != '' && !$('#price').prop('disabled')) {
			var max_price = Number($('#price').val().replace(/[^0-9\.]+/g,""));
			if (max_price < property.price) {
				return false;
			}
		}

		if ($('#cap_rate').val() != '' && !$('#cap_rate').prop('disabled')) {
			var min_cap_rate = parseFloat($('#cap_rate').val()) / 100.0;
			var property_cap_rate = (property.restimate * 12 - property.yearly_taxes) / property.price;
			if (min_cap_rate > property_cap_rate) {
				return false;
			}
		}

		if ($('#cash_flow').val() != '' && !$('#cash_flow').prop('disabled')) {

			var monthly_mortgage = getMonthlyMortgage(property.price);
			var min_yearly_cash_flow = Number($('#cash_flow').val().replace(/[^0-9\.]+/g,""));
			var property_cash_flow = (property.restimate * 12) - property.yearly_taxes - (monthly_mortgage * 12);
			
			if (min_yearly_cash_flow > property_cash_flow) {
				return false;
			} 

		}

		if ($('#cash_on_cash').val() != '' && !$('#cash_on_cash').prop('disabled')) {
			var min_cash_on_cash = parseFloat($('#cash_on_cash').val()) / 100.0;
			var monthly_mortgage = getMonthlyMortgage(property.price);

			var property_cash_on_cash = (property.restimate * 12 - property.yearly_taxes - monthly_mortgage * 12) / (property.price * .2);
			if (min_cash_on_cash > property_cash_on_cash) {
				return false;
			}
		}


		return true;
	};
	// delete all markers on the map each time a new neighborhood is selected
	function deleteMarkers() {
		for (var i = 0; i < markers.length; i++) {
			var marker = markers[i];
			marker.setMap(null);
		};
		markers = [];
	};

	// add the appropriate properties to the map each time a new neighborhood is selected
	function neighborhoodClickHandler(id) {
		deleteMarkers();

		var properties = neighborhood_dict[id].properties;

		var count = 0.0;
		var total_lat = 0.0;
		var total_long = 0.0;

		for (var i = 0; i < properties.length; i++) {
			var property = properties[i];
			if (filter(property)) {
				count++;

				var latitude = parseFloat(property.latitude);
				total_lat += latitude;
				var longitude = parseFloat(property.longitude);
				total_long += longitude;

				addMarker(property);
			}
		};
		// recenter the map
		if (count > 0) {

			var avg_lat = total_lat / count;
			var avg_long = total_long / count;

			var latlng = new google.maps.LatLng(avg_lat, avg_long);

			map.setCenter(latlng);

		}
	};

	function formatToDollars(dollars) {
		return '$' + dollars.toFixed(2).replace(/(\d)(?=(\d{3})+\.)/g, '$1,');
	}

	// add a marker to the map
	function addMarker(property) {
		var latitude = parseFloat(property.latitude)
		var longitude = parseFloat(property.longitude)

		var latlng = new google.maps.LatLng(latitude, longitude);

		var marker = new google.maps.Marker({
			position: latlng,
			title: name,
			map: map
		});

		marker.addListener('click', function() {
			var monthly_mortgage = getMonthlyMortgage(property.price);

			content_string = '<div>Price: ' + formatToDollars(property.price) + '<br>';
			content_string += 'Rent: ' + formatToDollars(property.restimate) + '<br>';

			var cash_flow = parseInt(property.restimate * 12) - parseInt(property.yearly_taxes) - parseInt(monthly_mortgage * 12);
			content_string += 'Yearly Cash Flow: ' + formatToDollars(cash_flow);
			content_string += '<br><a href="http://www.zillow.com/homes/' + property.zpid + '_zpid/">Zillow Home Detail Page</a>';
			
			infoWindow.close();

			infoWindow.setContent(content_string);

			infoWindow.open(map, marker);
		});

		markers.push(marker);
	}