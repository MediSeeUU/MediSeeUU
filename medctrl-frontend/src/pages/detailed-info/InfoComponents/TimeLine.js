function TimeLine(props) {
  let procedures = props.procs

  let allElements = procedures.map((proc) => {
    return (
      <TimeLineElement
        date={proc.DecisionDate}
        event={proc.ProcType}
        key={proc.DecisionDate.toString() + '-' + proc.ProcType.toString()}
      />
    )
  })

  return <div className="timeline">{allElements}</div>
}

function TimeLineElement(props) {
  return (
    <div className="el">
      <div className="timestamp">
        <span className="date">{props.date}</span>
      </div>
      <div className="border-div" />
      <div className="event">
        <span>{props.event}</span>
      </div>
    </div>
  )
}

export default TimeLine
