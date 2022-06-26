// This program has been developed by students from the bachelor Computer Science at
// Utrecht University within the Software Project course.
// © Copyright Utrecht University (Department of Information and Computing Sciences)

import React from 'react'

// Function based component, represents detail group component which
// preferably holds individual detail components, which are included as childern
function DetailGroup(props) {
  return (
    <div className="med-info-detail-group">
      <h2 className="med-info-detail-group-title">{props.title}</h2>
      {props.children}
    </div>
  )
}

export default DetailGroup
