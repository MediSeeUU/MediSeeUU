import React from 'react';
import '../shared.css'

function Menu() {
    return (
        <div>
            <label>Active table settings</label>
            <button className="tableButtons"><i className='bx bx-cog filter-Icon'></i>Filter & Sort</button>
            <hr></hr>
        </div>
    );
}

export default Menu;