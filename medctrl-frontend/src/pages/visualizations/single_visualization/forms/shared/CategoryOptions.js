import React from 'react'

// a component for showing and selecting categories for a variable
class CategoryOptions extends React.Component {
  constructor(props) {
    // Receives a key, a list of categories of the selected variable and
    // a function to send the state back to the form.
    super(props)

    // the state contains a list with the names of the selected categories
    this.settings = this.props.settings

    // event handlers
    this.handleAllCategorySelection = this.handleAllCategorySelection.bind(this)
    this.handleCategorySelection = this.handleCategorySelection.bind(this)
  }

  // EVENT HANDLERS:

  // allows user to select all categories
  handleAllCategorySelection(event) {
    if (this.settings.selectAllCategories) {
      this.props.onChange(this.settings.categoriesSelected)
    } else {
      this.props.onChange(this.props.categories)
    }
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
      this.props.onChange([...this.settings.categoriesSelected, name])
    } else {
      // remove if the category was previously on the list
      if (this.settings.categoriesSelected.includes(name)) {
        this.props.onChange(
          this.settings.categoriesSelected.filter((el) => el !== name)
        )
      }
    }
  }

  // GENERAL FUNCTIONS:

  // create the list of category checkboxes
  renderCategoryOptions() {
    this.settings = this.props.settings
    const categories = this.props.categories
    return categories.map((category) => {
      return (
        <React.Fragment key={category}>
          <label>
            <input
              type="checkbox"
              name={category}
              checked={this.settings.categoriesSelected.includes(category)}
              onChange={this.handleCategorySelection}
            />
            &nbsp;&nbsp;{category}
          </label>
        </React.Fragment>
      )
    })
  }

  // RENDERER:

  // renders checkboxes for each category of the given variable
  render() {
    const categories = this.renderCategoryOptions()
    return (
      <React.Fragment>
        <br />
        <label>
          <input
            type="checkbox"
            name="selectAllCategories"
            checked={this.settings.selectAllCategories}
            onChange={this.handleAllCategorySelection}
          />
          &nbsp;&nbsp;Select all categories
        </label>
        <div className="country-options">{categories}</div>
      </React.Fragment>
    )
  }
}

export default CategoryOptions
