import React from 'react';
import ReactDOM from 'react-dom';
import { render, fireEvent, waitFor, screen, cleanup, within } from '@testing-library/react'
import Table from '../table';
import DummyData from '../../../json/small_data.json'; // we can replace this with a mock API?

test("renders without crashing", () => {
  const root = document.createElement("div");
  ReactDOM.render(<Table data={DummyData} />, root);
})

test("expected amount of rows in the table", () => {
  const wrapper = render(<Table data={DummyData} />);
  const table = wrapper.getByRole('table');
  const rows = within(table).getAllByRole('row');
  expect(rows).toHaveLength(DummyData.length + 1);
})

test("expected amount of headers in the table", () => {
  const wrapper = render(<Table data={DummyData} />);
  const table = wrapper.getByRole('table');
  const rows = within(table).getAllByRole('row');
  const headers = within(rows[0]).queryAllByRole('columnheader');
  if (DummyData.length > 0) {
    expect(headers).toHaveLength(Object.keys(DummyData[0]).length);
  }
  else {
    expect(headers).toHaveLength(0);
  }
})
