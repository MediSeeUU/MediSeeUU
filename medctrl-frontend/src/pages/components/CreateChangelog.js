import React from 'react'
import CollapsibleButton from './CollapsibleButton'


function ChangelogToText(changes)
{
    let text = ""

    for(var key1 in changes) {
        for (var key2 in changes[key1]) {
            if (changes[key1][key2] == "") 
            {
                text += CapitalizeFirstLetter(key2) + ":\n\n"  
            }
            else
            {
                text += CapitalizeFirstLetter(key2) + ": " + changes[key1][key2] + '\n'
            }
        }
     }
    
    return text
}

function CapitalizeFirstLetter(string) {
    return string.charAt(0).toUpperCase() + string.slice(1);
  }

function CreateChangelog({json}) {

    let changelog = json["changelogs"].map((change) => {
        return (
            <CollapsibleButton
                name={change["new_file"]}
                content={ChangelogToText(change["changes"])}
            />
        )
    })

    return <div>{changelog}</div>
}

export default CreateChangelog