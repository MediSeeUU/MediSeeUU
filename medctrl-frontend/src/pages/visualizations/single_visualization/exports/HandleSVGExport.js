// This program has been developed by students from the bachelor Computer Science at
// Utrecht University within the Software Project course.
// © Copyright Utrecht University (Department of Information and Computing Sciences)
// exports the visualization with the given id to an svg file
export default function HandleSVGExport(id, title, ApexCharts) {
  let inst = ApexCharts.getChartByID(String(id))
  try {
    inst.exports.triggerDownload(
      inst.exports.svgUrl(),
      'Graph ' + id + ' - ' + title,
      '.svg'
    )
  } catch {
    console.log('an error occurred when trying to export to svg')
  }
}
