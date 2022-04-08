// external import

// exports the visualization with the given id to an svg file
export default function HandleSVGExport(id, ApexCharts) {
  let inst = ApexCharts.getChartByID(String(id))
  inst.exports.triggerDownload(
    inst.exports.svgUrl(),
    'Graph ' +
    id +
    ' - ' +
    document.getElementById('graphName' + id).value,
    '.svg'
  )
}