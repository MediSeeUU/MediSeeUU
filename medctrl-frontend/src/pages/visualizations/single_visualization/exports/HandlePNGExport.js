// This program has been developed by students from the bachelor Computer Science at
// Utrecht University within the Software Project course.
// © Copyright Utrecht University (Department of Information and Computing Sciences)
// external imports
import { changeDpiDataUrl } from 'changedpi'

// Event handler for exporting the visualization to png.
// Does not export the actual data.
export default function HandlePNGExport(id, title, ApexCharts) {
  // Get the visualization in the base64 format,
  // we scale it for a better resolution.
  ApexCharts.exec(String(id), 'dataURI', { scale: 3.5 })
    .then(({ imgURI }) => {
      // changes the dpi of the visualization to 300
      const dataURI300 = changeDpiDataUrl(imgURI, 300)

      let inst = ApexCharts.getChartByID(String(id))
      inst.exports.triggerDownload(
        dataURI300,
        'Graph ' + id + ' - ' + title,
        '.png'
      )
    })
    .catch((err) =>
      console.log('an error occurred when trying to export to png')
    )
}
