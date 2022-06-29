# Code expansion guide

## General
We have tried to make the dashboard as dynamic as possible by making it depend on the backend, meaning we do not have many hardcoded components. Therefore, for tasks like adding a new variable, we refer to the backend guide. If a new variable is added on the backend, then the frontend instantly supports this new variable.

If you want to write unit tests that use new variables, the only things you need to do is replace the `structServer` json file, which is located in the `src\json` folder, with the new structure data retrieved from the respective endpoint of the backend. This file essentially translates the backend key to a frontend version and includes some information like the data type. The same must be done for the `allServerData` json file, which is located in the same directory, but then should be replaced with the updated medicines data retrieved from the respective endpoint again of the backend. All files in this directory are used to mock the backend server which allows to unit test certain components that normally need these data from the server.

## Text
Text on e.g. the information and home page can easily be changed as well. They are all located in their respective page files, e.g. `HomePage` in `src\pages\home`. The text in the header is located in the `src\core\header` directory in the `Header` file. Analogously, the text in the footer is located in the `src\core\footer` directory in the `Footer` file.

## Visualizations
There are a variety of visualization types, each having its own options or properties in their display. To keep the visualizations modular and therefore extensible, a visualization is built of 3 individual components: visualization_type, data_interface and form. These are all located in the `src\pages\visualizations\single_visualization` directory. We will discuss each of them more in-depth.

### visualization_types
The `visualization_types` directory contains a separate file for each chart. This file holds a function-based component which initializes the settings of the chart and renders the chart. To add a new chart, a new file must be created in this directory. The structure of such a file is as follows:

```jsx
import React from 'react'
import Chart from 'react-apexcharts'

// Replace "SomeChart" with the name of your chart component, e.g. "BarChart"
function SomeChart(props) {
  let settings = {
    options: {
      // Some chart specific options here
    }
    // Add the series to the settings
    // The series is passed as a property to the component
    series: props.series,
  }

  return (
    // Replace "charttype" with the type of the chart, e.g. "bar"
    <div className="med-vis-chart">
      <Chart
        options={settings.options}
        series={settings.series}
        type="charttype"
        height={700}
      />
    </div>
  )
}
```

