import './DetailedInfo.css'

import DetailGroup from './InfoComponents/DetailGroup'
import Detail from './InfoComponents/Detail'
import Procedure from './InfoComponents/Procedure'
import CustomLink from './InfoComponents/CustomLink'
import TimeLine from './InfoComponents/TimeLine'
import ProcSelectModal from './InfoComponents/ProcSelectModal'

import { useData } from '../../shared/contexts/DataContext'
import { useParams } from 'react-router-dom'
import { useEffect, useState } from 'react'
import { v4 } from 'uuid'

// function based component, which represents the top level detailed info page
// component, it collects and fetches all the correct data and then passes this data
// to the info page component and returns that component
export default function DetailedInfoPage() {
  const { medID } = useParams()
  const [procData, setProcData] = useState(null)

  // all information of all medicines is retrieved and the correct entry
  // corresponding to the desired medicine is extracted from the array
  const alldata = useData()
  let medData = alldata.find(
    (element) => element.EUNoShort.toString() === medID.toString()
  )

  // all of the procedure data related to the desired medicine is asynchronously
  // retrieved from the server. the result is stored in a state
  useEffect(() => {
    async function fetchProcedureData(medID) {
      const response = await fetch(
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

  // retrieve a date from the backend which indicates when the last update
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

// function based component, which represents the entire detailed information page
// it display the given medicine and procedure data
export function InfoPage({ medData, procData, lastUpdatedDate }) {
  // a filter which determines which prodcures to show, and which to omit from
  // the detailed info page
  const [procFilter, setProcFilter] = useState([
    'Centralised - Authorisation',
    'Centralised - Transfer Marketing Authorisation Holder',
    'Centralised - Annual reassessment',
    'Centralised - Annual renewal',
  ])

  // if no medicine data is provided, no meaning full can be displayed
  if (!medData) {
    return (
      <h1 className="med-info-unknown-medID">Unknown Medicine ID Number</h1>
    )
  }

  // if there is procedure data present, two containers should be added to the page
  // with only the relevant procedure entries (based on the display proc types above)
  // one container should display the procedures in text form, and the other should
  // visually display them as a timeline. if no procedure data is present, both
  // containers should not be displayed
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

  // returns the component which discribes the entire detailed information page
  // the page consists of three containers, each holds a specific category of
  // information pertaining to the current medicine. this first holds general
  // information, the next procedure related information, and the last holds some
  // links to external website which could be usefull
  return (
    <div>
      <div className="med-content-container">
        <h1>{medData.BrandName} Medicine Details</h1>
        <hr className="med-top-separator" />

        <div className="med-flex-columns">
          <DetailGroup title="General Information">
            <Detail name="Brand Name" value={medData.BrandName} />
            <Detail name="Marketing Authorisation Holder" value={medData.MAH} />
            <Detail name="Active Substance" value={medData.ActiveSubstance} />
            <Detail name="Decision Date" value={medData.DecisionDate} />
          </DetailGroup>

          <DetailGroup title="Identifying Information">
            <Detail name="Application Number" value={medData.ApplicationNo} />
            <Detail name="EU Number" value={medData.EUNumber} />
            <Detail name="Short EU Number" value={medData.EUNoShort} />
          </DetailGroup>

          <DetailGroup title="(Co-)Rapporteur">
            <Detail name="Rapporteur" value={medData.Rapporteur} />
            <Detail name="Co-Rapporteur" value={medData.CoRapporteur} />
          </DetailGroup>

          <DetailGroup title="Medicine Designations">
            <Detail name="ATMP" value={medData.ATMP} />
            <Detail
              name="Orphan Designation"
              value={medData.OrphanDesignation}
            />

            <Detail name="NAS Qualified" value={medData.NASQualified} />
            <Detail name="CMA" value={medData.CMA} />
            <Detail name="AEC" value={medData.CMA} />
            <Detail name="PRIME" value={medData.PRIME} />
          </DetailGroup>

          <DetailGroup title="ATC Code Information">
            <Detail name="ATC Code Level 1" value={medData.ATCCodeL1} />
            <Detail name="ATC Code Level 2" value={medData.ATCCodeL2} />
            <Detail name="ATC Name Level 2" value={medData.ATCNameL2} />
          </DetailGroup>

          <DetailGroup title="Legal Information">
            <Detail name="Legal Scope" value={medData.LegalSCope} />
            <Detail name="Legal Type" value={medData.LegalType} />
          </DetailGroup>

          <DetailGroup title="Authorisation Timing">
            <Detail
              name="Accelerated Granted"
              value={medData.AcceleratedGranted}
            />
            <Detail
              name="Accelerated Executed"
              value={medData.AcceleratedExecuted}
            />
            <Detail
              name="Active Time Elapsed (days)"
              value={medData.ActiveTimeElapsed}
            />
            <Detail
              name="Clock Stop Elapsed (days)"
              value={medData.ClockStopElapsed}
            />
            <Detail
              name="Total Time Elapsed (days)"
              value={medData.TotalTimeElapsed}
            />
          </DetailGroup>
        </div>
      </div>

      {timeLineContainer}
      {procedureContrainer}

      <div className="med-content-container">
        <h1>Additional Resources</h1>
        <hr className="med-top-separator" />

        <CustomLink
          className="med-info-external-link"
          name="EMA Website"
          dest="https://www.ema.europa.eu/en"
        />
        <CustomLink
          className="med-info-external-link"
          name="EC Website"
          dest="https://ec.europa.eu/info/index_en"
        />
        <CustomLink
          className="med-info-external-link"
          name="MEB Website"
          dest="https://english.cbg-meb.nl/"
        />
        <CustomLink
          className="med-info-external-link"
          name="MAH Website"
          dest="https://www.ema.europa.eu/en/glossary/marketing-authorisation-holder"
        />
      </div>
    </div>
  )
}
