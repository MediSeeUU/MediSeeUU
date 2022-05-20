
export default function cleanFetchedData(fetchedData) {
  const cleanedData = []
  for (var i = 0; i < fetchedData.length; ++i) {
    const dataPoint = fetchedData[i]
    // the datapoint should only be included if it is a valid datapoint,
    // this is the case when it has a non null eunumber (Short EU Number)
    if (dataPoint.eunumber) {
      cleanedData.push(
        cleanFetchedDataPoint(dataPoint)
      )
    }
  }
  return cleanedData
}

function cleanFetchedDataPoint(fetchedDataPoint) {
  const dataPoint = fetchedDataPoint
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