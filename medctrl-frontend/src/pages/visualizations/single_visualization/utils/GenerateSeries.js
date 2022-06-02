// internal imports
import GenerateBarSeries from '../data_interfaces/BarInterface'
import GenerateLineSeries from '../data_interfaces/LineInterface'
import GeneratePieSeries from '../data_interfaces/PieInterface'
import GenerateHistogramSeries from '../data_interfaces/HistogramInterface'

// Returns series data depending on the chart type,
// as each chart type expects data in a certain way.
// For example, a pie chart only expect one variable,
// whereas a bar chart expect two.
export function generateSeries(settings) {
  switch (settings.chartType) {
    case 'bar':
      return GenerateBarSeries(settings)

    case 'line':
      return GenerateLineSeries(settings)

    case 'pie':
      return GeneratePieSeries(settings)

    case 'histogram':
      return GenerateHistogramSeries(settings)

    default:
      throw Error('visualization settings incorrect settings')
  }
}
