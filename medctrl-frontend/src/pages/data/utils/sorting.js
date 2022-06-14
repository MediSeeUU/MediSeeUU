import { firstBy } from 'thenby'
import voca from 'voca'

// Sorting function is called for any sorting call in the table. Sorts the data on one or more attributes, in ascending or descending order.
// This sorting function requires data, given as an array of objects, each object containing key:value pairs for the variables;
//          e.g. data = [ {"eunumber":1, "brandname": "GONAL-f" } , {"eunumber":2, "brandname" : "Taxotere"} ]
// Function requires sortingParameters, which is the sorting state object passed from the filtermenu; it is an array containing an object for each active sorting filter;
//          e.g. sortingparameters = [ {"selected":"eunumber", "order":"asc"}, {"selected":"legaltype", "order":"desc"}]
export default function sortData(data, sortingparameters) {
  //remove sorting parameters which have unspecified sorting categories
  for (
    var sortparIndex = 0;
    sortparIndex < sortingparameters.length;
    sortparIndex++
  ) {
    if (sortingparameters[sortparIndex].selected === '') {
      sortingparameters.splice(sortparIndex, 1)
    }
  }
  //if no sorting parameters are given, do not sort
  if (sortingparameters.length === 0) {
    return data
  }

  //determine the primary variable to sort on and its sorting order(asc or desc)
  let initialComparisonFunction =
    convertSortingAttributeNameToComparisonFunction(
      sortingparameters[0].selected,
      sortingparameters[0].order
    )
  let initialOrder = sortingparameters[0].order === 'asc' ? 1 : -1

  //Create a multi-level sorting function; first sort on one variable,
  //then sort equal values on another variable, etc.
  let compositeSortingFunction = firstBy(
    initialComparisonFunction,
    initialOrder
  )
  for (let i = 1; i < sortingparameters.length; i++) {
    compositeSortingFunction = compositeSortingFunction.thenBy(
      convertSortingAttributeNameToComparisonFunction(
        sortingparameters[i].selected,
        sortingparameters[i].order
      ),
      sortingparameters[i].order === 'asc' ? 1 : -1
    )
  }

  //sort the data using the composite sorting function
  data.sort(compositeSortingFunction)

  return data
}

//function which creates a sorting function for general attributes
function createComparisonFunction(attr, sortingorder) {
  const NAvalues = ['NA', 'unknown', 'na', 'null']

  //in case the attribute is unspecified, return a default comparison function
  if (attr === undefined || attr === '') {
    return function baseComparison(jsonObject1, jsonObject2) {
      return String.toString(jsonObject1[0]).localeCompare(
        String.toString(jsonObject2[0])
      )
    }
  }
  //otherwise, create either a numerical or alphanumerical sorting function,
  //depending on wether the variable values contain numbers and/or letters
  else {
    return function alphanumericalcomparison(jsonobject1, jsonobject2) {
      if (
        typeof jsonobject1[attr] === 'number' &&
        typeof jsonobject2[attr] === 'number'
      ) {
        if (NAvalues.includes(jsonobject1[attr])) {
          return sortingorder === 'asc' ? 1 : -1
        } else if (NAvalues.includes(jsonobject2[attr])) {
          return sortingorder === 'asc' ? -1 : 1
        } else return jsonobject1[attr] - jsonobject2[attr]
      }

      if (NAvalues.includes(jsonobject1[attr])) {
        return sortingorder === 'asc' ? 1 : -1
      } else if (NAvalues.includes(jsonobject2[attr])) {
        return sortingorder === 'asc' ? -1 : 1
      } else {
        return convertStringToAlphaNumerical(jsonobject1[attr]).localeCompare(
          convertStringToAlphaNumerical(jsonobject2[attr])
        )
      }
    }
  }
}

//helper function which preprocesses strings before sorting
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

