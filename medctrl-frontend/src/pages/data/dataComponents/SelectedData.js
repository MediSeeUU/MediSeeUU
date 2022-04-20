import React, { useState } from 'react'
import { useSelectedData } from '../../../shared/contexts/DataContext'
import TableView from './TableView'
import ExportMenu from '../ExportMenu/ExportMenu'
import ContentContainer from '../../../shared/container/ContentContainer'

function SelectedData() {
  //amount of databse hits shown per page
  const [resultsPerPage, setResultsPerPage] = useState(25)

  //current page
  const [loadedPage, setPage] = useState(1)

  const selectedData = useSelectedData()

  //main body of the page
  return (
    <ContentContainer>
      <div>
        <ExportMenu />
        <hr></hr>
      </div>
      {TableView(
        selectedData,
        resultsPerPage,
        loadedPage,
        setPage,
        setResultsPerPage,
        false,
        'No data has been selected, select data points in the table above.'
      )}
    </ContentContainer>
  )
}

export default SelectedData
