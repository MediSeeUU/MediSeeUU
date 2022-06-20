// This program has been developed by students from the bachelor Computer Science at
// Utrecht University within the Software Project course.
// © Copyright Utrecht University (Department of Information and Computing Sciences)
import { cssVar } from '../SettingsPage'

// Function based component, represents a single color selector
// it display the human friendly variable name and a color input
// field for the user to change the current color value
export default function ColorSelector({ variable, name }) {
  const currentValue = cssVar(variable)
  return (
    <div className="med-color-select-field">
      <span>{name}</span>
      <input
        type="color"
        defaultValue={currentValue}
        className="med-color-picker"
        id={variable}
      />
    </div>
  )
}
