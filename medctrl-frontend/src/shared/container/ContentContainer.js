import './ContentContainer.css'

// function based element, represents a content container in which content
// can be displayed on the page
function ContentContainer(props) {
  let className = "content-container";
  let addClassName = props.className;
  if(addClassName !== "") {
    className = className + " " + addClassName;
  }
  return (
    <div className={className}>
      {props.children}
    </div>
  );
}

export default ContentContainer;