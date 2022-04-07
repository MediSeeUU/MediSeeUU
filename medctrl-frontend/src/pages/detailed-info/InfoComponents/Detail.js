
// function based component, represents a single detail entry, which
// preferably resides inside a detail group component
function Detail(props) {
  return (
    <div className="detail">
      <span className="detail-name">{props.name}</span>
      <span className="detail-value">{props.value}</span>
    </div>
  );
}

export default Detail;