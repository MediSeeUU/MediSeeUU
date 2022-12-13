import React from 'react'
import './ToggleButtons.css'
import './Button.css'

class ToggleButtons extends React.Component{
    constructor(){
      super();
      this.state = {
        buttonId: 1
      }
      this.setOrangeButton = this.setActiveButton.bind(this);
    }
    setActiveButton(id){
      this.setState({buttonId: id});
    }

    buttonString = "med-primary-solid med-bx-button-special med-selector-button" 

    render(){

        const { clickFunction1, clickFunction2 } = this.props

        return (
            <div
                style={{
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                }}>
                <input
                    className={this.state.buttonId === 1 ? "button active " + this.buttonString : "button " + this.buttonString}
                    onClick={() => {
                        clickFunction1();
                        this.setActiveButton(1)
                    }}
                    value="Human Medicinal Products"
                    type="button" />
                <input
                    className={this.state.buttonId === 2 ? "button active " + this.buttonString : "button " + this.buttonString}
                    onClick={() => {
                        clickFunction2();
                        this.setActiveButton(2)
                    }}
                    value="Orphan Designations"
                    type="button" />

            </div>
        )
    }
}

export default ToggleButtons