The series, stored in the settings variable, is the data that will be displayed in the chart. This is constructed with the data_interface corresponding to the specific chart. More on that later. For information on which specific options are available for each chart type, visit [the documentation of ApexCharts](https://apexcharts.com/docs).

### data_interfaces
We can not blindly pass the medicines data retrieved from the API to display the data in the chart. Some sort of processing of this data must be done beforehand. This is where the data_interface comes into play.

The `data_interfaces` directory contains a separate file for each chart type. This file holds a JavaScript function that calculates the series for the specific chart. The parameter `settings` passed to this function must contain the settings specified by the user in the form and the complete medicines data.

The directory furthermore contains the directories `shared_one_dimension` and `shared_two_dimensions`. These directories contain files again with functions that help calculating the series. The functions of `shared_one_dimension` are used by any chart with only one dimension (e.g. pie and histogram), while the functions of `shared_two_dimensions` are used by any chart with two dimensions (e.g. bar and line).

The `shared_one_dimension` directory only contains the file `pollChosenVariable`. This file holds a function with the same name. Based on the passed data, the chosen x-axis (the variable chosen to display) and the chosen categories (values of the variable), it calculates the frequency for each chosen category in the data (e.g. Decision Year 1995 has a frequency of 3). The function returns an array with a dictionary `dict` that maps categories to frequencies and another dictionary `euNumbers` that maps categories to the eu numbers that contributed to the frequency. The `dict` dictionary is essentially the calculated series. The `euNumbers` dictionary is additionally returned to identify the data points again. If a user clicks on a specific area of the chart, we can filter the data on these numbers and display this in a separate table. An example of the content those dictionaries:

```jsx
// Variable: Decision Year
// Chosen categories: 1995

// Maps categories to frequencies
dict = {
  1995: 3
}

// Maps categories to their eu numbers
// So the data with eu numbers 1, 2 and 3 have Decision Year 1995
euNumbers = {
  1995: [1, 2, 3]
}
```

The `shared_two_dimensions` directory contains multiple files. To calculate the series, first the `pollChosenVariable` function is used. It is very similar to the one in the `shared_one_dimension`, however, a chosen y-axis  and the chosen categories on the y-axis must be passed this time as well. It calculates the frequency again of the chosen categories on the x-axis, but it also makes a distinction between the chosen categories on the y-axis now. An example of those dictionaries:

```jsx
// X-axis: Decision Year
// Y-axis: Rapporteur
// Chosen categories x-axis: 1995
// Chosen categories y-axis: United Kingdom and France

dict = {
  1995: {
    "United Kingdom": 2,
    "France": 1
  }
}

euNumbers = {
  1995: {
    "United Kingdom": [1, 3],
    "France": [2]
  }
}
```

However, this format is not the expected format of the library yet. It expects a dictionary that maps each category chosen on the y-axis to an array of frequencies, with each frequency element corresponding to a chosen category on the x-axis. This will be translated by the `createSelectedSeries` function into a format like this:

```jsx
// X-axis: Decision Year
// Y-axis: Rapporteur
// Chosen categories x-axis: 2004, 2005 and 2006
// Chosen categories y-axis: Belgium and Ireland

series = {
  "Belgium": [1, 3, 3],
  "Ireland": [2, 2, 2]
}

euSeries = {
  "Belgium": [[270], [299, 301, 302], [325, 330, 333]],
  "Denmark": [[284, 286], [306, 307], [354, 361]]
}
```

The `toSeriesFormat` function will then finalize the format by putting the `series` and `euSeries` together in one output value, which can then be used to display the data in the chart.

To add support for a new chart, a new file must be created in the `data_interfaces` directory. Depending on the dimension of the chart, you should use the corresponding helper functions described above. The expected format of the series for a chart can be found again at [the documentation of ApexCharts](https://apexcharts.com/docs).

On top of that, a case to the switch statement in the `generateSeries` function must be added. The file is located in the `single_visualization\utils` directory. This function calls the series function which corresponds with the chart type. Add the following code to the switch:

```jsx
// Replace "charttype" with the type of the chart, e.g. "bar"
case 'charttype':
  // Replace "generateChartSeries" with your new function that calculates the series, e.g. "generateBarSeries"
  return generateChartSeries(settings)
```

### forms
The `forms` directory contains the file `VisualizationForm` which is a function-based component that renders the main form of the visualizations page. The directory also contains the directories `types` and `shared`. The `shared` directory contains the `CategoryOptions` file. This file holds a function-based component rendering the category list, where categories can be selected based on the selected variable. This component is currently used in the forms of all the chart types. The `types` directory contains a separate file for each chart type. This file contains a function-based component that renders all the options on the form, e.g. "stacked" and "switch axes" for a bar chart, the dropdowns for the variables and the category options.

To add support for a new chart, a new file must be created in the `types` directory with similar content to the content of the other files. Based on what options this new chart has, you can build the modifiers in this new file. The options of a chart can be found again at [the documentation of ApexCharts](https://apexcharts.com/docs). When you have created such a new file, you should also add a new case to the switch statement in the `renderChartOptions` function in the `VisualizationForm` file:

```jsx
// Replace "charttype" with the name of the new chart type, e.g. "bar"
case 'charttype':
  return (
    // Replace "ChartForm" with the name of your form component, e.g. "BarForm"
    <ChartForm
      uniqueCategories={props.uniqueCategories}
      onChange={handleChange}
      chartSpecificOptions={settings.chartSpecificOptions}
    />
  )
```

To make the new chart visible to the "Visualization type" dropdown, you should add an option to the select element in the return statement of the same file:

```html
<!-- Replace "charttype" with the same name you just provided to the case in the switch statement, e.g. "bar" -->
<option value="charttype">Your new chart type</option>
```

### Add render
If you performed all the previous steps correctly, you should now be able to add the chart to the renderer. To do this, go back to the `single_visualization` directory. This contains the `SingleVisualization` file which holds a function-based component that renders the chosen visualization type and the export and remove buttons. Import the chart file you added in the `visualization_types` folder before and add a new case to the switch statement in the `renderChart` function:

```jsx
// Replace "charttype" with the name of the new chart type, e.g. "bar"
case 'charttype':
  return (
    // Replace "SomeChart" with the name of your chart component, e.g. "BarChart"
    <SomeChart
      legend={legendOn}
      labels={labelsOn}
      id={id}
      series={series}
      categories={categories}
      options={options}
      onDataClick={onDataClick}
    />
  )
```

You may also want to add an extra case to the `renderTitlePlaceHolder` function in the `SingleVisualization` file to customize the title placeholder.
The dashboard should now have support for your new visualization type.

## Pages
Adding more pages to the dashboard is also possible. First, you should create a new directory in the `src\pages` directory with the name of your new page, e.g. `data`. In your new directory, a JavaScript file should be created with the appropriate name, e.g. `DataPage`. You can also create CSS file with the same name if you want to apply styling. The JavaScript file will hold a function-based component that renders your new page. It has the following structure:

```jsx
import React from 'react'

// Import CSS for styling
import './YourPage.css'

function YourPage() {
  // Some variables and/or functions here
  return (
    // The HTML code of your new page (with CSS references)
  )
}

export default YourPage
```

Note that all pages in the dashboard are constructed this way. So making changes to the content of existing pages should be straightforward.

Then navigate to the `src\core` directory. This directory contains the `Routing` file holding a function-based component that provides the dashboard with routing information. To add your new page to the routing, add the following line between the `Routes` element in the return statement of the function:

```jsx
// Replace "/PATH" with your desired path
// Replace "YourPage" with the name of the page component
<Route path="/PATH" element={<YourPage />} />
```

If you now enter your path in the url of the application, your new page should appear. However, the navigation bar does not show this new page yet. Navigate to the `src\core\navigation` directory. This directory contains the file `Navigation` which renders the navigation bar and its components. To add your new page to the navigation bar, add the following component between the other similar components in the return statement:

```jsx
// Replace "NAME OF YOUR PAGE" with the name of your new page, e.g. "Data"
// Replace "CLASSNAME OF ICON" with the classname of a icon that suits your page; see boxicons.com
// Replace "/PATH" with your earlier specified path

<NavLink
  name="NAME OF YOUR PAGE"
  image="CLASSNAME OF ICON"
  dest="/PATH"
  parent={this}
/>
```

Now the dashboard fully supports this new page.

## Contexts
The application uses contexts to provide components with data. Data is regularly passed as properties in a component, but in some cases, the same data is used in multiple (non-related) components which makes it inconvenient to pass them constantly as properties to each other.

To add a context, first navigate to the `src\shared\contexts` directory. This directory contains all the separate contexts of the application. Create a new file in this directory (which also ends with Context). The structure of this file is as follows:

```jsx
import React from 'react'

// Replace "YourContext" with the name of your context, e.g. "DataContext"
const YourContext = React.createContext()

// Replace "useYour" with something that corresponds to the name, e.g. "useData"
export function useYour() {
  // Replace "YourContext" with the name of your context specified in the constant
  return useContext(YourContext)
}

// Replace "YourProvider" with the name of your context, e.g. "DataProvider"
export function YourProvider({ children }) {
  // Some variables and/or functions here
  return (
    // Replace "YourContext" with the name of your context specified in the constant
    // Replace "InsertDataHere" with the variable that contains the data you want to pass
    <YourContext.Provider value={InsertDataHere}>
      {children}
    </YourContext.Provider>
  )
}
```

What remains is adding this individual provider to the chain of providers. Navigate to the `src\shared` directory. This directory contains a `Provider` file which represents the chain of providers. You can add your provider somewhere between those other providers. It does not matter where you put it in general, but if you need data from one of other providers in your context, then you should put your provider as a child of this provider.

Now you can get this data anywhere in the application if you call the following statement:

```jsx
// Replace "useYour" with the same name of the function of your context specified earlier
const data = useYour()
```
