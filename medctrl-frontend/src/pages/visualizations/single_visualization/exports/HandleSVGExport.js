// exports the visualization with the given id to an svg file
export default function HandleSVGExport(id, title, ApexCharts) {
  // uses the functions ApexCharts itself uses for export to .svg
  // try catch was needed for passing tests...
  try {
    let inst = ApexCharts.getChartByID(String(id))
    inst.exports.triggerDownload(
      inst.exports.svgUrl(),
      'Graph ' + id + ' - ' + title,
      '.svg'
    )
  } catch (err) {
    console.log('an error occurred when trying to export to svg: {' + err + '}')
  }
}
