// A mock necessary for testing, 
// in particular when a chart is drawn.
class ResizeObserver {
  observe() {
    // do nothing
  }
  unobserve() {
    // do nothing
  }
}

window.ResizeObserver = ResizeObserver
export default ResizeObserver
