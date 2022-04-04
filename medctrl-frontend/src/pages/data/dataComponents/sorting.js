import { firstBy } from 'thenby' //used for subcase sorting
import { useState } from 'react'
import { v4 as uuidv4 } from 'uuid' //used to generate unique component key identifiers
import voca from 'voca' //used for string manipulation necessry for proper string comparising for sorting functionality

//"every time when you update state(call the stateupdatingfunction of the hook), the component rerenders " https://www.youtube.com/watch?v=O6P86uwfdR0

//function requires all Data, given as Array of objects, each object containing key:value; e.g. [ {"id":1, "clr": "red" } , {"id":2, "clr" : "blue"} ]
//function requires sortingParameters, given as array of strings: [ nameofFirstAttributeToSortOn, descendingOrAscending, nameofSecondAttributeToSortOn, ascendingOrDescending,..]

//sortingparameters is array containing sorting objects : [ {selected, order},  {selected, order}, ...]
export function sortData(data, sortingparameters) {
  let initialComparisonFunction =
    convertSortingAttributeNameToComparisonFunction(
      sortingparameters[0].selected
    )
  let initialOrder = convertSortingAttributeNameToComparisonFunction(
    sortingparameters[0].order
  )
  let dezefunc = firstBy(initialComparisonFunction, initialOrder) //(function (v1, v2) {return v1["ApplicationNo"].toString().length - v2["ApplicationNo"].toString().length} , initialOrder)
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
  return function compareAlphabetical(object1, object2) {
    if (typeof object1[attr] == 'number') {
      return object1[attr] - object2[attr]
    }
    return convertStringToAlphaNumerical(object1[attr]).localeCompare(
      convertStringToAlphaNumerical(object2[attr])
    )
  }
}
function convertStringToAlphaNumerical(word) {
  var lowercaselatinizedWord = voca.latinise(word.toString().toLowerCase())
  var AlphaNumericOnlyLatinizedWord = lowercaselatinizedWord.replace(
    /[^a-zA-Z0-9]+/g,
    ''
  )
  return AlphaNumericOnlyLatinizedWord
}

//function to sort one single array containing all possible values for one attribute,
//only sorts on the one attribute specified, delivers sorted array in ascending order.
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
            convertStringToAlphaNumerical(
              jsonObject1['ActiveSubstance']
            ).localeCompare(
              convertStringToAlphaNumerical(jsonObject2['ActiveSubstance'])
            )
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
    //sortingFunctionToUse = (value1, value2)=> value1.toString().localeCompare(value2.toString());
  }

  return sortingFunctionToUse
}
