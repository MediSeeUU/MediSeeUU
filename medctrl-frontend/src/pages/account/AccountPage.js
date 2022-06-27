// This program has been developed by students from the bachelor Computer Science at
// Utrecht University within the Software Project course.
// © Copyright Utrecht University (Department of Information and Computing Sciences)

import React from 'react'
import SavedSelections from './saved_selection/SavedSelections'

// Function based component that renders the account page
// The component displays general account information, in this case, only the saved selections
function AccountPage() {
  return (
    <div className="med-content-container">
      <h1>Saved Data Selections</h1>
      <hr className="med-top-separator" />
      <SavedSelections />
    </div>
  )
}

export default AccountPage
