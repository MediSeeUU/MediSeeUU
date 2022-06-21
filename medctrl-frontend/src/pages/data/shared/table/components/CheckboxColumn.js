// This program has been developed by students from the bachelor Computer Science at
// Utrecht University within the Software Project course.
// © Copyright Utrecht University (Department of Information and Computing Sciences)
import React from 'react'

// Function based component that renders a checkbox
function CheckboxColumn({ value, onChange }) {
  return (
    <td className="med-table-body-cell med-table-narrow-column med-column-left">
      <input
        className="tableCheckboxColumn"
        type="checkbox"
        checked={value || false}
        onChange={onChange}
      />
    </td>
  )
}

export default CheckboxColumn
