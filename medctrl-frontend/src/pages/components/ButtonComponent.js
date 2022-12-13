import React from 'react'
import '../data/data_select/menu/Menu.css'
import './Button.css'

const ButtonType = {
  Simple: "simple",
  Special: "special"
}

function ButtonComponent( { text, icon, clickFunction, buttonType} ) {

  var buttonString = ""

  switch (buttonType) 
  {
    case ButtonType.Simple:
      buttonString = "med-primary-solid med-bx-button med-data-button"
      break;
    case ButtonType.Special:
      buttonString = "med-primary-solid med-bx-button-special med-selector-button"                
      break;
  }

  var iconPath = "bx " + icon + " med-button-image"

  return (
    <button 
      onClick = {() => {
        clickFunction();
      }}
      className={buttonString}
    >
    <i className={iconPath} />    
      {text}
    </button>
  )
} 

export default ButtonComponent

