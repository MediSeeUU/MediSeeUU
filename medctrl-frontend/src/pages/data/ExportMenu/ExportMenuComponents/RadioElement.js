// function based element, represents a radio button with custom styling
function RadioElement(props) {
  return (
    <label className="radio-label">
      <input
        onChange={props.onChange}
        type="radio"
        name={props.name}
        className="radio-input"
        id={props.id}
      />
      <div className="radio-visual"> </div>
      <span>{props.value}</span>
      {props.children}
    </label>
  )
}

export default RadioElement
