// This program has been developed by students from the bachelor Computer Science at
// Utrecht University within the Software Project course.
// © Copyright Utrecht University (Department of Information and Computing Sciences)
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
      <ColumnAmount />
      <table className={!select ? 'med-table med-table-select' : 'med-table'}>
        <Header data={data} select={select} sorters={sorters} setSorters={setSorters} />
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
