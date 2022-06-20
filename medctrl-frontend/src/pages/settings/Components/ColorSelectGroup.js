// This program has been developed by students from the bachelor Computer Science at
// Utrecht University within the Software Project course.
// © Copyright Utrecht University (Department of Information and Computing Sciences)
import ColorSelector from './ColorSelector'
import { v4 } from 'uuid'

// Function based component, represents a single group of color
// selectors. Each group has a title, a small description, followed
// by all the individual color selectors
export default function ColorSelectGroup({ colors, name, desc }) {
  const colorSelectors = []
  for (const idx in colors) {
    const color = colors[idx]
    colorSelectors.push(
      <ColorSelector
        variable={color['Variable']}
        name={color['Display Name']}
        key={v4()}
      />
    )
  }

  return (
    <div className="med-color-group">
      <h1>{name}</h1>
      <hr className="med-top-separator" />
      <p className="med-color-group-desc">{desc}</p>
      {colorSelectors}
    </div>
  )
}
