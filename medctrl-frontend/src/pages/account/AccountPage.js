import SavedSelections from './SavedSelections/SavedSelections'

function AccountPage() {
  return (
    <div className="med-content-container">
      <h1>Additional Account Information</h1>
      <hr className="med-top-separator" />

      <div className="flex-columns">
        <SavedSelections />
      </div>
    </div>
  )
}

export default AccountPage
