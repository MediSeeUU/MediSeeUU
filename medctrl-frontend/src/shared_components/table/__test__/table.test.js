import React from 'react';
import ReactDOM from 'react-dom';
import {render, fireEvent, waitFor, screen, cleanup} from '@testing-library/react'
import Table from '../table';
import DummyData from '../../../json/small_data.json'; // we can replace this with a mock API?

test("renders without crashing", () => {
    const root = document.createElement("div");
    ReactDOM.render(<Table data={DummyData} />, root);
})

test("at least one column in the table", () => {
    const wrapper = render(<Table data={DummyData} />);
    const table = wrapper.getByRole('table');
    const heads = table.getElementsByTagName('thead');
    expect(heads).toHaveLength(1);
    const head = heads[0];
    expect(head.childElementCount).toBeGreaterThan(0);
})

test("at least one row in the table", () => {
    const wrapper = render(<Table data={DummyData} />);
    const table = wrapper.getByRole('table');
    const bodies = table.getElementsByTagName('tbody');
    expect(bodies).toHaveLength(1);
    const body = bodies[0];
    expect(body.childElementCount).toBeGreaterThan(0);
})

test("checkboxes displayed", () => {
    const data = DummyData
    const wrapper = render(<Table data={data}
                                  selectTable={true}
                                  dataToParent={() => {}} />);
    const table = wrapper.getByRole('table');
    const checkboxes = table.getElementsByClassName('checkboxColumn');
    expect(checkboxes).toHaveLength(data.length);
})