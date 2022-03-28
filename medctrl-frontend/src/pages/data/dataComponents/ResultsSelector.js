import React from 'react';

function ResultsSelector(){
    return (
        <div className="bottomOfTableHolder">
            <div className="resultsSelector">
                <label>Results per page</label>
                <select name="AmountShown" id="topSelector">
                    <option value="25">25</option>
                    <option value="50">50</option>
                    <option value="100">100</option>
                    <option value="All">All</option>
                </select>
            </div>
        </div>
    );
}

export default ResultsSelector;