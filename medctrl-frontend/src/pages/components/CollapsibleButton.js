import React from 'react'
import { useState } from 'react'

function CollapsibleButton({name, content}) {

    const [open, setOpen] = useState(false)

    const toggle = () => {
        setOpen(!open)
    }

    return (
        <div>
            <button 
                className="med-primary-solid med-info-changelog-button"
                onClick={toggle}>
                    {name}
            </button>  
            {
                open && 
                <div className="med-info-changelog-container ">
                    {content}

                </div>
            }    
        </div>
    )
}

export default CollapsibleButton
