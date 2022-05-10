import './DetailedInfo.css'

import DetailGroup from './InfoComponents/DetailGroup'
import Detail from './InfoComponents/Detail'
import Procedure from './InfoComponents/Procedure'
import CustomLink from './InfoComponents/CustomLink'
import TimeLine from './InfoComponents/TimeLine'

import { useData } from '../../shared/contexts/DataContext'
import { useParams } from 'react-router-dom'
import { useEffect, useState } from 'react'
import { v4 } from "uuid";

// function based component, which represents the entire detailed information page
// a medicine id number is from the URL and the specific information related to 
// that medince is displayed.
function DetailedInfoPage() {
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
      const response = await fetch(`${process.env.PUBLIC_URL}/api/procedure/`+medID+'/', {
        method: 'GET',
        headers: { 'Content-Type': 'application/json' },
      })
      const data = await response.json()
      setProcData(data)
    }
    fetchProcedureData(medID)
  }, [setProcData, medID])

  // if the medIDnumber does not correspond to any medicine in the datacontext,
  // a static error page is displayed
  if (medData === undefined) {
    return (
      <h1 className="detailedinfopage-unknown-medID">
        Unknown Medicine ID Number
      </h1>
    )
  }

  // for each procedure present in the medicine data object, an procedure component
  // is created and added to an array for temporary storage
  let allProcedures = []
  if (procData !== null) {
    allProcedures = procData.map((proc) => {
      return <Procedure proc={proc} key={v4()}/>
    })
  }

  // put all of the procedures from the allProcedures array into a content containers,
  // together with a meaningful title. The procuedures are also combined into a visual
  // timeline component, this component is placed in its own content container if
  // there are no procedures to display, the both containers should not be displayed
  let procedureContrainer = (
    <div className="med-content-container">
      <h1 className="title">Procedure Details</h1>
      <hr className="med-top-separator" />
      {allProcedures}
    </div>
  )

  let timeLineContainer = (
    <div className="med-content-container">
      <h1 className="title">Medicine Timeline</h1>
      <hr className="med-top-separator" />
      <TimeLine procs={procData} />
    </div>
  )

  if (allProcedures.length === 0) {
    procedureContrainer = null
    timeLineContainer = null
  }

  // returns the component which discribes the entire detailed information page
  // the page consists of three containers, each holds a specific category of
  // information pertaining to the current medicine. this first holds general
  // information, the next procedure related information, and the last holds some
  // links to external website which could be usefull
  return (
    <div>
      <div className="med-content-container">
        <h1 className="title">{medData.BrandName} Medicine Details</h1>
        <hr className="med-top-separator" />

        <div className="flex-columns">
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

          <DetailGroup title="Reporting Countries">
            <Detail name="Primary Reporter" value={medData.Rapporteur} />
            <Detail name="Secondary Reporter" value={medData.CoRapporteur} />
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
            <Detail name="NAS" value={medData.NAS} />
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
        <h1 className="title">Additional Resources</h1>
        <hr className="med-top-separator" />

        <CustomLink
          className="external-link"
          name="EMA Website"
          dest="https://www.ema.europa.eu/en"
        />
        <CustomLink
          className="external-link"
          name="EC Website"
          dest="https://ec.europa.eu/info/index_en"
        />
        <CustomLink
          className="external-link"
          name="MEB Website"
          dest="https://english.cbg-meb.nl/"
        />
        <CustomLink
          className="external-link"
          name="MAH Website"
          dest="https://www.ema.europa.eu/en/glossary/marketing-authorisation-holder"
        />
      </div>
    </div>
  )
}

export default DetailedInfoPage