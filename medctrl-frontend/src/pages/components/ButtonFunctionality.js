import React, {useState} from 'react'
import raw from './showText.txt'
import json from './comparison.json'

export function FieldsMenu() {
    alert("Fields Menu")  
}

export function FilterMenu() {
    alert("Filter Menu") 
}

export function OpenHuman() {
    alert("You pressed on Human Medicinal Products.")
}

export function OpenOrphan() {
    alert("You pressed on Orphan Designations.")
}

const disableClick = event => {
    event.currentTarget.disabled = true;
}

export function ShowText() {
    alert(json["changes"][0]['old text'], json["changes"][0]["new text"])

    // outputs the content of the text file
}
