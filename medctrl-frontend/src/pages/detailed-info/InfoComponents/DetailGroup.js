
// function based component, represents detail group component which 
// preferably holds individual detail components, which are included as childern
function DetailGroup(props) {
  return (
    <div className="detail-group">
      <h2 className="detail-group-title">
        {props.title}
      </h2>
      {props.children}
    </div>
  );
}

export default DetailGroup;