import React from 'react'
import CollapsibleButton from './CollapsibleButton'

function CreateChangelog({json}) {

    let changelog = json["changelogs"].map((change) => {
        return (
            <CollapsibleButton
                name={change["new_file"]}
                content={JSON.stringify(change["changes"])}
            />
        )
    })

    return <div>{changelog}</div>
}

export default CreateChangelog