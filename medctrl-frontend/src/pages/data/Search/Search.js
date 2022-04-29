import React, { useState } from 'react'
import './Search.css'

function Search({data, updateData}) {
  const [searchQuery, setQuery] = useState("")

  const updateSearch = () => {
    let updatedData = [...data]
    updatedData = updatedData.filter(obj => {
      let inText = false
      let vals = Object.values(obj)
      for (const val of vals) {
        if (val.toString().toLowerCase().includes(searchQuery.toLowerCase())) {
          inText = true
          break
        }
      }
      return inText
    })
    updateData(updatedData)
  }

  return (
    <div className="med-content-container">
      <input
        type="text"
        placeholder="Search"
        className="content__container__textinput med-text-input"
        onChange={(e) => setQuery(e.target.value)}
      />
      <button className="med-primary-solid med-bx-button" onClick={updateSearch}>
        <i className="bx bx-search search-Icon"></i>Search
      </button>
    </div>
  )
}

export default Search
