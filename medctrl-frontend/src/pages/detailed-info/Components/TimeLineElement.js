// This program has been developed by students from the bachelor Computer Science at
// Utrecht University within the Software Project course.
// © Copyright Utrecht University (Department of Information and Computing Sciences)
// function based component, which represents a single element on the time line
// component. is displays both a date and event string, one above a decorative
// circle, and one below, separated by a line
function TimeLineElement({ date, event, specialEvent }) {
  let topLevelClassName = 'med-info-timeline-element'
  topLevelClassName += specialEvent ? ' med-info-special' : ''
  return (
    <div className={topLevelClassName}>
      <div className="med-info-timeline-element-timestamp">
        <span>{date}</span>
      </div>
      <div className="med-info-timeline-element-decoration" />
      <div className="med-info-timeline-element-event">
        <span>{event}</span>
      </div>
    </div>
  )
}

export default TimeLineElement