// Some attributes require a special sorting function to sort their values.
// additionally, "asc" or "desc" specified sorting orders need to be converted to "1" and "-1" values to be used in multi level sorting.
// This function takes one sorting attribute as a string, and returns the corresponding comparison function for json objects (or sorting order in numerical form).
// Use this returned comparison function as an argument to a sort function, like the multilevel ThenBy sort.
export function convertSortingAttributeNameToComparisonFunction(
  attributeNameAsString,
  sortingorder
) {
  var sortingFunctionToUse
  const NAvalues = ['NA', 'unknown', 'na', 'null']

  switch (attributeNameAsString) {
    case 'DecisionDate':
      //reformat date from  month/day/year  to  day/month/year
      function CompareDateFunction(jsonObject1, jsonObject2) {
        if (NAvalues.includes(jsonObject1['DecisionDate'])) {
          return sortingorder === 'asc' ? 1 : -1
        } else if (NAvalues.includes(jsonObject2['DecisionDate'])) {
          return sortingorder === 'asc' ? -1 : 1
        } else {
          var splittedDate1 = jsonObject1['DecisionDate'].split('/')
          var rightDatum1 =
            splittedDate1[2] + splittedDate1[0] + splittedDate1[1]
          var splittedDate2 = jsonObject2['DecisionDate'].split('/')
          var rightDatum2 =
            splittedDate2[2] + splittedDate2[0] + splittedDate2[1]
          return rightDatum1.localeCompare(rightDatum2)
        }
      }
      sortingFunctionToUse = CompareDateFunction
      break
    case 'MAH':
      function MAHcomparison(jsonObject1, jsonObject2) {
        if (NAvalues.includes(jsonObject1['MAH'])) {
          return sortingorder === 'asc' ? 1 : -1
        } else if (NAvalues.includes(jsonObject2['MAH'])) {
          return sortingorder === 'asc' ? -1 : 1
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
        if (NAvalues.includes(jsonObject1['ActiveSubstance'])) {
          return sortingorder === 'asc' ? 1 : -1
        } else if (NAvalues.includes(jsonObject2['ActiveSubstance'])) {
          return sortingorder === 'asc' ? -1 : 1
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
        if (NAvalues.includes(jsonobject1['ApplicationNo'])) {
          return sortingorder === 'asc' ? 1 : -1
        } else if (NAvalues.includes(jsonobject2['ApplicationNo'])) {
          return sortingorder === 'asc' ? -1 : 1
        } else {
          return jsonobject1['ApplicationNo'] - jsonobject2['ApplicationNo']
        }
      }
      sortingFunctionToUse = numberorNAcompare
      break
    case 'LegalType':
      function legaltypecompare(jsonobject1, jsonobject2) {
        if (NAvalues.includes(jsonobject1['LegalType'])) {
          return sortingorder === 'asc' ? 1 : -1
        } else if (NAvalues.includes(jsonobject2['LegalType'])) {
          return sortingorder === 'asc' ? -1 : 1
        } else {
          if (
            jsonobject1['LegalType'].slice(0, 7) !== 'article' ||
            jsonobject2['LegalType'].slice(0, 7) !== 'article'
          ) {
            console.log(
              "sorting error: unknown article format. Please specify sorting order for this legaltype comparison; '" +
                jsonobject1['LegalType'] +
                "' compared to '" +
                jsonobject2['LegalType'] +
                "'"
            )
            return 0
          }
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
            'NA',
          ]
          if (!sortOrder.includes(legalnumber1)) {
            console.log(
              "article number '" +
                legalnumber1 +
                "' is not specified in the legaltype articles sorting order, please specifiy this article number's order in the sorting array 'sortOrder' in the file 'sorting.js'"
            )
            return 0
          }
          if (!sortOrder.includes(legalnumber2)) {
            console.log(
              "article number '" +
                legalnumber2 +
                "' is not specified in the legaltype articles sorting order, please specifiy this article number's order in the sorting array 'sortOrder' in the file 'sorting.js'"
            )
            return 0
          }

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
      sortingFunctionToUse = createComparisonFunction(
        attributeNameAsString,
        sortingorder
      )
  }

  return sortingFunctionToUse
}
