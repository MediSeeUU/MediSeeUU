// exports the visualization with the given id to an svg file
export default function HandleSVGExport(id, ApexCharts) {
  // uses the functions ApexCharts itself uses for export to .svg
  const chart = ApexCharts.getChartByID(String(id))
  const ctx = chart.ctx
  ctx.exports.exportToSVG(ctx)
}
