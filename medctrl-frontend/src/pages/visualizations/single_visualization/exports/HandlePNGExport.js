// external imports
import { changeDpiDataUrl } from 'changedpi'

// event handler for exporting the visualization to png
export default function HandlePNGExport(id, title, ApexCharts) {
  const fileName = 'Graph ' + id + ' - ' + title
  const fileType = '.png'
  const downloadLink = document.createElement('a')
  // get the visualization in the base64 format
  ApexCharts.exec(String(id), 'dataURI', { scale: 3.5 }).then(({ imgURI }) => {
    // changes the dpi of the visualization to 300
    downloadLink.href = changeDpiDataUrl(imgURI, 300)
    downloadLink.download = fileName + fileType
    document.body.appendChild(downloadLink)
    downloadLink.click()
    document.body.removeChild(downloadLink)
  })
}
