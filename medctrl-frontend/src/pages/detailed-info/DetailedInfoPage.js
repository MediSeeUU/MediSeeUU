// This program has been developed by students from the bachelor Computer Science at
// Utrecht University within the Software Project course.
// © Copyright Utrecht University (Department of Information and Computing Sciences)

import React, { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import { slashDateToStringDate } from '../data/shared/table/format'
import { v4 } from 'uuid'
import { useData } from '../../shared/contexts/DataContext'
import { useStructure } from '../../shared/contexts/StructureContext'
import { fetchWithToken } from '../../shared/api'

import './DetailedInfo.css'
import DetailGroup from './components/DetailGroup'
import Detail from './components/Detail'
import Procedure from './components/Procedure'
import CustomLink from './components/CustomLink'
import TimeLine from './components/TimeLine'
import ProcSelectModal from './components/ProcSelectModal'

// Function based component, which represents the top level detailed info page
// component, it collects and fetches all the correct data and then passes this data
// to the info page component and returns that component
export default function DetailedInfoPage() {
  const { medID } = useParams()
  const [procData, setProcData] = useState(null)

  // All information of all medicines is retrieved and the correct entry
  // corresponding to the desired medicine is extracted from the array
  const alldata = useData()
  let medData = alldata.find(
    (element) => element.EUNoShort.toString() === medID.toString()
  )

  // All of the procedure data related to the desired medicine is asynchronously
  // retrieved from the server. The result is stored in a state.
  useEffect(() => {
    async function fetchProcedureData(medID) {
      const response = await fetchWithToken(
        `${process.env.PUBLIC_URL}/api/procedure/` + medID + '/',
        {
          method: 'GET',
          headers: { 'Content-Type': 'application/json' },
        }
      )
      const data = await response.json()
      setProcData(data)
    }
    fetchProcedureData(medID)
  }, [setProcData, medID])

  // Retrieve a date from the backend which indicates when the last update
  // to the procedures in the database was. i.e. the database, and thus the
  // procedure data on this page is complete up to this date
  const lastUpdatedDate = undefined

  return (
    <InfoPage
      medData={medData}
      procData={procData}
      lastUpdatedDate={lastUpdatedDate}
    />
  )
}

// Function based component, which represents the entire detailed information page
// it display the given medicine and procedure data
export function InfoPage({ medData, procData, lastUpdatedDate }) {
  const variableCategories = useStructure()

  // A filter which determines which prodcures to show, and which to omit from
  // the detailed info page
  const [procFilter, setProcFilter] = useState([
    'Centralised - Authorisation',
    'Centralised - Transfer Marketing Authorisation Holder',
    'Centralised - Annual reassessment',
    'Centralised - Annual renewal',
  ])

  // If no medicine data is provided, no meaning full can be displayed
  if (!medData) {
    return (
      <h1 className="med-info-unknown-medID">Unknown Medicine ID Number</h1>
    )
  }

  // If there is procedure data present, two containers should be added to the page
  // with only the relevant procedure entries (based on the display proc types above)
  // one container should display the procedures in text form, and the other should
  // visually display them as a timeline. If no procedure data is present, both
  // containers should not be displayed.
  let procedureContrainer = null
  let timeLineContainer = null

  if (procData !== null) {
    const removeDuplicates = (arr) => {
      return arr.filter((item, index) => arr.indexOf(item) === index)
    }
    const availableProcTypes = removeDuplicates(
      procData.map((proc) => proc.proceduretype)
    )
    const procSelectModal = (
      <ProcSelectModal
        availableProcTypes={availableProcTypes}
        currentProcFilter={procFilter}
        setProcFilter={setProcFilter}
      />
    )

    const procedures = procData.filter((proc) =>
      procFilter.includes(proc.proceduretype)
    )

    const noProcs = procedures.length === 0
    const noProcMessage = (
      <p className="med-info-no-proc-message">
        There are no procedures to display, make sure that there are procedure
        types selected for display in the menu in the top right corner of the
        container.
      </p>
    )

    procedureContrainer = (
      <div className="med-content-container med-info-container">
        <h1>Procedure Details</h1>
        {procSelectModal}
        <hr className="med-top-separator" />
        {!noProcs
          ? procedures.map((proc) => {
              return <Procedure proc={proc} key={v4()} />
            })
          : noProcMessage}
      </div>
    )

    timeLineContainer = (
      <div className="med-content-container med-info-container">
        <h1>Medicine Timeline</h1>
        {procSelectModal}
        <hr className="med-top-separator" />
        {!noProcs ? (
          <TimeLine procedures={procedures} lastUpdatedDate={lastUpdatedDate} />
        ) : (
          noProcMessage
        )}
      </div>
    )
  }

  const detailGroups = []

  for (let category in variableCategories) {
    const details = []

    for (let varIndex in variableCategories[category]) {
      const variable = variableCategories[category][varIndex]
      if (variable['data-format'] !== 'link') {
        let value = medData[variable['data-front-key']]
        if (variable['data-format'] === 'date') {
          value = slashDateToStringDate(value)
        }

        details.push(
          <Detail name={variable['data-value']} value={value} key={v4()} />
        )
      }
    }

    if (details.length > 0) {
      detailGroups.push(
        <DetailGroup title={category} key={v4()}>
          {details}
        </DetailGroup>
      )
    }
  }

  // Returns the component which discribes the entire detailed information page
  // the page consists of three containers, each holds a specific category of
  // information pertaining to the current medicine. This first holds general
  // information, the next procedure related information, and the last holds some
  // links to external website which could be useful.
  return (
    <div>
      <div className="med-content-container">
        <h1>{medData.BrandName} Medicine Details</h1>
        <hr className="med-top-separator" />

        <div className="med-flex-columns">{detailGroups}</div>
      </div>

      {timeLineContainer}
      {procedureContrainer}

      <div className="med-content-container">
        <h1>Additional Resources</h1>
        <hr className="med-top-separator" />

        <CustomLink
          className="med-info-external-link"
          name={'EMA Website for ' + medData.BrandName}
          dest={medData.EMAurl}
        />
        <CustomLink
          className="med-info-external-link"
          name={'EC Website for ' + medData.BrandName}
          dest={medData.ECurl}
        />
      </div>
    </div>
  )
}
