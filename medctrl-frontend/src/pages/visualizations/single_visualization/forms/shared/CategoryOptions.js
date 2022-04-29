import React from 'react'

// a component for showing and selecting categories for a variable
class CategoryOptions extends React.Component {
  constructor(props) {
    // Receives a key, a list of categories of the selected variable and
    // a function to send the state back to the form.
    super(props)

    // the state contains a list with the names of the selected categories
    this.state = { categoriesSelected: this.props.categories, selectAllCategories: true }

    // event handlers
    this.handleAllCategorySelection = this.handleAllCategorySelection.bind(this)
    this.handleCategorySelection = this.handleCategorySelection.bind(this)
  }

  // EVENT HANDLERS:

  // allows user to select all categories
  handleAllCategorySelection(event) {
    if (this.state.selectAllCategories) {
      this.setState(
        {
          selectAllCategories: false,
          categoriesSelected: [],
        },
        () => this.props.onChange(this.state.categoriesSelected)
      )
    } else {
      this.setState(
        {
          selectAllCategories: true,
          categoriesSelected: this.props.categories,
        },
        () => this.props.onChange(this.state.categoriesSelected)
      )
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

  // GENERAL FUNCTIONS:

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
            checked={this.state.selectAllCategories}
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
