// This program has been developed by students from the bachelor Computer Science at
// Utrecht University within the Software Project course.
// © Copyright Utrecht University (Department of Information and Computing Sciences)
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