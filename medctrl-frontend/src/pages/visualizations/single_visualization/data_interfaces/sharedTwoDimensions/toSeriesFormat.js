// turning a dict into the data format accepted by ApexChart
// the entry key becomes the name, the entry value becomes the data
export default function toSeriesFormat(dict, euSeries) {
  let series = []
  for (let key in dict) {
    series.push({ name: key, data: dict[key], euNumbers: euSeries[key] })
  }
  return series
}
