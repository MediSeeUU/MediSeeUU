// This program has been developed by students from the bachelor Computer Science at
// Utrecht University within the Software Project course.
// © Copyright Utrecht University (Department of Information and Computing Sciences)

// Function based component, represents a link to an external
// address, the link is opened in a new tab, and via the class,
// this link can have a custom appearance
function CustomLink(props) {
  let dest = props.dest
  let className = props.className
  if (!props.dest || props.dest === 'NA') {
    className += ' disabled'
    dest = '#'
  }
  return (
    <a href={dest} target="_blank" rel="noreferrer" className={className}>
      <i className={props.image} />
      <span>{props.name}</span>
    </a>
  )
}

export default CustomLink
