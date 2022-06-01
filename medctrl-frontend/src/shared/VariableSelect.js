import { useStructure } from './contexts/DataContext'
import { v4 } from 'uuid'

// Function based component, represents a select element. All of the select options
// are subdivided into categories, each option's value is the key at which to access
// the corresponding data field in the context, but the display name is a more
// user friendly version of the same name
export default function VariableSelect({
  className,
  onChange,
  defaultValue,
  dataTestId,
}) {
  const variableCategories = useStructure()
  const optGroups = []

  for (let category in variableCategories) {
    const options = [
      <option value="" hidden>
        Choose a variable...
      </option>,
    ]

    for (let varIndex in variableCategories[category]) {
      const variable = variableCategories[category][varIndex]
      options.push(
        <option value={variable['data-front-key']} key={v4()}>
          {variable['data-value']}
        </option>
      )
    }

    optGroups.push(
      <optgroup label={category} key={v4()}>
        {options}
      </optgroup>
    )
  }

  return (
    <select
      className={className}
      onChange={onChange}
      value={defaultValue}
      data-testid={dataTestId}
    >
      {optGroups}
    </select>
  )
}
