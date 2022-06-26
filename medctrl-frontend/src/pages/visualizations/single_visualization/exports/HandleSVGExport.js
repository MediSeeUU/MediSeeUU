// This program has been developed by students from the bachelor Computer Science at
// Utrecht University within the Software Project course.
// © Copyright Utrecht University (Department of Information and Computing Sciences)

// exports the visualization with the given id to an svg file
export default function HandleSVGExport(id, ApexCharts) {
  // uses the functions ApexCharts itself uses for export to .svg
  const chart = ApexCharts.getChartByID(String(id))
  const ctx = chart.ctx
  ctx.exports.exportToSVG(ctx)
}
