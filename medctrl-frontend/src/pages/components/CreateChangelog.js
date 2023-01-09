import React from 'react'
import CollapsibleButton from './CollapsibleButton'


function ChangelogToText(changes)
{
    let text = ""


    // "change": "added section",
    // "header": "1 | turn the page for more advice",
    // "section_text": "now turn over>\n 17\n",


    for(var key1 in changes) {
        text += changes[key1]["change_note"]
        // text += changes[key1]["change"]
        // text += changes[key1]["header"] + "\n"
        // text += "Section Text: " + changes[key1]["section_text"] + "\n"
        // for (var key2 in changes[key1]) {
            // if (changes[key1][key2] == "") 
            // {
            //     text += CapitalizeFirstLetter(key2) + ":\n\n"  
            // }
            // else
            // {
            //     text += CapitalizeFirstLetter(key2) + ": " + changes[key1][key2] + '\n'
            // }
            
        //}
     }
    
    return text
}

function CapitalizeFirstLetter(string) {
    return string.charAt(0).toUpperCase() + string.slice(1);
  }

function CreateChangelog({json}) {

    let last_updated = json["last_updated"]
    const myArray = last_updated.split(".")
    let noMicroseconds = myArray[0]
    //last_updated = String.prototype.split(".")[0]


    let changelog = json["changelogs"].map((change) => {
        return (
            <CollapsibleButton
                name={change["old_file"] + "    →    " + change["new_file"]}
                content={ChangelogToText(change["changes"])}
            />
        )
    })

    return (
        <>
             <h2 className="med-header">Last Updated: {noMicroseconds}</h2>
            <div>{changelog}</div>
        </>
        )
}

export default CreateChangelog