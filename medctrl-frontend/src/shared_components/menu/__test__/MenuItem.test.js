import React from 'react';
import ReactDOM from 'react-dom';
import { render, fireEvent, waitFor, screen, cleanup, within } from '@testing-library/react';
import MenuItem from '../MenuItem';

test("renders without crashing", () => {
  const root = document.createElement("div");
  ReactDOM.render(<MenuItem item={ {selected: null, input: [""]} } />, root);
})
