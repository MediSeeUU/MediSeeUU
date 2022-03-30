import React from 'react';
import ReactDOM from 'react-dom';
import { render, fireEvent, waitFor, screen, cleanup, within } from '@testing-library/react';
import Menu from '../Menu';
import DummyData from '../../../json/small_data.json';

test("renders without crashing", () => {
  const root = document.createElement("div");
  ReactDOM.render(<Menu cachedData={DummyData} />, root);
})

test("opens menu after clicking button", () => {
  const { getByText, getByLabelText, queryByLabelText } = render(<Menu cachedData={DummyData} />);
  expect(queryByLabelText(/Menu/i)).not.toBeInTheDocument();
  fireEvent.click(getByText(/Open Menu/i));
  expect(getByLabelText(/Menu/i)).toBeInTheDocument();
})

test("apply button calls update function", () => {
  const update = jest.fn();
  const { getByText } = render(<Menu cachedData={DummyData} updateTable={update} />);
  fireEvent.click(getByText(/Open Menu/i));
  expect(update).not.toHaveBeenCalled();
  fireEvent.click(getByText(/Apply/i));
  expect(update).toHaveBeenCalled();
})

test("clear button calls update function", () => {
  const update = jest.fn();
  const { getByText } = render(<Menu cachedData={DummyData} updateTable={update} />);
  fireEvent.click(getByText(/Open Menu/i));
  expect(update).not.toHaveBeenCalled();
  fireEvent.click(getByText(/Clear/i));
  expect(update).toHaveBeenCalled();
})

test("clear button resets data", () => {
  const update = data => expect(data).toBe(DummyData);
  const { getByText } = render(<Menu cachedData={DummyData} updateTable={update} />);
  fireEvent.click(getByText(/Open Menu/i));
  fireEvent.click(getByText(/Clear/i));
})

test("close button closes menu", () => {
  const { getByText, queryByLabelText } = render(<Menu cachedData={DummyData} />);
  fireEvent.click(getByText(/Open Menu/i));
  fireEvent.click(getByText(/Close/i));
  expect(queryByLabelText(/Menu/i)).not.toBeInTheDocument();
})

test("add filter adds filter item", () => {
  const { getByText, queryAllByRole } = render(<Menu cachedData={DummyData} />);
  fireEvent.click(getByText(/Open Menu/i));
  expect(queryAllByRole("combobox")).toHaveLength(1);
  fireEvent.click(getByText(/Add Filter/i));
  expect(queryAllByRole("combobox")).toHaveLength(2);
})
