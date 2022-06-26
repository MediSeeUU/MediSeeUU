// This program has been developed by students from the bachelor Computer Science at
// Utrecht University within the Software Project course.
// © Copyright Utrecht University (Department of Information and Computing Sciences)

import React, { useContext, useState } from 'react'
import Joyride, { ACTIONS, EVENTS, STATUS } from 'react-joyride'
import { useNavigate } from 'react-router-dom'
import { useTableUtils } from '../../shared/contexts/TableUtilsContext'
import { useCheckedState } from '../../shared/contexts/CheckedContext'
import { useVisuals } from '../../shared/contexts/VisualsContext'

// This array holds all of the steps that the tour will take, each has
// a specific target which that step should highlight, the title and
// content fields are the actually informative fields for the user
import steps from './TourSteps.json'
import { useColumnSelection } from '../../shared/contexts/ColumnSelectionContext'

// A data context which allows the 'start tour' button on the home
// page to actually start a tour
const TourRunContext = React.createContext()
export function useTourRun() {
  return useContext(TourRunContext)
}

// Function based component, which acts as a tour provider, all of its children
// can trigger the tour discribed by the steps above
function DashboardTour(props) {
  // Internal states which say whether or not a tour is currently taking place,
  // and what the current step of the tour is (if it is currently taking place)
  const [runJoyride, setRunJoyride] = useState(false)
  const [step, setStep] = useState(0)

  let navigate = useNavigate()

  let { setTableUtils } = useTableUtils()

  let { checkedState, setCheckedState } = useCheckedState()

  let { setVisuals } = useVisuals()

  let { setColumnSelection } = useColumnSelection()

  // Function to handle a update to the tour, i.e. when the user wants to
  // view the next step in the tour
  const handleCallback = (data) => {
    const { action, index, lifecycle, status, type } = data

    // If the dashboard tour is not active, we should not update
    // the internal joyride state
    if (!runJoyride) {
      return
    }

    // If the tour is starting, make sure that the tour starts on the correct page,
    // and that all of the contexts have the correct values to support the tour
    if (index === 0 && lifecycle === 'init') {
      navigate(steps[0].page)

      // During the tour, we only want to show medicines by pfizers
      setTableUtils({
        search: 'pfizer',
        sorters: [{ selected: 'DecisionDate', order: 'asc' }],
        filters: [
          {
            selected: 'BrandName',
            input: [{ var: '', filterRange: 'from' }],
            filterType: '',
          },
        ],
      })

      // From all of the medicines by pfizers, only select the ones
      // with a 'withdrawn' status
      let newCheckedState = {}
      const checked = [
        59, 60, 78, 121, 167, 244, 259, 327, 353, 1100, 1165, 1183, 1421,
      ]
      for (let key in checkedState) {
        newCheckedState[key] = checked.includes(parseInt(key))
      }
      setCheckedState(newCheckedState)

      // For the visualization, we want to see how many medicines by pfizers have
      // a 'withdrawn' status, plotted against the year that they were first approved
      setVisuals([
        {
          id: 1,
          chartType: 'histogram',
          chartSpecificOptions: {
            xAxis: 'DecisionYear',
            yAxis: 'Rapporteur',
            categoriesSelectedY: [],
            categoriesSelectedX: [
              1998, 1999, 2001, 2003, 2006, 2016, 2017, 2020,
            ],
          },
          legendOn: false,
          labelsOn: true,
        },
      ])

      // When displaying the datapoints on the data page, we are referring to all
      // medicines which have a withdrawn status, we want to make sure that the
      // status variable is visible in the selection table
      setColumnSelection([
        'EUNoShort',
        'BrandName',
        'MAH',
        'DecisionDate',
        'Status',
      ])
    }

    // If the user wants to progress the tour a step, but the next step
    // resides on a different page, first navigate to that page, before
    // advancing the tour a step
    if (
      index + 1 < steps.length &&
      steps[index].page !== steps[index + 1].page &&
      type === EVENTS.STEP_AFTER &&
      action === ACTIONS.NEXT
    ) {
      navigate(steps[index + 1].page)
      setStep(index + 1)
      return
    }

    // Otherwise, the tour can be advanced without having to navigate
    // to another page. if the tour is finished, the internal state should
    // be reset and the user redirected to the home page
    if ([EVENTS.STEP_AFTER, EVENTS.TARGET_NOT_FOUND].includes(type)) {
      setStep(index + (action === ACTIONS.PREV ? -1 : 1))
    } else if (
      [STATUS.FINISHED, STATUS.SKIPPED].includes(status) ||
      action === ACTIONS.CLOSE
    ) {
      setRunJoyride(false)
      setStep(0)
      navigate('/')
    }
  }

  // Returns the actual html element, which includes the joyride component,
  // as well as the data context
  return (
    <div>
      <TourRunContext.Provider value={setRunJoyride}>
        <Joyride
          steps={steps}
          stepIndex={step}
          run={runJoyride}
          callback={handleCallback}
          showProgress={false}
          continuous={true}
          showSkipButton={true}
          disableScrolling={true}
          disableCloseOnEsc={true}
          disableOverlayClose={true}
          locale={{
            back: 'Back',
            close: 'Close',
            last: 'Finish',
            next: 'Next',
            open: 'Open the dialog',
            skip: 'End',
          }}
          styles={{
            options: {
              arrowColor: 'var(--secondary-light)',
              backgroundColor: 'var(--secondary-light)',
              primaryColor: 'var(--primary-normal)',
              textColor: 'var(--text-primary)',
              zIndex: 10000,
            },
          }}
        />
        {props.children}
      </TourRunContext.Provider>
    </div>
  )
}

export default DashboardTour
