import React, { useState } from 'react'
import './Search.css'
import { useSearchParams } from 'react-router-dom'

function Search({data, updateData}) {
  const [params, setParams] = useSearchParams()
  const [query, setQuery] = useState("")

  const update = (value) => {
    let updatedData = [...data]
    updatedData = updatedData.filter(obj => {
      let inText = false
      let vals = Object.values(obj)
      for (const val of vals) {
        if (val.toString().toLowerCase().includes(value.toLowerCase())) {
          inText = true
          break
        }
      }
      return inText
    })
    updateData(updatedData)
  }

  const paramValue = params.get('q')
  if (paramValue) {
    // Delete the parameter value to prevent infinite loop in rendering
    params.delete('q')
    setParams(params)
    
    update(paramValue)
  }

  const handlerKeyDown = (e) => {
    if (e.key === 'Enter') {
      update(query)
    }
  }

  return (
    <div className="med-content-container">
      <input
        type="text"
        placeholder="Search"
        className="content__container__textinput med-text-input"
        onChange={(e) => setQuery(e.target.value)}
        onKeyDown={handlerKeyDown}
      />
      <button className="med-primary-solid med-bx-button" onClick={() => update(query)}>
        <i className="bx bx-search search-Icon"></i>Search
      </button>
    </div>
  )
}

export default Search
