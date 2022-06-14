# med-ctrl frontend

# Table of contents

* [General Information](#project-information)
* [Setup](#setup)
* [Used Technologies](#used-technolgies)
* [Structure Overview](#structure-overview)

# General Information

This software development project is a collaboration between Utrecht University (UU) and the Dutch Medicines Evaluation Board (MEB), also known as College ter Beoordeling van Geneesmiddelen (CBG). The goal of the project is to make data on medicines regulation and marketing approval openly available. Currently, data on medicines regulation in Europe and beyond is often dispersed across multiple sources. This includes for instance relevant data on the regulatory approval of medicines for rare diseases, innovative gene- and cell-based therapies and approvals of vaccines to treat Covid-19. The project aims to use data published by the European Medicines Agency (EMA), the United States Food and Drug Administration (US FDA) and the European Commission (EC) to create an interactive dashboard to allow intuitive visualization and make quantitative analyses of these data easier and more consistent.

# Setup

1. Download and install the node package manager installer using the following link: https://nodejs.org/en/download/. During the install process, the default settings will be sufficient.

2. If you do not use a compatible IDE already and wish to continue developing the software, you can download and open Visual Studio Code editor. (You can download VSCode using the following via the website: https://code.visualstudio.com/).

3. Create a folder and clone the repository there, either using the command line, terminal, GitHub Desktop or your compatible IDE.

4. Open a terminal or powershell window, navigate to the folder where you cloned the repository (or using the integrated terminal functionality in your IDE) and then navigate to the medctrl-frontend directory.

5. In the medctrl-frontend directory, run `$ npm install` to install all the required dependencies.

6. If you wish to use backend functionality in the frontend without running a local version of the med-ctrl backend, add a `.env.local` file in the medctrl-frontend directory with the following contents: `REACT_APP_RDR_DEV=true`.

7. Finally, use `$ npm start` to start the application, you can now visit the local version at `localhost:3000`.

# Used Technolgies

This dasboard is built using the following technolgies:
* ReactJS framework 17.0.2
* ApexCharts library 3.33.2 (Used for the graphs and charts on the visualization page)
* Boxicons 2.1.2 (Used for all the icons on the dashboard)

# Structure Overview

In the root directory of this project, config files can be found for git, eslint and prettier, as well as the npm dependency information for this project. The `public` directory contains the base html file for the dashboard and the dashboard logo and favicon.

All of the source files are containted in the `src` directory. Mos of the source files are subdived into sub directories, which will be covered below. The files which reside in the `src` directory itself are files critical for the dashabord like `index.js` and `index.css` which provide an entry point for the application.  

## `core`
This directory contains all of the components which are always present on the dashboard (for example the header, footer and navigation), as well as the logic for logging in and out users. This is also the directory where the `App` component resides, which represents the main component and the whole dashboard.

## `image`
This directory contains all of the images and logos used in this project, ranging from UU and MED logos to the dashboard logo.

## `json`
This directory contains all the json files with data used for mocking and testing. This data is not used by the production version of the dashboard.

## `mocks`
This directory contains all of the javascript files and logic used for the mocking of specific functionalities during unit testing.

## `pages`
For each of the different pages, a sub directory holds all of the specific files and folder required for that page to correclty and fully function. Each page consists of one 'top level' component which describes the whole page, and can be build using multiple smaller components. All of these sub components are usually stored in a folder `components` or a named folder.

### `pages/account`
The account page shows a logged in user all of the data selections the user has made in the past and allows for the creation of new selections and the deletion of existing selections.

### `pages/data`
_To do_

### `pages/detailed_info`
The detailed info page shows all the available information regarding one single medicine. The page is devided in four main parts. First, the medicine details, which are rendered using the `Detail` and `DetailGroup` components. Second, the time line visual, which is created using the `TimeLineElement` and `TimeLine` components. Third, a list of all the selected procedures (selection is handled by the `ProcSelectModal` component), which are rendered using the `Procedure` and `ProcedureDetail` components. Finally, a few useful links are included at the end (using the `CustomLink` component). All of the componens mentioned above are located in the `./components/` directory.

### `pages/error`
The error page is the default page which is displayed when an invalid URL is requested.

### `pages/home`
The home page is a simple page, which gives a short overview of the dashboards functionality, provides a fast search and dashboard walkthrough functionality.

### `pages/info`
The home page is a simple page, which gives additional information about this dashboard and the orginations behind the development of this dashboard.

### `pages/visualizations`
_To do_

## `shared`
The `shared` directory contains all of the components that are used by multiple pages on the dashboard, these include:
* The data contexts and provider
* The search functionality components
* A dropdown variable selection menu component
* A custom modal component 

# Copyright Statement

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.

© Copyright Utrecht University (Department of Information and Computing Sciences)