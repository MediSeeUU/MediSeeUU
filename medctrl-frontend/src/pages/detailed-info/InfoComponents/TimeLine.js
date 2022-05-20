import TimeLineElement from './TimeLineElement'
import { v4 } from 'uuid'

// function based element, which represents a visual timeline that includes
// all of the procedures which are passed to this component as a prop. Each
// element displays both the date and the type of the procedure, if any of
// these fields are unavailable, 'NA' is displayed
function TimeLine(props) {
  let procedures = props.procs
  let allElements = procedures.map((proc) => {
    const clean = (value) => {
      return !value ? 'NA' : value
    }

    return (
      <TimeLineElement
        date={clean(proc.decisiondate)}
        event={clean(proc.proceduretype)}
        key={v4()}
      />
    )
  })

  return <div className="med-info-timeline">{allElements}</div>
}

export default TimeLine
