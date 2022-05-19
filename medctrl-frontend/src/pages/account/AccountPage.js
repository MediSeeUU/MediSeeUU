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
