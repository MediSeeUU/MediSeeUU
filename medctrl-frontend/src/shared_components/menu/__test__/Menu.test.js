import React from "react";
import ReactDOM from "react-dom";
import { render, fireEvent, waitFor, screen, cleanup, within } from "@testing-library/react";
import Menu from "../Menu";
import DummyData from "../../../json/data.json";

test("renders without crashing", () => {
  const root = document.createElement("div");
  ReactDOM.render(<Menu cachedData={DummyData} />, root);
});

test("opens menu after clicking button", () => {
  const { getByText, getByLabelText, queryByLabelText } = render(
    <Menu cachedData={DummyData} />
  );
  expect(queryByLabelText(/Menu/i)).not.toBeInTheDocument();
  fireEvent.click(getByText(/Open Menu/i));
  expect(getByLabelText(/Menu/i)).toBeInTheDocument();
});

test("apply button calls update function", () => {
  const update = jest.fn();
  const { getByText } = render(
    <Menu cachedData={DummyData} updateTable={update} />
  );
  fireEvent.click(getByText(/Open Menu/i));
  expect(update).not.toHaveBeenCalled();
  fireEvent.click(getByText(/Apply/i));
  expect(update).toHaveBeenCalled();
});

test("clear button calls update function", () => {
  const update = jest.fn();
  const { getByText } = render(
    <Menu cachedData={DummyData} updateTable={update} />
  );
  fireEvent.click(getByText(/Open Menu/i));
  expect(update).not.toHaveBeenCalled();
  fireEvent.click(getByText(/Clear/i));
  expect(update).toHaveBeenCalled();
});

test("clear button resets data", () => {
  const update = (data) => expect(data).toBe(DummyData);
  const { getByText } = render(
    <Menu cachedData={DummyData} updateTable={update} />
  );
  fireEvent.click(getByText(/Open Menu/i));
  fireEvent.click(getByText(/Clear/i));
});

test("close button closes menu", () => {
  const { getByText, queryByLabelText } = render(
    <Menu cachedData={DummyData} />
  );
  fireEvent.click(getByText(/Open Menu/i));
  fireEvent.click(getByText(/Close/i));
  expect(queryByLabelText(/Menu/i)).not.toBeInTheDocument();
});

test("add filter adds filter item", () => {
  const { getByText, queryAllByRole } = render(<Menu cachedData={DummyData} />);
  fireEvent.click(getByText(/Open Menu/i));
  expect(queryAllByRole("combobox")).toHaveLength(1);
  fireEvent.click(getByText(/Add Filter/i));
  expect(queryAllByRole("combobox")).toHaveLength(2);
});

test("single filter applied correctly", () => {
  const update = (data) => {
    data.forEach((element) => {
      expect(element.ApplicationNo.toString()).toContain("8");
    });
  };
  const { getByText, getByRole } = render(
    <Menu cachedData={DummyData} updateTable={update} />
  );
  fireEvent.click(getByText(/Open Menu/i));
  const select = getByRole("combobox");
  fireEvent.change(select, { target: { value: "ApplicationNo" } });
  const textBox = getByRole("textbox");
  fireEvent.change(textBox, { target: { value: "8" } });
  fireEvent.focusOut(textBox);
  fireEvent.click(getByText(/Apply/i));
});

/*
test("two filters applied correctly", () => {
  const update = (data) => {
    data.forEach((element) => {
      expect(element.ApplicationNo.toString()).toContain("7");
      expect(element.DecisionYear.toString()).toBe("2001");
    });
  };
  const { getByText, getAllByRole } = render(
    <Menu cachedData={DummyData} updateTable={update} />
  );
  fireEvent.click(getByText(/Open Menu/i));
  fireEvent.click(getByText(/Add Filter/i));
  const selects = getAllByRole("combobox");
  const textBoxes = getAllByRole("textbox");
  fireEvent.change(selects[0], { target: { value: "ApplicationNo" } });
  fireEvent.change(textBoxes[0], { target: { value: "7" } });
  fireEvent.focusOut(textBoxes[0]);
  fireEvent.change(selects[1], { target: { value: "DecisionYear" } });
  fireEvent.change(textBoxes[1], { target: { value: "2001" } });
  fireEvent.focusOut(textBoxes[1]);
  fireEvent.click(getByText(/Apply/i));
});
*/
