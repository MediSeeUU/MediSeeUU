// This program has been developed by students from the bachelor Computer Science at
// Utrecht University within the Software Project course.
// © Copyright Utrecht University (Department of Information and Computing Sciences)
import { v4 } from 'uuid'
import { useStructure } from './Contexts/StructureContext'

// Function based component, represents a select element. All of the select options
// are subdivided into categories, each option's value is the key at which to access
// the corresponding data field in the context, but the display name is a more
// user friendly version of the same name
export default function VariableSelect({
  className,
  onChange,
  defaultValue,
  dataTestId,
  name,
  tour,
}) {
  const variableCategories = useStructure()
  const optGroups = []

  for (let category in variableCategories) {
    const options = []

    for (let varIndex in variableCategories[category]) {
      const variable = variableCategories[category][varIndex]
      if (variable['data-format'] !== 'link') {
        options.push(
          <option value={variable['data-front-key']} key={v4()}>
            {variable['data-value']}
          </option>
        )
      }
    }

    if (options.length > 0) {
      optGroups.push(
        <optgroup label={category} key={v4()}>
          {options}
        </optgroup>
      )
    }
  }

  return (
    <select
      className={className}
      onChange={onChange}
      value={defaultValue}
      data-testid={dataTestId}
      name={name}
      tour={tour}
    >
      <option value="" key={v4()} hidden>
        Choose a variable...
      </option>
      {optGroups}
    </select>
  )
}
