import {
  cleanup,
  render,
  fireEvent,
  waitFor,
  screen,
  getByRole,
  getByText,
} from '@testing-library/react'
import GetUniqueCategories from '../../single_visualization/utils/GetUniqueCategories'
import VisualizationForm from '../../single_visualization/forms/VisualizationForm'

import data from '../../../../testJson/data.json'

let uniqueCategories
beforeAll(() => {
	uniqueCategories = GetUniqueCategories(data)
})

test('initial render', () => {
  const onChange = jest.fn()
	render(
		<VisualizationForm 
		  uniqueCategories={uniqueCategories}
			onchange={onChange}
		/>
	)
})

test('change to line chart type', () => {
  const onChange = jest.fn()
	render(
		<VisualizationForm 
		  uniqueCategories={uniqueCategories}
			onchange={onChange}
		/>
	)
	let target = screen.getByRole('combobox', 
	  { name: /visualization type/i })

	fireEvent.change(
		target,
		{ 
			target: 
			{ 
				value: 'line',
		    name: 'chart_type'
		  }
	  }
	)
})

test('change to pie chart type', () => {
  const onChange = jest.fn()
	render(
		<VisualizationForm 
		  uniqueCategories={uniqueCategories}
			onchange={onChange}
		/>
	)
	let target = screen.getByRole('combobox', 
	  { name: /visualization type/i })

	fireEvent.change(
		target,
		{ 
			target: 
			{ 
				value: 'pie',
		    name: 'chart_type'
		  }
	  }
	)	
})

test('change to bar chart', () => {
  const onChange = jest.fn()
	render(
		<VisualizationForm 
		  uniqueCategories={uniqueCategories}
			onchange={onChange}
		/>
	)
	let target = screen.getByRole('combobox', 
	  { name: /visualization type/i })

	fireEvent.change(
		target,
		{ 
			target: 
			{ 
				value: 'bar',
		    name: 'chart_type'
		  }
	  }
	)	
})

test('trigger defaults of resetChartSpecifics and renderChartOptions', () => {
	const onChange = jest.fn()
	render(
		<VisualizationForm 
		  uniqueCategories={uniqueCategories}
			onchange={onChange}
		/>
	)
	let target = screen.getByRole('combobox', 
	  { name: /visualization type/i })

	fireEvent.change(
		target,
		{ 
			target: 
			{ 
				value: 'pi',
		    name: 'chart_type'
		  }
	  }
	)	
})

test('do a chart specific change', () => {
	const onChange = jest.fn()
	render(
		<VisualizationForm 
		  uniqueCategories={uniqueCategories}
			onchange={onChange}
		/>
	)
	let target = screen.getByRole('combobox', 
	  { name: /x-axis/i })

	fireEvent.change(
		target,
		{ 
			target: 
			{ 
				value: 'Rapporteur',
		    name: 'xAxis'
		  }
	  }
	)	
})

test('make a submission', () => {
	const onChange = jest.fn()
	render(
		<VisualizationForm 
		  uniqueCategories={uniqueCategories}
			onchange={onChange}
		/>
	)
	let target = screen.getByRole('button', 
	  { name: /update/i })
		
	expect(() => fireEvent.click(
		target
	)).toThrow()	
})