// This program has been developed by students from the bachelor Computer Science at
// Utrecht University within the Software Project course.
// © Copyright Utrecht University (Department of Information and Computing Sciences)
// turning a dict into the data format accepted by ApexChart
// the entry key becomes the name, the entry value becomes the data
export default function toSeriesFormat(dict, euSeries) {
  let series = []
  for (let key in dict) {
    series.push({ name: key, data: dict[key], euNumbers: euSeries[key] })
  }
  return series
}
