// external imports
import { changeDpiDataUrl } from 'changedpi'

// Event handler for exporting the visualization to png.
// Does not export the actual data.
export default function HandlePNGExport(id, title, ApexCharts) {
  // Get the visualization in the base64 format,
  const imgURI = ApexCharts.exec(String(id), 'dataURI', {
    scale: 3.5,
  }) /* .catch(err =>
      console.log('an error occurred when trying to export to png: {' + err + '}')
    ) */
  // changes the dpi of the visualization to 300
  const dataURI300 = changeDpiDataUrl(imgURI, 300)
  const fileName = 'Graph ' + id + ' - ' + title
  const fileType = '.png'

  const downloadLink = document.createElement('a')
  downloadLink.href = dataURI300
  downloadLink.download = fileName + fileType
  document.body.appendChild(downloadLink)
  downloadLink.click()
  document.body.removeChild(downloadLink)
}
