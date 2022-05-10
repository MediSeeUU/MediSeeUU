
// function based component, which represents a single element on the time line
// component. is displays both a date and event string, one above a decorative
// circle, and one below, separated by a line
function TimeLineElement(props) {
  let date = props.date
  let event = props.event

  return (
    <div className="el">
      <div className="timestamp">
        <span className="date">{date}</span>
      </div>
      <div className="decoration" />
      <div className="event">
        <span>{event}</span>
      </div>
    </div>
  )
}

export default TimeLineElement