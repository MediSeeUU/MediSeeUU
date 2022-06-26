// This program has been developed by students from the bachelor Computer Science at
// Utrecht University within the Software Project course.
// © Copyright Utrecht University (Department of Information and Computing Sciences)

import React, { useState } from 'react'
import './Search.css'

// Function based component rendering the search bar and button
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
    setQuery('')
    update('')
  }

  return (
    <div tour={tour} className="med-content-container">
      <div className="med-search-container">
        { /* Only show the X if there is actual input in the search bar */
        query && (
          <i
            className="bx bx-x med-search-close-icon"
            onClick={clearSearch}
            data-testid="search-close-icon"
          ></i>
        )}
        <input
          type="text"
          placeholder="Search"
          className="med-search-text-input med-text-input"
          onChange={(e) => setQuery(e.target.value)}
          value={query || ''}
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
