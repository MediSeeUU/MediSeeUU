// function based component, represents a link to an external
// address, the link is opened in a new tab, and via the class,
// this link can have a custom appearance
function CustomLink(props) {
  return (
    <a
      href={props.dest}
      target="_blank"
      rel="noreferrer"
      className={props.className}
    >
      <i className={props.image} />
      <span>{props.name}</span>
    </a>
  )
}

export default CustomLink