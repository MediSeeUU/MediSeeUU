  export function PollChosenVariable(x_axis, y_axis, categories_y, data) {
		let dict = {};
		let uniqueCategories = [];

		data.forEach((element) => {
			if (uniqueCategories.includes(element[x_axis])) {
				if (categories_y.includes(element[y_axis])) {
					if (dict[element[x_axis]][element[y_axis]] === undefined) {
						dict[element[x_axis]][element[y_axis]] = 1;
					}
					else {
						dict[element[x_axis]][element[y_axis]]+= 1;
					}	
				}
			}
			else {				
				if (categories_y.includes(element[y_axis])) {
					dict[element[x_axis]] = {};
					dict[element[x_axis]][element[y_axis]] = 1;
					uniqueCategories = [...uniqueCategories, element[x_axis]];
				}							
			}
		})

		return [dict, uniqueCategories.sort()];
	}

	export function CreateSelectedSeries(dict, categories_y, categories_x) {
		let series = {}
		let keys = categories_x.sort();

		console.log(keys);
		keys.forEach((k) => {
			for (let category in categories_y) {
				category = categories_y[category];
				if (dict[k] === undefined) {
					if (series[category] === undefined) {
						series[category] = [];
					}
					else {
            series[category].push(0);
					}
					
				}
				else {
          if (series[category] === undefined) {
					  series[category] = [];
					  if ((category in dict[k])) {
						
						  series[category].push(dict[k][category]);
					  }		
					  else {
						  series[category].push(0);
				  	}			
				  }
				  else {
					  if (!(dict[k][category] === undefined)) {
						  series[category].push(dict[k][category]);
					  }			
					  else {
						  series[category].push(0);
					  }		
				  }			
				}
				
			}
		})

		return series;
	}


