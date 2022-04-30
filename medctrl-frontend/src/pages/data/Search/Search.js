import './Search.css'
import React, { useState } from 'react'
import { useSearchParams } from 'react-router-dom'

function Search({update}) {
  // We need a parameter state for the initial query
  const [params, setParams] = useSearchParams()

  // We need a separate state for saving the query given in the textbox
  const [query, setQuery] = useState("")

  // Check if the query is specified in the url parameter
  const paramValue = params.get('q')
  if (paramValue) {
    // Delete the parameter value to prevent infinite loop in rendering
    params.delete('q')
    setParams(params)

    // Update the search
    update(paramValue)
  }

  // Handler that updates the search after pressing enter key
  const handlerKeyDown = (e) => {
    if (e.key === 'Enter') {
      update(query)
    }
  }

  // The HTML code of the search component
  return (
    <div className="med-content-container">
      <input
        type="text"
        placeholder="Search"
        className="content__container__textinput med-text-input"
        onChange={(e) => setQuery(e.target.value)}
        defaultValue={paramValue || ""}
        onKeyDown={handlerKeyDown}
      />
      <button className="med-primary-solid med-bx-button" onClick={() => update(query)}>
        <i className="bx bx-search search-Icon"></i>Search
      </button>
    </div>
  )
}

export default Search
