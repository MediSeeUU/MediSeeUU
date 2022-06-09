import { cssVar } from '../SettingsPage'

// function based component, represents a single color selector
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
