// This program has been developed by students from the bachelor Computer Science at
// Utrecht University within the Software Project course.
// © Copyright Utrecht University (Department of Information and Computing Sciences)

import React, { useState } from 'react'
import MedModal from '../../shared/MedModal'
import '../data/data_select/menu/Menu.css'

// Function based component which renders the filter and sort menu
function DownloadChangelog({ data, fileName, fileType }) {

  const exportData = () => {
    const jsonString = `data:text/json;chatset=utf-8,${encodeURIComponent(
      JSON.stringify(data)
    )}`;
    const link = document.createElement("a");

    link.href = jsonString;
    link.download = fileName + fileType;

    link.click();
  };

  return (
    <>
      <button
        className="med-primary-solid med-info-changelog-button med-data-button"
        onClick={exportData}
      >
        <i className="bx bx-download med-button-image" />
        Download {fileType}
      </button>
    </>
  )
}

export default DownloadChangelog
