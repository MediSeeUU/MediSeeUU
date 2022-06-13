import { firstBy } from 'thenby'
import voca from 'voca'

// Function requires all Data, given as Array of objects, each object containing key:value; e.g. [ {"id":1, "clr": "red" } , {"id":2, "clr" : "blue"} ]
// Function requires sortingParameters, which is the sorting state object passed from the filtermenu; it is an array containing an object for each active sorting filter.
// One sorting filter object consists of 2 properties, { selected, order}. With selected being a string containing the name of the attribute to sort on.
// Order contains a string of either "asc" or "desc", for ascending or descending order
export default function sortData(data, sortingparameters) {
  for (
    var sortparIndex = 0;
    sortparIndex < sortingparameters.length;
    sortparIndex++
  ) {
    if (sortingparameters[sortparIndex].selected === '') {
      sortingparameters.splice(sortparIndex, 1)
    }
  }

  if (sortingparameters.length === 0) {
    return data
  }

  let initialComparisonFunction =
    convertSortingAttributeNameToComparisonFunction(
      sortingparameters[0].selected, sortingparameters[0].order
    )
  let initialOrder = (sortingparameters[0].order==='asc') ? 1:-1
  
  let dezefunc = firstBy(initialComparisonFunction, initialOrder)
  for (let i = 1; i < sortingparameters.length; i++) {
    dezefunc = dezefunc.thenBy(
      convertSortingAttributeNameToComparisonFunction(
        sortingparameters[i].selected, sortingparameters[i].order
      ),
      (sortingparameters[i].order==='asc') ? 1:-1
    )
  }

  data.sort(dezefunc)

  return data
}

function createComparisonFunction(attr, sortingorder) {
  const defValue = 'NA'

  if (attr === undefined || attr === '') {
    return function baseComparison(jsonObject1, jsonObject2) {
      return String.toString(jsonObject1[0]).localeCompare(
        String.toString(jsonObject2[0])
      )
    }
  } else {
    return function alphanumericalcomparison(jsonobject1, jsonobject2) {
      if (
        typeof jsonobject1[attr] === 'number' &&
        typeof jsonobject2[attr] === 'number'
      ) {
        if (jsonobject1[attr] === defValue) {
          if(sortingorder === 'asc')
          {return 1}
          else
          {return -1}
        } else if (jsonobject2[attr] === defValue) {
          if(sortingorder === 'asc')
          {return -1}
          else
          {return 1}
        } else return jsonobject1[attr] - jsonobject2[attr]
      }

      if (jsonobject1[attr] === defValue) {
        if(sortingorder === 'asc')
          {return 1}
        else
          {return -1}
      } else if (jsonobject2[attr] === defValue) {
        if(sortingorder === 'asc')
          {return -1}
        else
          {return 1}
      } else {
        return convertStringToAlphaNumerical(jsonobject1[attr]).localeCompare(
          convertStringToAlphaNumerical(jsonobject2[attr])
        )
      }
    }
  }
}
function convertStringToAlphaNumerical(word) {
  var lowercaselatinizedWord = voca.decapitalize(
    voca.latinise(word.toString().toLowerCase())
  )
  var AlphaNumericOnlyLatinizedWord = lowercaselatinizedWord.replace(
    /[^a-zA-Z0-9]+/g,
    ''
  )
  return AlphaNumericOnlyLatinizedWord
}

