// This program has been developed by students from the bachelor Computer Science at
// Utrecht University within the Software Project course.
// © Copyright Utrecht University (Department of Information and Computing Sciences)
import SavedSelections from './SavedSelections/SavedSelections'

function AccountPage() {
  return (
    <div className="med-content-container">
      <h1>Account Information</h1>
      <hr className="med-top-separator" />

      <div className="med-flex-columns">
        <SavedSelections />
      </div>
    </div>
  )
}

export default AccountPage
