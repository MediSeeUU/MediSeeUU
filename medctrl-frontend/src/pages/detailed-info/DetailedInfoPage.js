import './DetailedInfo.css'

// the data in this json file includes not only general medicine information,
// but also a few (bu not all) procedures which are related to medicine used
// for the demo dataset
import demoData from './detailed-info-data.json'

import Container from './InfoComponents/Container'
import DetailGroup from './InfoComponents/DetailGroup'
import Detail from './InfoComponents/Detail'
import Procedure from './InfoComponents/Procedure'
import CustomLink from './InfoComponents/CustomLink'

//
import { DataContext, DataProvider, useData } from '../../shared/contexts/DataContext'
import {useParams, useSearchParams}  from "react-router-dom";

// the function acts as a placeholder to pass the right through to the actual
// component, when the data flow is correctly linked, the component will
// no longer be required and can be removed
function DetailedInfoPage(medIDnumbertje) {

  const {medID} = useParams()

  /* const [searchParams, setSearchParams] = useSearchParams({});
  setSearchParams({ medID: medIDnumbertje  }); */

 var cooledata;
 /* var alledataAUB =  DataContext.value//useData
 for(var i in alledataAUB)
 {
    if(i["ApplicationNo"] === medIDnumbertje) 
    {cooledata = i}   

 } */
 return <DataProvider>
   <DataContext.Consumer>
     {(context) => (
      
       <InfoPage data ={context} medicijnnummer = {medID}></InfoPage>
     )}
   </DataContext.Consumer>
 </DataProvider>
 
  //return <InfoPage data = {cooledata}/>
  //return <InfoPage data={demoData} />
}

export default DetailedInfoPage

// function based component, which represents the entire detailed information page
// an json object is passed via the data tag. this is the data which is displayed on
// the details page.
function InfoPage(props) {
  // extract the medicine data from the props

  //AAAA
  var medicijnnummer = props.medicijnnummer
  var alldata = props.data
  var goededataobjectje = alldata.find((element) => element["EUNoShort"] === medicijnnummer)
  alldata.forEach(element => {
    var euNOelem = element["EUNoShort"].toString()
    var euNOklik = medicijnnummer
    if (euNOelem === euNOklik)//(String.toString( element["EUNoShort"]) === String.toString( medicijnnummer))
    {goededataobjectje = element}
  });


  let medicineData = {info:goededataobjectje, procedures:[]}//goededataobjectje//props.data
  

  // for each procedure present in the medicine data object, an procedure component
  // is created and added to an array for temporary storage
  let allProcedures = []
  for (var i = 0; i < medicineData.procedures.length; i++) {
    allProcedures.push(<Procedure proc={medicineData.procedures[i]} />)
  }

  // returns the component which discribes the entire detailed information page
  // the page consists of three containers, each holds a specific category of
  // information pertaining to the current medicine. this first holds general
  // information, teh next procedure related information, and the last holds some
  // links to external website which could be usefull
  return (
    <div>
      <Container>
        <h1 className="title">
          {medicineData.info.BrandName} Medicine Details
        </h1>
        <hr className="separator" />

        <div class="flex-columns">
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

          <DetailGroup title="Reporting Countries">
            <Detail
              name="Primary Reporter"
              value={medicineData.info.Rapporteur}
            />
            <Detail
              name="Secondary Reporter"
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
            <Detail name="NAS" value={medicineData.info.NAS} />
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
      </Container>

      <Container>
        <h1 className="title">Procedure Details</h1>
        <hr className="separator" />
        {allProcedures}
      </Container>

      <Container>
        <h1 className="title">Additional Resources</h1>
        <hr className="separator" />

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
      </Container>
    </div>
  )
}
