// This program has been developed by students from the bachelor Computer Science at
// Utrecht University within the Software Project course.
// © Copyright Utrecht University (Department of Information and Computing Sciences)

// Function based component, represents a single detail entry, which
// preferably resides inside a detail group component
function Detail(props) {
  return (
    <div className="med-info-detail">
      <span className="med-info-detail-name">{props.name}</span>
      <span className="med-info-detail-value">{props.value}</span>
    </div>
  )
}

export default Detail
