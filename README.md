# Interactive dashboard to make data on regulation of medicines openly available

Medicine evaluation boards across Europe evaluate medicines for European market approval. The resulting regulatory reports are published on the European Medicines Agency website. Data on these medicine regulatory procedures is collected by a scraper created in a collaboration between Utrecht University regulatory science researchers and the Dutch Medicines Evaluation Board. Visualization of this data can provide valuable insights toward improving the regulatory trajectory. The MedCtrl Scrum team has developed an interactive dashboard allowing rapid visualization of the collected medicine regulatory data. Intuitive controls combined with sharp-cut visualizations offer regulatory scientists direct insight into trends in medicine market authorizations. Continuously updated with data scraped from thousands of publicly available documents, the dashboard is a highly interactive React application backed by an extensible Django REST backend and MySQL database.

## Description

This repository has two significant branches: *development* and *master*. When a contributor has finished their work, the temporary branch will be pushed into the development branch. Once the development branch is stable, it will be pushed into the master branch. When the master branch is updated, the new changes will be deployed on the environment where the program is installed.

The repository consists of four crucial folders, each folder has a readme with more explanation:
* *medctrl-backend*, with the backend API and database code, including documentation
* *medctrl-frontend*, with the code for all node modules, pages, public files, and mocks, including unit tests and documentation
* *medctrl-scraper*, with the scraper including supplementary files, in this folder a file can be found with an example how to connect the scraper to the backend
* *selenium*, where the system tests are defined and handled

## Copyright statement

This program has been developed by students from the bachelor Computer Science at Utrecht University within the Software Project course.

© Copyright Utrecht University (Department of Information and Computing Sciences)

{py:mod}`api`
