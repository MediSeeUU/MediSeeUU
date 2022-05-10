import Joyride, { ACTIONS, EVENTS, STATUS } from 'react-joyride'
import { useState } from 'react'

const steps = [
  {
    target: "[tour='step-one']",
    content: 'This is my awesome feature!',
    disableBeacon: true,
  },
  {
    target: "[tour='step-two']",
    content: 'This another awesome feature!',
    page: '/',
  },
]

function DashboardTour() {
  const [runJoyride, setRunJoyride] = useState(false)
  const [step, setStep] = useState(0)

  const handleCallback = (data) => {
    const { action, index, status, type } = data

    if ([EVENTS.STEP_AFTER, EVENTS.TARGET_NOT_FOUND].includes(type)) {
      setStep(index + (action === ACTIONS.PREV ? -1 : 1))
    } else if ([STATUS.FINISHED, STATUS.SKIPPED].includes(status)) {
      setRunJoyride(false)
      setStep(0)
    }
  }

  return (
    <div tour="step-one" className="med-content-container step-one">
      <Joyride
        steps={steps}
        stepIndex={step}
        run={runJoyride}
        callback={handleCallback}
        showProgress={false}
        continuous={true}
        showSkipButton={true}
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
          },
        }}
      />
      <h1>Dashboard Tour</h1>
      <hr className="med-top-separator" />

      <button
        className="med-primary-solid med-bx-button"
        onClick={() => setRunJoyride(true)}
        style={{ float: 'right' }}
      >
        <i className="bx bx-code-alt search-Icon" />
        Start Tour
      </button>

      <p style={{ width: 'calc(100% - 180px)' }}>
        To explore all the features of this dashboard, take a guided tour around
        the website by clicking the button. This tour will not take long and
        familiarize you with all the core functionalities that this dashboard
        has to offer. You can end the tour at any time by clicking 'end'. When
        you reach the end of the tour, the tour will automaticly finish.
      </p>
    </div>
  )
}

export default DashboardTour
