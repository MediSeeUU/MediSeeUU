import React from 'react'
import '../data/data_select/menu/Menu.css'

function ButtonComponent( { text, icon, clickFunction} ) {

  var icon_path = "bx " + icon + " med-button-image"

  return (
    <button 
      onClick={clickFunction}
      className="med-primary-solid med-bx-button med-data-button">
    <i className={icon_path} />    
      {text}
    </button>
  )
} 

export default ButtonComponent

