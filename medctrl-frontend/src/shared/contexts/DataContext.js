import React, { useContext, useState, useEffect } from 'react'
import GetUniqueCategories from '../../pages/visualizations/single_visualization/utils/GetUniqueCategories'

export const DataContext = React.createContext()
export const SelectedContext = React.createContext()
export const CheckedContext = React.createContext()
export const CheckedContextUpdate = React.createContext()
export const ColumnSelectionContext = React.createContext()
export const ColumnSelectionContextUpdate = React.createContext()
export const VisualsContext = React.createContext()
export const VisualsUpdateContext = React.createContext()

export function useData() {
  return useContext(DataContext)
}

export function useSelectedData() {
  return useContext(SelectedContext)
}

export function useCheckedState() {
  return useContext(CheckedContext)
}

export function useCheckedStateUpdate() {
  return useContext(CheckedContextUpdate)
}

export function useColumnSelection() {
  return useContext(ColumnSelectionContext)
}

export function useColumnSelectionUpdate() {
  return useContext(ColumnSelectionContextUpdate)
}

export function useVisuals() {
  return useContext(VisualsContext)
}

export function useVisualsUpdate() {
  return useContext(VisualsUpdateContext)
}

export function DataProvider({ children }) {
  // list of all the medicine data points
  const [allData, setAllData] = useState([])

  // retrieve all medicine data points from the backend
  useEffect(() => {
    async function fetchAllData() {
      const response = await fetch(`${process.env.PUBLIC_URL}/api/medicine/`, {
        method: 'GET',
        headers: { 'Content-Type': 'application/json' },
      })
      const dataFromServer = await response.json()

      const clean = (value) => {
        return !value ? 'NA' : value
      }

      const cleanedData = []
      for (var i = 0; i < dataFromServer.length; ++i) {
        const dataPoint = dataFromServer[i]
        if (dataPoint.eunumber) {
          cleanedData.push(
            maakmooi(dataPoint)
            
            
          
          )
        }
      }
      setAllData(cleanedData)
    }
    fetchAllData()
  }, [setAllData])

  function maakmooi(dataPoint){
    const nullReplaceText = "NA"
    const clean = (value) => {
      return !value ? 'NA' : value
    }
    const bool01tostring = (bool01value) =>{
      switch(bool01value)
      {
          case null:
          return nullReplaceText
          case '':
          case "":
          case "unknown":
          case "NA":
          return nullReplaceText
          case 0:
          return "No"
          case 1:
          return "Yes"
          default:
            if(/^[0-9]+$/.test(bool01value))
            {return parseInt(bool01value)}
            else
            { return bool01value}
         

      }
     
    }
    // Y-M-D ->  M/D/Y 
    const reformatDate = (date) =>{
      if(date === null || date==='NA')
      {return 'NA'}
      else
      {let splitteddate = date.split('-')
      return splitteddate[1]+'/'+splitteddate[2]+'/'+splitteddate[0]}
      
      
    }
  // used ?? to filter out NULL values; https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Nullish_coalescing_operator
    
    var formattedDatapoint = {
      ApplicationNo: bool01tostring(dataPoint.emanumber),
      EUNumber: 'EMA-' + clean(dataPoint.eunumber),  //DELETE
      EUNoShort: dataPoint.eunumber ?? nullReplaceText,
      BrandName: bool01tostring( dataPoint.brandname),
      MAH: bool01tostring(dataPoint.mah),
      ActiveSubstance: dataPoint.activesubstance ?? nullReplaceText, //
      DecisionDate:reformatDate(bool01tostring(dataPoint.decisiondate)),
      DecisionYear:  bool01tostring(dataPoint.decisiondate).substring(0, 4),
      Period: 'NA', // how calc??
      Rapporteur: bool01tostring(dataPoint.rapporteur),
      CoRapporteur: bool01tostring(dataPoint.corapporteur),
      ATCCodeL2: bool01tostring(dataPoint.atccode),
      ATCCodeL1: 'NA',
      ATCNameL2: 'NA',
      LegalSCope:bool01tostring(dataPoint.legalscope),
      ATMP: bool01tostring(dataPoint.atmp),//clean(dataPoint.atmp)==='NA' ? 'NA' : booltostring(),
      OrphanDesignation: bool01tostring(dataPoint.orphan),
      NASQualified: 'NA',
      CMA: 'NA',
      AEC: 'NA', 
      LegalType: bool01tostring(dataPoint.legalbasis),
      PRIME: bool01tostring(dataPoint.prime),
      NAS: 'NA',
      AcceleratedGranted: bool01tostring(dataPoint.acceleratedgranted), //
      AcceleratedExecuted:bool01tostring(dataPoint.acceleratedmaintained), //
      ActiveTimeElapsed: dataPoint.authorisationactivetime ?? nullReplaceText,
      ClockStopElapsed: dataPoint.authorisationstoppedtime ?? nullReplaceText,
      TotalTimeElapsed: dataPoint.authorisationtotaltime ?? nullReplaceText,
    }
    return formattedDatapoint
  }


  //list of checked datapoints
  const [checkedState, setCheckedState] = useState(
    Object.assign({}, ...allData.map((entry) => ({ [entry.EUNumber]: true })))
  )

  // update the checked datapoints state when the allData state is changed
  useEffect(() => {
    setCheckedState(
      Object.assign({}, ...allData.map((entry) => ({ [entry.EUNumber]: true })))
    )
  }, [allData])

  //selected datalist
  const selectedData = allData.filter((item, index) => {
    return checkedState[item.EUNumber]
  })

  //the column selection state with the default columns on key names
  const [columnSelection, setColumnSelection] = useState([
    'EUNoShort',
    'BrandName',
    'MAH',
    'DecisionDate',
    'ATCNameL2',
  ])

  // visualisation context to save the visualisations when navigating the page
  const [visuals, setVisuals] = useState([])

  // update the visualisation context state when the allData state is changed
  useEffect(() => {
    let uniqueCategories = GetUniqueCategories(allData)
    setVisuals([
      {
        id: 1,
        chartType: 'bar',
        chartSpecificOptions: {
          xAxis: 'DecisionYear',
          yAxis: 'Rapporteur',
          categoriesSelectedY: uniqueCategories['Rapporteur'],
          categoriesSelectedX: uniqueCategories['DecisionYear'],
        },
        legendOn: false,
        labelsOn: false,
        data: [],
        series: [],
        uniqueCategories: [],
        key: '',
      },
    ])
  }, [allData])

  return (
    <DataContext.Provider value={allData}>
      <SelectedContext.Provider value={selectedData}>
        <CheckedContext.Provider value={checkedState}>
          <CheckedContextUpdate.Provider value={setCheckedState}>
            <ColumnSelectionContext.Provider value={columnSelection}>
              <ColumnSelectionContextUpdate.Provider value={setColumnSelection}>
                <VisualsContext.Provider value={visuals}>
                  <VisualsUpdateContext.Provider value={setVisuals}>
                    {children}
                  </VisualsUpdateContext.Provider>
                </VisualsContext.Provider>
              </ColumnSelectionContextUpdate.Provider>
            </ColumnSelectionContext.Provider>
          </CheckedContextUpdate.Provider>
        </CheckedContext.Provider>
      </SelectedContext.Provider>
    </DataContext.Provider>
  )
}
