import React, {Component} from "react";

class CategoryOptions extends React.Component {
  constructor(props) {
		super(props);
    this.state = {categoriesSelected: []}
		this.handleCategorySelection = this.handleCategorySelection.bind(this);
	}

	  // updating what categories have been selected,
  // then passes it to the general form
  handleCategorySelection(event) {
    const target = event.target;
    const value = target.checked;
    const name = target.name;

    // if the category has been selected,
    // add it to the list of selected categories
    if (value) {
      this.setState(state => ({
        categoriesSelected: [...state.categoriesSelected, name]}),
         () => this.props.onChange(this.state.categoriesSelected));
    }
    else {
      // remove if the category was previously on the list,
      if (this.state.categoriesSelected.includes(name)) {
        this.setState(state => ({
          categoriesSelected: state.categoriesSelected.filter(el => 
            el !== name
          )
        }), () => this.props.onChange(this.state.categoriesSelected));
      }
    }
  }

  // create the list of category checkboxes
  renderCategoryOptions() {
    const categories = this.props.categories;
    return (categories.map(category => {
      return (
        <React.Fragment key={category}>
          <label>
            show {category}
            <input type="checkbox"
                   name={category}
                   checked={this.state.categoriesSelected.includes(category)}
                   onChange={this.handleCategorySelection} />
          </label>
          <br />
        </React.Fragment>       
      );
    }));
  }

	render() {
		const categories = this.renderCategoryOptions();
		return (
			<div style={{backgroundColor: "whitesmoke", 
                     height: "100px", 
                     overflowY: "scroll"}}>
          {categories}
      </div>
		);
	}
} 

export default CategoryOptions