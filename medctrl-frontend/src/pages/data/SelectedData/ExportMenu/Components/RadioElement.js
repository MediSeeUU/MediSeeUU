// This program has been developed by students from the bachelor Computer Science at
// Utrecht University within the Software Project course.
// © Copyright Utrecht University (Department of Information and Computing Sciences)
// function based element, represents a radio button with custom styling
function RadioElement(props) {
  return (
    <label className="med-radio-label">
      <input
        onChange={props.onChange}
        type="radio"
        name={props.name}
        className="med-radio-input"
        id={props.id}
      />
      <div className="med-radio-visual"> </div>
      <span>{props.value}</span>
      {props.children}
    </label>
  )
}

export default RadioElement
