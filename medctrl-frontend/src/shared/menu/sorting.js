import { firstBy } from 'thenby' 
import voca from 'voca' 

//function requires all Data, given as Array of objects, each object containing key:value; e.g. [ {"id":1, "clr": "red" } , {"id":2, "clr" : "blue"} ]
//function requires sortingParameters, which is the sorting state object passed from the filtermenu; it is an array containing an object for each active sorting filter.
//one sorting filter object consists of 2 properties, { selected, order}. With selected being a string containing the name of the attribute to sort on.
// order contains a string of either "asc" or "desc", for ascending or descending order
export function sortData(data, sortingparameters) {
  
  for(var sortparIndex=0; sortparIndex<sortingparameters.length; sortparIndex++)
  {
    if(sortingparameters[sortparIndex].selected === '')
    {sortingparameters.splice(sortparIndex,1)}
  }
  if(sortingparameters.length === 0 )
  {return data}


  let initialComparisonFunction =
    convertSortingAttributeNameToComparisonFunction(
      sortingparameters[0].selected
    )
  let initialOrder = convertSortingAttributeNameToComparisonFunction(
    sortingparameters[0].order
  )
  let dezefunc = firstBy(initialComparisonFunction, initialOrder)
  for (let i = 1; i < sortingparameters.length; i++) {
    dezefunc = dezefunc.thenBy(
      convertSortingAttributeNameToComparisonFunction(
        sortingparameters[i].selected
      ),
      convertSortingAttributeNameToComparisonFunction(
        sortingparameters[i].order
      )
    )
  }

  data.sort(dezefunc)

  return data
}

function createComparisonFunction(attr) {
  console.log(attr)
  if(attr === undefined || attr === ''){
      return function baseComparison(jsonObject1, jsonObject2){
          jsonObject1[0].toString().localeCompare(jsonObject2[0].toString())
      }
    }
  else{
    return function alphanumericalcomparison(jsonobject1, jsonobject2){
      console.log(attr + "____"+ jsonobject1[attr] + "____"+ jsonobject1.toString()) // logt getallen id voor ApplicationNo
      return convertStringToAlphaNumerical(jsonobject1[attr]).localeCompare(
        convertStringToAlphaNumerical(jsonobject2[attr]))
    }
  }
  //return convertStringToAlphaNumerical(object1[attr]).localeCompare(
  //  convertStringToAlphaNumerical(object2[attr])
  //)

  /* return function compareAlphabetical(object1, object2) {
      if(attr === undefined || attr === ''){
        return function baseComparison(jsonObject1, jsonObject2){
            jsonObject1[0].toString().localeCompare(jsonObject2[0].toString())
        }
      }
    if (typeof object1[attr] === "number") {
      return object1[attr] - object2[attr]
    }
    return convertStringToAlphaNumerical(object1[attr]).localeCompare(
      convertStringToAlphaNumerical(object2[attr])
    )
  } */
}
function convertStringToAlphaNumerical(word) {
  console.log(word)
  if (typeof word === 'Number')
  {word = Number.toString(word)
   console.log("!!!!!!"+ word)
  }
  var lowercaselatinizedWord = voca.latinise(word.toString().toLowerCase())
  var AlphaNumericOnlyLatinizedWord = lowercaselatinizedWord.replace(
    /[^a-zA-Z0-9]+/g,
    ''
  )
  return AlphaNumericOnlyLatinizedWord
}
//-----------------------------------------------------------------------------------------------------------------------
//function takes one attributeName as a string, and returns the corresponding comparison function for json objects.
//use this returned comparison function as an argument to .sort function of an array containing jsonObjects.
export function convertSortingAttributeNameToComparisonFunction(
  attributeNameAsString
) {
  var sortingFunctionToUse
  switch (attributeNameAsString) {
    case 'asc':
      sortingFunctionToUse = 1
      break
    case 'desc':
      sortingFunctionToUse = -1
      break
    case 'DecisionDate':
      //format:  month/day/year -> day/month/year
      try {
        function CompareDateFunction(jsonObject1, jsonObject2) {
          var splittedDate1 = jsonObject1['DecisionDate'].split('/')
          var rightDatum1 =
            splittedDate1[2] + splittedDate1[0] + splittedDate1[1]
          var splittedDate2 = jsonObject2['DecisionDate'].split('/')
          var rightDatum2 =
            splittedDate2[2] + splittedDate2[0] + splittedDate2[1]
          return rightDatum1.localeCompare(rightDatum2)
        }

        sortingFunctionToUse = CompareDateFunction
      } catch (errorID) {
        console.Error(errorID)
        sortingFunctionToUse = (value1, value2) =>
          value1['DecisionDate']
            .toString()
            .localeCompare(value2['DecisionDate'].toString())
      }

      break
    case 'MAH':
      try {
        function MAHcomparison(jsonObject1, jsonObject2) {
          return convertStringToAlphaNumerical(
            jsonObject1['MAH']
          ).localeCompare(convertStringToAlphaNumerical(jsonObject2['MAH']))
        }
        sortingFunctionToUse = MAHcomparison
      } catch (errorID) {
        console.Error(errorID)
        sortingFunctionToUse = (value1, value2) =>
          value1['MAH'].toString().localeCompare(value2['MAH'].toString())
      }
      break
    case 'ActiveSubstance':
      try {
        function ActSubComparison(jsonObject1, jsonObject2) {
          return convertStringToAlphaNumerical(
              jsonObject1['ActiveSubstance']
            ).localeCompare(
              convertStringToAlphaNumerical(jsonObject2['ActiveSubstance'])
            )
          
        }
        sortingFunctionToUse = ActSubComparison
      } catch (errorID) {
        console.Error(errorID)
        sortingFunctionToUse = (value1, value2) =>
          value1['ActiveSubstance']
            .toString()
            .localeCompare(value2['ActiveSubstance'].toString())
      }
      break
    default:
      sortingFunctionToUse = createComparisonFunction(attributeNameAsString)
    
  }

  return sortingFunctionToUse
}

