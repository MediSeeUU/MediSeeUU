import React from 'react'

// a component for showing and selecting categories for a variable
class CategoryOptions extends React.Component {
  constructor(props) {
    // Receives a key, a list of categories of the selected variable and
    // a function to send the state back to the form.
    super(props)

    // the state contains a list with the names of the selected categories
    this.state = { categoriesSelected: this.props.categoriesSelected }

    // event handlers
    this.handleAllCategorySelection = this.handleAllCategorySelection.bind(this)
    this.handleCategorySelection = this.handleCategorySelection.bind(this)
  }

  // EVENT HANDLERS:

  // allows user to deselect/select all categories
  handleAllCategorySelection(event) {
    if (this.state.categoriesSelected.length === this.props.categories.length) {
      this.setState({ categoriesSelected: [] }, () => {
        this.props.onChange(this.state.categoriesSelected)
      })
    } else {
      this.setState({ categoriesSelected: this.props.categories }, () => {
        this.props.onChange(this.props.categories)
      })
    }
  }

  // Updating what categories have been selected,
  // then passes it to the general form.
  handleCategorySelection(event) {
    const target = event.target
    const value = target.checked
    const name = target.name

    if (value) {
      // add category to the list
      const newCategories = [...this.state.categoriesSelected, name]
      this.setState({ categoriesSelected: newCategories }, () => {
        this.props.onChange(newCategories)
      })
    } else {
      // remove if the category was previously on the list
      if (this.state.categoriesSelected.includes(name)) {
        const newCategories = this.state.categoriesSelected.filter(
          (el) => el !== name
        )
        this.setState({ categoriesSelected: newCategories }, () => {
          this.props.onChange(this.state.categoriesSelected)
        })
      }
    }
  }

  // GENERAL FUNCTIONS:

  // create the list of category checkboxes
  renderCategoryOptions() {
    return this.props.categories.map((category) => {
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
            checked={this.state.categoriesSelected.length === categories.length}
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
