// This program has been developed by students from the bachelor Computer Science at
// Utrecht University within the Software Project course.
// © Copyright Utrecht University (Department of Information and Computing Sciences)
import './SettingsPage.css'
import ColorData from './ColorSettingData.json'
import ColorSelectGroup from './Components/ColorSelectGroup'
import { v4 } from 'uuid'

// Function based component, represents the entire settings page. On this page
// all the colors used on the dashboard are displayed and can be changed by the
// user. All of the actual color information is read from a json file
export default function SettingsPage() {
  const groups = []

  for (const color in ColorData) {
    const name = color
    const desc = ColorData[color]['Description']
    const colors = ColorData[color]['Colors']

    groups.push(
      <ColorSelectGroup colors={colors} name={name} desc={desc} key={v4()} />
    )
  }

  const handleOnSubmit = (event) => {
    event.preventDefault()
    var idx = 0
    while (
      event.target[idx] !== undefined &&
      event.target[idx].type === 'color'
    ) {
      cssVar(event.target[idx].id, event.target[idx].value)
      idx++
    }
  }

  return (
    <div className="med-content-container med-color-content">
      <h1>Color Settings Panel</h1>
      <hr className="med-top-separator" />

      <p>
        In the color settings panel you can change all of the colors used on
        this dashboard. The form below shows all of the colors and their current
        values. Each color value can be changed to your preference, and when you
        are satisfied you can use the Apply button to commit to the new colors.
        If you want to start from scratch, use the reset button. The colors are
        not permanently changed, when you reload the dashboard, the original
        colors will return.
      </p>

      <form onSubmit={handleOnSubmit}>
        <div className="med-flex-columns med-color-container">{groups}</div>

        <div className="med-color-button-container">
          <button className="med-primary-solid med-bx-button" type="reset">
            Reset
          </button>
          <button className="med-primary-solid med-bx-button" type="submit">
            Apply
          </button>
        </div>
      </form>
    </div>
  )
}

// custom function used to read and write css variable values
export function cssVar(name, value) {
  if (name[0] !== '-') name = '--' + name
  if (value) document.documentElement.style.setProperty(name, value)
  return getComputedStyle(document.documentElement)
    .getPropertyValue(name)
    .trim()
}