// Function takes one attributeName as a string, and returns the corresponding comparison function for json objects.
// Use this returned comparison function as an argument to .sort function of an array containing jsonObjects.
export function convertSortingAttributeNameToComparisonFunction(
  attributeNameAsString, sortingorder
) {
  var sortingFunctionToUse
  const defValue = 'NA'

  switch (attributeNameAsString) {
    case 'DecisionDate':
      //format:  month/day/year -> day/month/year

      function CompareDateFunction(jsonObject1, jsonObject2) {
        if (jsonObject1['DecisionDate'] === defValue) {
          if(sortingorder === 'asc')
          {return 1}
          else
          {return -1}
        } else if (jsonObject2['DecisionDate'] === defValue) {
          if(sortingorder === 'asc')
          {return -1}
          else
          {return 1}
        } else {
          var splittedDate1 = jsonObject1['DecisionDate'].split('/')
          var rightDatum1 = splittedDate1[2] + splittedDate1[0] + splittedDate1[1]
          var splittedDate2 = jsonObject2['DecisionDate'].split('/')
          var rightDatum2 = splittedDate2[2] + splittedDate2[0] + splittedDate2[1]
          return rightDatum1.localeCompare(rightDatum2)
        }
      }

      sortingFunctionToUse = CompareDateFunction

      break
    case 'MAH':
      function MAHcomparison(jsonObject1, jsonObject2) {
        if (jsonObject1['MAH'] === defValue) {
          if(sortingorder === 'asc')
          {return 1}
          else
          {return -1}
        } else if (jsonObject2['MAH'] === defValue) {
          if(sortingorder === 'asc')
          {return -1}
          else
          {return 1}
        } else {
          return convertStringToAlphaNumerical(
            jsonObject1['MAH']
          ).localeCompare(convertStringToAlphaNumerical(jsonObject2['MAH']))
        }
      }
      sortingFunctionToUse = MAHcomparison

      break
    case 'ActiveSubstance':
      function ActSubComparison(jsonObject1, jsonObject2) {
        if (jsonObject1['ActiveSubstance'] === defValue) {
          if(sortingorder === 'asc')
          {return 1}
          else
          {return -1}
        } else if (jsonObject2['ActiveSubstance'] === defValue) {
          if(sortingorder === 'asc')
          {return -1}
          else
          {return 1}
        }
        return convertStringToAlphaNumerical(
          jsonObject1['ActiveSubstance']
        ).localeCompare(
          convertStringToAlphaNumerical(jsonObject2['ActiveSubstance'])
        )
      }
      sortingFunctionToUse = ActSubComparison

      break

    case 'ApplicationNo':
      function numberorNAcompare(jsonobject1, jsonobject2) {
        if (jsonobject1['ApplicationNo'] === defValue) {
          if(sortingorder === 'asc')
          {return 1}
          else
          {return -1}
        } else if (jsonobject2['ApplicationNo'] === defValue) {
          if(sortingorder === 'asc')
          {return -1}
          else
          {return 1}
        } else {
          return jsonobject1['ApplicationNo'] - jsonobject2['ApplicationNo']
        }
      }

      sortingFunctionToUse = numberorNAcompare

      break
    case 'LegalType':
      function legaltypecompare(jsonobject1, jsonobject2) {
        if (jsonobject1['LegalType'] === defValue) {
          if(sortingorder === 'asc')
          {return 1}
          else
          {return -1}
        } else if (jsonobject2['LegalType'] === defValue) {
          
          if(sortingorder === 'asc')
          {return -1}
          else
          {return 1}
        } else {
          var legalnumber1 = jsonobject1['LegalType'].slice(8)
          var legalnumber2 = jsonobject2['LegalType'].slice(8)
          var sortOrder = [
            '4.8a(1)',
            '4.8a(2)',
            '4.8a(3)',
            '8.3',
            '10a',
            '10b',
            '10c',
            '10.1',
            '10.3',
            '10.4',
            defValue,
          ]

          var sortres =
            sortOrder.indexOf(legalnumber1) - sortOrder.indexOf(legalnumber2)
          if (sortres === 0) {
            sortres = 0
          }
          if (sortres < 0) {
            sortres = -1
          }
          if (sortres > 0) {
            sortres = 1
          }
          return sortres
        }
      }
      return legaltypecompare
    default:
      sortingFunctionToUse = createComparisonFunction(attributeNameAsString, sortingorder)
  }

  return sortingFunctionToUse
}
