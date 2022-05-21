import './DetailedInfo.css'

import DetailGroup from './InfoComponents/DetailGroup'
import Detail from './InfoComponents/Detail'
import Procedure from './InfoComponents/Procedure'
import CustomLink from './InfoComponents/CustomLink'
import TimeLine from './InfoComponents/TimeLine'

import { useData, useStructure } from '../../shared/contexts/DataContext'
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

  return <InfoPage medData={medData} procData={procData} />
}

// function based component, which represents the entire detailed information page
// it display the given medicine and procedure data
export function InfoPage({ medData, procData }) {

  const variableCategories = useStructure()

  // if no medicine data is provided, no meaning full can be displayed
  if (!medData) {
    return (
      <h1 className="med-info-unknown-medID">Unknown Medicine ID Number</h1>
    )
  }

  // a filter which determines which prodcures to show, and which to omit from
  // the detailed info page
  let displayProcTypes = [
    'Centralised - Authorisation',
    'Centralised - Transfer Marketing Authorisation Holder',
    'Centralised - Annual reassessment',
    'Centralised - Annual renewal',
  ]

  // if there is procedure data present, two containers should be added to the page
  // with only the relevant procedure entries (based on the display proc types above)
  // one container should display the procedures in text form, and the other should
  // visually display them as a timeline. if no procedure data is present, both
  // containers should not be displayed
  let procedureContrainer = null
  let timeLineContainer = null

  if (procData !== null) {
    let procedures = procData.filter((proc) =>
      displayProcTypes.includes(proc.proceduretype)
    )

    procedureContrainer = (
      <div className="med-content-container">
        <h1>Procedure Details</h1>
        <hr className="med-top-separator" />
        {procedures.map((proc) => {
          return <Procedure proc={proc} key={v4()} />
        })}
      </div>
    )

    timeLineContainer = (
      <div className="med-content-container">
        <h1>Medicine Timeline</h1>
        <hr className="med-top-separator" />
        <TimeLine procs={procedures} />
      </div>
    )
  }
  
  const detailGroups = []

  for (let category in variableCategories) {
    const details = []

    for (let varIndex in variableCategories[category]) {
      const variable = variableCategories[category][varIndex]
      details.push(
        <Detail 
          name={variable["data-value"]} 
          value={medData[variable["data-front-key"]]} 
          key={v4()} />
      )
    }

    detailGroups.push(
      <DetailGroup title={category} key={v4()}>
        {details}
      </DetailGroup>
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
          {detailGroups}
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
