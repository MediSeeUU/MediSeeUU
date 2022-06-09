import Joyride, { ACTIONS, EVENTS, STATUS } from 'react-joyride'
import React, { useContext, useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import {
  useCheckedState,
  useCheckedStateUpdate,
  useTableUtilsUpdate,
  useVisuals,
  useVisualsUpdate,
} from '../../shared/contexts/DataContext'
import { v4 } from 'uuid'

// A data context which allows the 'start tour' button on the home
// page to actually start a tour
const TourRunContext = React.createContext()
export function useTourRun() {
  return useContext(TourRunContext)
}

// this array holds all of the steps that the tour will take, each has
// a specific target which that step should highlight, the title and
// content fields are the actually informative fields for the user
const steps = [
  {
    target: "[tour='step-search']",
    title: 'Quick Search',
    content: (
      <p>
        You can quickly search for a specific medicine using this quick search
        feature. When you type in a search query and hit enter, you will be
        redirected to view the search results.
      </p>
    ),
    placement: 'auto',
    disableBeacon: true,
    page: '/',
  },
  {
    target: "[tour='step-nav-login']",
    title: 'Login',
    content: (
      <p>
        Use this button to access the login screen. There you can login, after
        which you may enjoy an enhanced experience.
      </p>
    ),
    placement: 'left-start',
    disableBeacon: true,
    page: '/',
  },
  {
    target: "[tour='step-nav-data']",
    content: (
      <p>
        Use this link to access the data page, on this page you can view, select
        and export all the datapoints available to you. Let's navigate to the
        data page and start selecting some datapoints!
      </p>
    ),
    title: 'Data Page',
    placement: 'auto',
    disableBeacon: true,
    page: '/',
  },
  {
    target: "[tour='step-data-search']",
    content: (
      <p>
        On the data page, you again find a search bar, use this search bar to
        look for specific medicines. We can search for 'pfizer' and all
        medicines related to pfizer will be displayed in the table below. Let's
        explore that table next!
      </p>
    ),
    title: 'Data Search',
    placement: 'auto',
    disableBeacon: true,
    page: '/data',
  },
  {
    target: "[tour='step-data-select']",
    content: (
      <p>
        In this table you can select individual datapoints using the checkmark
        on the left and view more information using the 'i' on the right. Use
        the filter and sort button to filter and sort the data points which are
        displayed in the table. Here we can select all the medicines which have
        a status of 'withdrawn'.
      </p>
    ),
    title: 'Data Selection Table',
    placement: 'auto',
    disableBeacon: true,
    page: '/data',
  },
  {
    target: "[tour='step-data-selected']",
    content: (
      <p>
        All of the datapoints that you have selected in the table above (in our
        case, all medicines by pfizer with a status of 'withdrawn'), will appear
        here. You can either export these datapoints to a file (using the export
        button), or use them to create a visualization. Let's see if we can make
        an informative visualization using these datapoints.
      </p>
    ),
    title: 'Selected Data Points',
    placement: 'auto',
    disableBeacon: true,
    page: '/data',
  },
  {
    target: "[tour='step-nav-vis']",
    content: (
      <p>
        To create a visualization, we first need to navigate to the
        visualization page. We can use this link to accomplish this.
      </p>
    ),
    title: 'Visualizations Page',
    placement: 'auto',
    disableBeacon: true,
    page: '/data',
  },
  {
    target: "[tour='step-vis-main']",
    content: (
      <p>
        On the visualization page, we are greeted by a single visualization. But
        to make it ours, we still need to adjust some of its parameters.
      </p>
    ),
    title: 'Visualization',
    placement: 'auto',
    disableBeacon: true,
    page: '/visualizations',
  },
  {
    target: "[tour='step-vis-type']",
    content: (
      <p>
        First, we need to pick a chart type, for example a bar or line chart. If
        applicable you can select extra modifiers below to further customize the
        chart, like flipping the chart on its side (using horizontal). Here we
        select the histogram type, this way we can see how many medicine by
        pfizer have a 'withdrawn' status per year.
      </p>
    ),
    title: 'Chart Type',
    placement: 'auto',
    disableBeacon: true,
    page: '/visualizations',
  },
  {
    target: "[tour='step-vis-vars']",
    content: (
      <p>
        Next we need to decide what variables we want to visualize. For bar and
        line charts we need to select two variables, but for a pie chart one is
        more than enough. For a histogram we only need to select one variable,
        since we want to plot against time, we select the decision year variable
        here.
      </p>
    ),
    title: 'Variables',
    placement: 'auto',
    disableBeacon: true,
    page: '/visualizations',
  },
  {
    target: "[tour='step-vis-categories']",
    content: (
      <p>
        Finally, we can select certain categories, for both the X-axis and the
        Y-axis variables to be included or excluded from the visualization. For
        our example we are interested in all of the categories.
      </p>
    ),
    title: 'Categories',
    placement: 'auto',
    disableBeacon: true,
    page: '/visualizations',
  },
  {
    target: "[tour='step-vis-plot']",
    content: (
      <p>
        After having configured all of the appropriate settings, we are left
        with our final result. Here we can see that in 1998, the most medicines
        by pfizer have a 'withdrawn' status. If we want to download this
        visualisation, we can do so using the two buttons below.
      </p>
    ),
    title: 'Final Visualization',
    placement: 'auto',
    disableBeacon: true,
    page: '/visualizations',
  },
  {
    target: "[tour='step-nav-home']",
    content: (
      <p>
        That concludes our tour, you will be returned to the home page after
        which you can start to use all of the features that this dashboard has
        to offer!
      </p>
    ),
    title: 'End of Tour',
    placement: 'auto',
    disableBeacon: true,
    page: '/visualizations',
  },
]

// function based component, which acts as a tour provider, all of its children
// can trigger the tour discribed by the steps above
function DashboardTour(props) {
  // internal states which say whether or not a tour is currently taking place,
  // and what the current step of the tour is (if it is currently taking place)
  const [runJoyride, setRunJoyride] = useState(false)
  const [step, setStep] = useState(0)

  let navigate = useNavigate()

  let utilsUpdate = useTableUtilsUpdate()

  let checkedState = useCheckedState()
  let checkedStateUpdate = useCheckedStateUpdate()

  let visualState = useVisuals()
  let updateVisualState = useVisualsUpdate()

  // function to handle a update to the tour, i.e. when the user wants to
  // view the next step in the tour
  const handleCallback = (data) => {
    const { action, index, lifecycle, status, type } = data

    // if the dashboard tour is not active, we should not update
    // the internal joyride state
    if (!runJoyride) {
      return
    }

    // if the tour is starting, make sure that the tour starts on the correct page,
    // and that all of the contexts have the correct values to support the tour
    if (index === 0 && lifecycle === 'init') {
      navigate(steps[0].page)

      // during the tour, we only want to show medicines by pfizers
      utilsUpdate({
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

      // from all of the medicines by pfizers, only select the ones
      // with a 'withdrawn' status
      let newCheckedState = {}
      const checked = [
        59, 60, 78, 121, 167, 244, 259, 327, 353, 1100, 1165, 1183, 1421,
      ]
      for (let key in checkedState) {
        newCheckedState[key] = checked.includes(parseInt(key))
      }
      checkedStateUpdate(newCheckedState)

      // for the visualization, we want to see how many medicines by pfizers have
      // a 'withdrawn' status, plotted against the year that they were first approved
      updateVisualState([
        {
          id: 1,
          chartType: 'histogram',
          chartSpecificOptions: {
            xAxis: 'DecisionYear',
            categoriesSelectedX: [
              1998, 1999, 2001, 2003, 2006, 2016, 2017, 2020,
            ],
            ...visualState.chartSpecificOptions,
          },
          legendOn: false,
          labelsOn: true,
          key: v4(),
          ...visualState,
        },
      ])
    }

    // if the user wants to progress the tour a step, but the next step
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

    // otherwise, the tour can be advanced without having to navigate
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

  // returns the actual html element, which includes the joyride component,
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
