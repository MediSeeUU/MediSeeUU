import './Search.css'
import React, { useState } from 'react'

function Search({ update, initial, tour }) {
  // We need a separate state for saving the query given in the textbox
  const [query, setQuery] = useState(initial)

  // Handler that applies the search by updating the query
  const applySearch = () => {
    // eslint-disable-next-line no-new-wrappers
    update(new String(query)) // new String() is required here to also update with same query string
  }

  // Handler that updates the search after pressing enter key
  const handlerKeyDown = (e) => {
    if (e.key === 'Enter') {
      applySearch()
    }
  }

  // Handler that clears the search query
  const clearSearch = () => {
    setQuery("")
    update("")
  }

  // The HTML code of the search component
  return (
    <div tour={tour} className="med-content-container">
      <div className="med-search-container">
        {query && <i className="bx bx-x med-search-close-icon" onClick={clearSearch}></i>}
        <input
          type="text"
          placeholder="Search"
          className="med-search-text-input med-text-input"
          onChange={(e) => setQuery(e.target.value)}
          value={query || ""}
          onKeyDown={handlerKeyDown}
        />
      </div>
      <button
        className="med-primary-solid med-bx-button med-search-button"
        onClick={applySearch}
      >
        <i className="bx bx-search med-button-image"></i>Search
      </button>
    </div>
  )
}

export default Search
