// internal imports
import generateBarSeries from '../data_interfaces/generateBarSeries'
import generateLineSeries from '../data_interfaces/generateLineSeries'
import generatePieSeries from '../data_interfaces/generatePieSeries'
import generateHistogramSeries from '../data_interfaces/generateHistogramSeries'

// Returns series data depending on the chart type,
// as each chart type expects data in a certain way.
// For example, a pie chart only expect one variable,
// whereas a bar chart expect two.
export default function generateSeries(settings) {
  switch (settings.chartType) {
    case 'bar':
      return generateBarSeries(settings)

    case 'line':
      return generateLineSeries(settings)

    case 'pie':
      return generatePieSeries(settings)

    case 'histogram':
      return generateHistogramSeries(settings)

    default:
      throw Error('visualization settings incorrect settings')
  }
}
