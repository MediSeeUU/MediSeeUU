import SavedSelections from './SavedSelections/SavedSelections'

// Account page component that displays the general account information
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
