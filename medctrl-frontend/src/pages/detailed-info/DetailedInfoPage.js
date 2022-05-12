import './DetailedInfo.css'

import DetailGroup from './InfoComponents/DetailGroup'
import Detail from './InfoComponents/Detail'
import Procedure from './InfoComponents/Procedure'
import CustomLink from './InfoComponents/CustomLink'
import { DataContext, DataProvider } from '../../shared/contexts/DataContext'
import { useParams } from 'react-router-dom'

// the function takes the unique medicine ID number (EUshortNumber) and
// passes this ID to the detailedPage component, along with the access
// to the overarching datacontext, where the DetailedInfoPage will request
// the medicine data corresponding to the medID number.
function DetailedInfoPage() {
  const { medID } = useParams()

  return (
    <DataProvider>
      <DataContext.Consumer>
        {(context) => <InfoPage data={context} medIDnumber={medID}></InfoPage>}
      </DataContext.Consumer>
    </DataProvider>
  )
}

export default DetailedInfoPage

// function based component, which represents the entire detailed information page
// the loaded data in datacontext is passed via the data tag. The specific medID no.
// is passed via the me  this is the data which is displayed on
// the details page.
export function InfoPage(props) {
  var medIDnr = props.medIDnumber
  var alldata = props.data

  var medDataObject
  var procedureDataPresentFlag = false

  //depending on the provided JSONdata (not) containing proceduredata,
  //use appropriate function to get the medicine data component

  if (alldata[0].hasOwnProperty('procedures')) {
    medDataObject = alldata.find(
      (element) => element['info'].EUNoShort.toString() === medIDnr.toString()
    )
    procedureDataPresentFlag = true
  } else {
    medDataObject = alldata.find(
      (element) => element['EUNoShort'].toString() === medIDnr.toString()
    )
  }

  //if the medIDnumber does not correspond to any medicine in the datacontext,
  //a static page is displayed
  if (medDataObject === undefined) {
    return (
      <div>
        <h1
          className="detailedinfopage-unknown-medID"
          testid="detailedInfoPageTitle"
        >
          Unknown Medicine ID Number
        </h1>
      </div>
    )
  }

  //place the data corresponding to the specified medIDnumber in the medicine data capsule,
  //procedures currently are not supported, will be implemented after correct database connection
  var medicineData
  if (procedureDataPresentFlag) {
    medicineData = {
      info: medDataObject['info'],
      procedures: medDataObject['procedures'],
    }
  } else {
    medicineData = { info: medDataObject, procedures: [] }
  }

  // for each procedure present in the medicine data object, an procedure component
  // is created and added to an array for temporary storage
  let allProcedures = []
  for (let i = 0; i < medicineData.procedures.length; i++) {
    allProcedures.push(
      <Procedure key={i} proc={medicineData.procedures[i]} id={i} />
    )
  }

  // put all of the procedures from the allProcedures array into a content containers,
  // together with a meaningful title. if there are no procedures to display, the whole
  // container should not be displayed
  let procedureContrainer = (
    <div className="med-content-container">
      <h1 className="title">Procedure Details</h1>
      <hr className="med-top-separator" />
      {allProcedures}
    </div>
  )

  if (allProcedures.length === 0) {
    procedureContrainer = null
  }

  // returns the component which discribes the entire detailed information page
  // the page consists of three containers, each holds a specific category of
  // information pertaining to the current medicine. this first holds general
  // information, the next procedure related information, and the last holds some
  // links to external website which could be usefull
  return (
    <div>
      <div className="med-content-container">
        <h1 className="title">
          {medicineData.info.BrandName} Medicine Details
        </h1>
        <hr className="med-top-separator" />

        <div className="flex-columns">
          <DetailGroup title="General Information">
            <Detail name="Brand Name" value={medicineData.info.BrandName} />
            <Detail
              name="Marketing Authorisation Holder"
              value={medicineData.info.MAH}
            />
            <Detail
              name="Active Substance"
              value={medicineData.info.ActiveSubstance}
            />
            <Detail
              name="Decision Date"
              value={medicineData.info.DecisionDate}
            />
          </DetailGroup>

          <DetailGroup title="Identifying Information">
            <Detail
              name="Application Number"
              value={medicineData.info.ApplicationNo}
            />
            <Detail name="EU Number" value={medicineData.info.EUNumber} />
            <Detail
              name="Short EU Number"
              value={medicineData.info.EUNoShort}
            />
          </DetailGroup>

          <DetailGroup title="(Co-)Rapporteur">
            <Detail name="Rapporteur" value={medicineData.info.Rapporteur} />
            <Detail
              name="Co-Rapporteur"
              value={medicineData.info.CoRapporteur}
            />
          </DetailGroup>

          <DetailGroup title="Medicine Designations">
            <Detail name="ATMP" value={medicineData.info.ATMP} />
            <Detail
              name="Orphan Designation"
              value={medicineData.info.OrphanDesignation}
            />
            <Detail
              name="NAS Qualified"
              value={medicineData.info.NASQualified}
            />
            <Detail name="CMA" value={medicineData.info.CMA} />
            <Detail name="AEC" value={medicineData.info.CMA} />
            <Detail name="PRIME" value={medicineData.info.PRIME} />
          </DetailGroup>

          <DetailGroup title="ATC Code Information">
            <Detail
              name="ATC Code Level 1"
              value={medicineData.info.ATCCodeL1}
            />
            <Detail
              name="ATC Code Level 2"
              value={medicineData.info.ATCCodeL2}
            />
            <Detail
              name="ATC Name Level 2"
              value={medicineData.info.ATCNameL2}
            />
          </DetailGroup>

          <DetailGroup title="Legal Information">
            <Detail name="Legal Scope" value={medicineData.info.LegalSCope} />
            <Detail name="Legal Type" value={medicineData.info.LegalType} />
          </DetailGroup>

          <DetailGroup title="Authorisation Timing">
            <Detail
              name="Accelerated Granted"
              value={medicineData.info.AcceleratedGranted}
            />
            <Detail
              name="Accelerated Executed"
              value={medicineData.info.AcceleratedExecuted}
            />
            <Detail
              name="Active Time Elapsed (days)"
              value={medicineData.info.ActiveTimeElapsed}
            />
            <Detail
              name="Clock Stop Elapsed (days)"
              value={medicineData.info.ClockStopElapsed}
            />
            <Detail
              name="Total Time Elapsed (days)"
              value={medicineData.info.TotalTimeElapsed}
            />
          </DetailGroup>
        </div>
      </div>

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
