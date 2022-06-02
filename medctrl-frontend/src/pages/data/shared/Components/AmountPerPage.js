// Function based component that renders the select component with amount of entries per page
function AmountPerPage({data, resultsPerPage}) {
  // Available options
  let options = []

  // Calculate the max amount of entries per page
  let upper = data.length >= 300 ? 300 : data.length
  if (data.length % 25 > 0 && data.length < 300) upper += 25

  // Populate the options
  for (let j = 25; j <= upper; j += 25) {
    options.push(
      <option key={j} value={j}>
        {j}
      </option>
    )
  }

  return (
    <div className="med-result-count-selector-container">
      <label>Results per page</label>
      <select
        onChange={(event) => resultsPerPage(event.target.value)}
        name="AmountShown"
        className="med-select"
        id="med-result-count-selector"
      >
        {options}
      </select>
    </div>
  )
}

export default AmountPerPage
