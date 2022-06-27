// This program has been developed by students from the bachelor Computer Science at
// Utrecht University within the Software Project course.
// © Copyright Utrecht University (Department of Information and Computing Sciences)

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
