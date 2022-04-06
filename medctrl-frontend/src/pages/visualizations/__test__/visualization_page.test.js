import React from 'react'
import ReactDOM from 'react-dom'
import {render, fireEvent, waitFor, screen} from '@testing-library/react'
import VisualizationPage from "../visualization_page"
import CategoryOptions from '../CategoryOptions'
import PieForm from "../form_types/pie_form"
import VisualizationForm from "../visualization_form"
import SingleVisualization from "../single_visualization"


import data from "../data.json"

test("render initial page", () => {
	require("../__Mocks__/observer.js")
	const root = document.createElement('div')
	ReactDOM.render((< VisualizationPage/>), root)
})

test("render initial Category Options", () => {
	const root = document.createElement('div')
	ReactDOM.render((<CategoryOptions categories={[]} />), root)
})

test("render initial Pie form", () => {
	const root = document.createElement('div')
	let categories = {};
	categories["Rapporteur"] = []
	ReactDOM.render((<PieForm uniqueCategories={categories} />), root)
})

test("render initial form", () => {
	const root = document.createElement('div')
	let categories = {};
	categories["Rapporteur"] = []
	ReactDOM.render((<VisualizationForm uniqueCategories={categories} />), root)
})

test("render initial single visualization", () => {
	require("../__Mocks__/observer.js")
	const root = document.createElement('div')
	ReactDOM.render((<SingleVisualization number={1} data={data}/>), root)
})