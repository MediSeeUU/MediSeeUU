import Joyride, { ACTIONS, EVENTS, STATUS } from 'react-joyride'
import React, { useContext, useState } from 'react'
import { useNavigate } from 'react-router-dom'

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
        data page!
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
        look for specific medicines. The results to your query will be displayed
        in the table below. Let's explore that table next!
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
        displayed in the table.
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
        All of the datapoints that you have selected in the table above, will
        appear here. You can either export these datapoints to a file (using the
        export button), or use them to create a visualization.
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
        If we want to create a visualization, we first need to navigate to the
        visualization page. We can use this link to do this.
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
        to make it ours, we still need to adjust some of its parameters. And
        when we are done, we can download it with the buttons below.
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
        chart, like flipping the chart on its side (using horizontal).
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
        more than enough.
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
        Y-axis variables to be included or excluded from the visualization.
      </p>
    ),
    title: 'Categories',
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

  // function to handle a update to the tour, i.e. when the user wants to
  // view the next step in the tour
  const handleCallback = (data) => {
    const { action, index, status, type } = data

    // if the tour is starting, navigate to the page where the first step
    // is meant to take place
    if (index === 0) {
      navigate(steps[0].page)
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
