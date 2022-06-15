// This program has been developed by students from the bachelor Computer Science at
// Utrecht University within the Software Project course.
// © Copyright Utrecht University (Department of Information and Computing Sciences)
import React from 'react'

// a component for showing and selecting categories for a variable
function CategoryOptions(props) {
  // the settings contains a list with the names of the selected categories
  let settings = props.categoriesSelected

  // event handlers
  const handleAllCategorySelection = handleAllCategorySelectionFunc.bind(this)
  const handleCategorySelection = handleCategorySelectionFunc.bind(this)

  // EVENT HANDLERS:

  // allows user to deselect/select all categories
  function handleAllCategorySelectionFunc(event) {
    // Check if the amount of categories currently selected
    // equals the total amount of categories available.
    const newCategoriesSelected =
      settings.length === props.categories.length ? [] : props.categories
    settings = newCategoriesSelected
    props.onChange({
      target: {
        type: 'array',
        value: newCategoriesSelected,
        name: 'categoriesSelected' + props.dimension,
      },
    })
  }

  // Updating what categories have been selected,
  // then passes it to the general form.
  function handleCategorySelectionFunc(event) {
    const target = event.target
    const value = target.checked
    const name = target.name

    let newCategoriesSelected
    if (value) {
      // Adds the selected category to the list.
      // A filter was added because the data type of name is returned as a string instead of its original datatype,
      // but it is not a very elegant solution...
      const addition = props.categories.filter(
        (el) => String(el) === String(name)
      )[0]
      newCategoriesSelected = [...settings, addition]
    } else {
      // removes the selected category of the list
      newCategoriesSelected = settings.filter(
        (el) => String(el) !== String(name)
      )
    }
    settings = newCategoriesSelected

    props.onChange({
      target: {
        type: 'array',
        value: newCategoriesSelected,
        name: 'categoriesSelected' + props.dimension,
      },
    })
  }

  // GENERAL FUNCTIONS:

  // create the list of category checkboxes
  function renderCategoryOptions() {
    // props.categories is already sorted
    return props.categories.map((category) => {
      return (
        <React.Fragment key={category}>
          <label>
            <input
              type="checkbox"
              name={category}
              checked={settings.includes(category)}
              onChange={handleCategorySelection}
            />
            &nbsp;&nbsp;{category}
          </label>
        </React.Fragment>
      )
    })
  }

  // RENDERER:

  return (
    <>
      <br />
      <b>{props.dimension}-axis</b>
      <br />
      <label>
        <input
          type="checkbox"
          name="selectAllCategories"
          checked={settings.length === props.categories.length}
          onChange={handleAllCategorySelection}
        />
        &nbsp;&nbsp;Select all categories
      </label>
      <div className="country-options">{renderCategoryOptions()}</div>
    </>
  )
}

export default CategoryOptions
