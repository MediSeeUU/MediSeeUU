
// function based component, represents a content container, in 
// which all content components should be displayed
function Container(props) {
  return (
    <div className="content-container">
      {props.children}
    </div>
  );
}

export default Container;