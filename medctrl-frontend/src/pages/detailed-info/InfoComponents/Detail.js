// function based component, represents a single detail entry, which
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
