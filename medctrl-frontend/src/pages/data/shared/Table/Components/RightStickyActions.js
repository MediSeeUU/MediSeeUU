import React from 'react'
import { Link } from 'react-router-dom'

// Function based component that holds actions that are always on the right side of the table
function RightStickyActions({ entry, select, onChange }) {
  return (
    <td className="med-table-body-cell med-table-narrow-column med-column-right">
      {!select && (
        <i
          className="bx bx-trash med-table-icons med-primary-text"
          onClick={onChange.bind(null, entry.EUNoShort)}
        ></i>
      )}
      <Link to={`/details/${entry.EUNoShort}`}>
        <i
          className="bx bx-info-circle med-table-icons med-primary-text"
          id={'detailInfo' + entry.EUNoShort}
          testid={'detailInfo' + entry.EUNoShort}
        />
      </Link>
    </td>
  )
}

export default RightStickyActions
