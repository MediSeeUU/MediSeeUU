// This program has been developed by students from the bachelor Computer Science at
// Utrecht University within the Software Project course.
// © Copyright Utrecht University (Department of Information and Computing Sciences)
import TimeLineElement from './TimeLineElement'
import { v4 } from 'uuid'

// function based element, which represents a visual timeline that includes
// all of the procedures which are passed to this component as a prop. Each
// element displays both the date and the type of the procedure, if any of
// these fields are unavailable, 'NA' is displayed
function TimeLine({ procedures, lastUpdatedDate }) {
  const clean = (value) => {
    return !value ? 'NA' : value
  }

  // for each of the given procedures, create a timeline element
  // and add each element to an array for temporary storage
  let allElements = procedures.map((proc) => {
    return (
      <TimeLineElement
        date={clean(proc.decisiondate)}
        event={clean(proc.proceduretype)}
        specialEvent={false}
        key={v4()}
      />
    )
  })

  // add a final timeline element the signify the date up to
  // which this timeline is complete
  if (lastUpdatedDate !== undefined && lastUpdatedDate !== null) {
    allElements.push(
      <TimeLineElement
        date={clean(lastUpdatedDate)}
        event={'End of Database'}
        specialEvent={true}
        key={v4()}
      />
    )
  }

  return <div className="med-info-timeline">{allElements}</div>
}

export default TimeLine
