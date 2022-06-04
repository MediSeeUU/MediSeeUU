import React from 'react'
import './Table.css'
import Header from './Components/Header'
import ColumnAmount from './Components/ColumnAmount'
import Body from './Components/Body'

// Function based component which renders the table
function Table({
  data,
  select,
  amountPerPage,
  currentPage,
  sorters,
  setSorters,
}) {
  return (
    <>
      <ColumnAmount options={Object.keys(data[0])} />
      <table className="med-table">
        <Header select={select} sorters={sorters} setSorters={setSorters} />
        <Body
          data={data}
          select={select}
          amountPerPage={amountPerPage}
          currentPage={currentPage}
        />
      </table>
    </>
  )
}

export default Table
