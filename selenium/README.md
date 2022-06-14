
# Selenium
#### Selenium is an automated testing framework used to validate web applications across different browsers and platforms. Selenium is mostly used for writing automated test cases, especially integration and system tests.
## About

This project is initialized to automatically test the application on both 
integration and system level. 
This was part of the quality assurance of the project to minimize the chances of 
introducing bugs in the functionalities of the application. 
The project contains a variety of test cases that cover individual pages, as well as 
the interaction of multiple pages. Furthermore, the project adheres the Page Object Model 
(POM) to make the tests more readable and allow reusable code that can be shared across 
multiple test cases.

## Installation

The tests are written in `Python 3.10` together with the `selenium` and 
`webdriver_manager` packages.
As the `selenium` package itself does not provide a 
testing framework, the `unittest` module was used to write test cases. 
The WebDriver implementation used is Chrome. Since the project was developed on a Windows 
machine, we will be providing a guide to install it on a similar machine.

To install all the necessary packages at once, the following command should be run:

```bash
  pip install -r requirements.txt
```

Simply run all tests by the following command:

```bash
  py TestRunner.py
```

## Contents

`TestRunner.py`: Script to run all the test cases located in the `Tests` directory.

`WebDriverSetup.py`: Sets up the WebDriver to perform the tests on a separate browser.

`Tests`: This directory contains all the test cases divided over multiple files.

`DataTests`: This directory contains test cases that manipulate data. The reason for keeping this separate of the other test cases is that you may have to setup the backend locally if you do not want the data on the actual server to be touched.

`Pages`: This directory contains for each page a seperate file with methods to interact in the browser.
- `shared`: This directory contains shared component files of the pages.

`Resources`: This directory contains all resource definitions of the application.
- `locators.py`: Contains all the locators of the application to locate the elements of the pages.


## Copyright Statement

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.

© Copyright Utrecht University (Department of Information and Computing Sciences)