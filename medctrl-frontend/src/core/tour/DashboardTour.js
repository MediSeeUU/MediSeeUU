import Joyride, { ACTIONS, EVENTS, STATUS } from 'react-joyride'
import React, { useContext, useState } from 'react'
import { useNavigate } from 'react-router-dom'

const TourRunContext = React.createContext()
export function useTourRun() {
  return useContext(TourRunContext)
}

const steps = [
  {
    target: "[tour='step-search']",
    title: 'Quick Search',
    content: 'This is my awesome feature!',
    placement: 'auto',
    disableBeacon: true,
    page: '/'
  },
  {
    target: "[tour='step-nav-login']",
    title: 'Login',
    content: 'This another awesome feature!',
    placement: 'left-start',
    disableBeacon: true,
    page: '/'
  },
  {
    target: "[tour='step-nav-data']",
    content: 'This another awesome feature!',
    title: 'Data Page',
    placement: 'auto',
    disableBeacon: true,
    page: '/'
  },
  {
    target: "[tour='step-data-search']",
    content: 'This another awesome feature!',
    title: 'Data Search',
    placement: 'auto',
    disableBeacon: true,
    page: '/data',
  },
  {
    target: "[tour='step-data-select']",
    content: 'This another awesome feature!',
    title: 'Data Selection Table',
    placement: 'auto',
    disableBeacon: true,
    page: '/data',
  },
  {
    target: "[tour='step-data-selected']",
    content: 'This another awesome feature!',
    title: 'Selected Data Points',
    placement: 'auto',
    disableBeacon: true,
    page: '/data',
  },
  {
    target: "[tour='step-nav-vis']",
    content: 'This another awesome feature!',
    title: 'Visualizations Page',
    placement: 'auto',
    disableBeacon: true,
    page: '/data',
  },
  {
    target: "[tour='step-vis-main']",
    content: 'This another awesome feature!',
    title: 'Visualization',
    placement: 'auto',
    disableBeacon: true,
    page: '/visualizations',
  },
]

function DashboardTour(props) {
  const [runJoyride, setRunJoyride] = useState(false)
  const [step, setStep] = useState(0)
  let navigate = useNavigate()

  const handleCallback = (data) => {
    const { action, index, status, type } = data

    if (index === 0) {
      navigate(steps[0].page)
    }

    if (index + 1 < steps.length && steps[index].page !== steps[index + 1].page) {
      navigate(steps[index + 1].page)
    }

    if ([EVENTS.STEP_AFTER, EVENTS.TARGET_NOT_FOUND].includes(type)) {
      setStep(index + (action === ACTIONS.PREV ? -1 : 1))
    }
    else if ([STATUS.FINISHED, STATUS.SKIPPED].includes(status)) {
      setRunJoyride(false)
      setStep(0)
      navigate('/')
    }

  }

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