//----------------------------------------------------------------------------------------------------------------------------------
//Function takes the name of an attribute as a string, returns the appropriate sorting function
//use this function to sort an array containing only values of the provided AttributeName type.
//use like: arrayName.sort(comparisonFunctionAsReturnedByThisFunction)
export function getSortingFunctionFromAttributeName(
    attributeNameAsString
  ) {
    var sortingFunctionToUse
    switch (attributeNameAsString) {
      case 'DecisionDate':
        //format:  month/day/year -> day/month/year
        try {
          function CompareDateFunction(value1, value2) {
            var splittedDate1 = value1.split('/')
            var rightDatum1 =
              splittedDate1[2] + splittedDate1[0] + splittedDate1[1]
            var splittedDate2 = value2.split('/')
            var rightDatum2 =
              splittedDate2[2] + splittedDate2[0] + splittedDate2[1]
            return rightDatum1.localeCompare(rightDatum2)
          }
  
          sortingFunctionToUse = CompareDateFunction
        } catch (errorID) {
          console.Error(errorID)
          sortingFunctionToUse = (value1, value2) =>
            value1
              .toString()
              .localeCompare(value2.toString())
        }
  
        break
      case 'MAH':
        try {
          function MAHcomparison(value1, value2) {
            return convertStringToAlphaNumerical(
              value1
            ).localeCompare(convertStringToAlphaNumerical(value2))
          }
          sortingFunctionToUse = MAHcomparison
        } catch (errorID) {
          console.Error(errorID)
          sortingFunctionToUse = (value1, value2) =>
            value1.toString().localeCompare(value2.toString())
        }
        break
      case 'ActiveSubstance':
        try {
          function ActSubComparison(value1, value2) {
            return convertStringToAlphaNumerical(
                value1
              ).localeCompare(
                convertStringToAlphaNumerical(value2)
              )
            
          }
          sortingFunctionToUse = ActSubComparison
        } catch (errorID) {
          console.Error(errorID)
          sortingFunctionToUse = (value1, value2) =>
            value1
              .toString()
              .localeCompare(value2.toString())
        }
        break
      default:
        sortingFunctionToUse = createComparisonFunction2(attributeNameAsString)
        
      
    }
  
    return sortingFunctionToUse
  }
//function takes an attribute name and returns the correpsonding comparison function,
//base clause for when no other match is found in getSortingFunctionFromAttributeName(attributeName)
function createComparisonFunction2(attr) {
  
    if(attr === undefined || attr === ''){
        return function baseComparison(value1, value2){
            return value1.toString().localeCompare(value2.toString())
        }
    }
    if (typeof value1 == 'number') {
    return function basenumbercompare(value1, value2){ return (value1 - value2)}
    }
    return function alphanumericalcompare (value1, value2) {
      return convertStringToAlphaNumerical(value1).localeCompare(convertStringToAlphaNumerical(value2))
    }
    
  
/* return function compareAlphabeticalA(value1, value2) {
    if(attr === undefined || attr === ''){
        return function baseComparison(value1, value2){
            value1.toString().localeCompare(value2.toString())
        }
    }
    if (typeof value1 == 'number') {
    return function basenumbercompare(value1, value2){ return (value1 - value2)}
    }
    return convertStringToAlphaNumerical(value1).localeCompare(
    convertStringToAlphaNumerical(value2)
    )
} */
}