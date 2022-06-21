// This program has been developed by students from the bachelor Computer Science at
// Utrecht University within the Software Project course.
// © Copyright Utrecht University (Department of Information and Computing Sciences)
import SavedSelections from './SavedSelections/SavedSelections'

// Account page component that displays the general account information
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
