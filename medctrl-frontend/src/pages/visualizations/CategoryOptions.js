import React from 'react'

// a component for showing and selecting categories for a variable
class CategoryOptions extends React.Component {
  constructor(props) {
    // Receives a key, a list of categories of the selected variable and
    // a function to send the state back to the form.
    super(props)

    // the state contains a list with the names of the selected categories
    this.state = { categoriesSelected: [] }

    // event handlers
    this.handleCategorySelection = this.handleCategorySelection.bind(this)
  }

  // Updating what categories have been selected,
  // then passes it to the general form.
  handleCategorySelection(event) {
    const target = event.target
    const value = target.checked
    const name = target.name

    // If the category has been selected,
    // add it to the list of selected categories.
    // The event is only triggered when the value changes,
    // so we know that it was previously not on the list
    if (value) {
      this.setState(
        (state) => ({
          categoriesSelected: [...state.categoriesSelected, name],
        }),
        () => this.props.onChange(this.state.categoriesSelected)
      )
    } else {
      // remove if the category was previously on the list
      if (this.state.categoriesSelected.includes(name)) {
        this.setState(
          (state) => ({
            categoriesSelected: state.categoriesSelected.filter(
              (el) => el !== name
            ),
          }),
          () => this.props.onChange(this.state.categoriesSelected)
        )
      }
    }
  }

  // create the list of category checkboxes
  renderCategoryOptions() {
    const categories = this.props.categories
    return categories.map((category) => {
      return (
        <React.Fragment key={category}>
          <label>
            <input
              type="checkbox"
              name={category}
              checked={this.state.categoriesSelected.includes(category)}
              onChange={this.handleCategorySelection}
            />
            &nbsp;&nbsp;{category}
          </label>
          <br />
        </React.Fragment>
      )
    })
  }

  // renders checkboxes for each category of the given variable
  render() {
    const categories = this.renderCategoryOptions()
    return <div className="country-options">{categories}</div>
  }
}

export default CategoryOptions
