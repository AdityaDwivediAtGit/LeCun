# LeCun

Predicting whether a new customer will purchase a car based on a social network ad dataset using K Nearest Neighbour.

## Table of Contents

- [Team Members](#team-members)
- [Problem Statement](#problem-statement)
- [Project Tasks](#project-tasks)
- [Installation](#installation)
- [Usage](#usage)

## Team Members

- Aditya Dwivedi - CDEA
- Swaraj Pal - DPE
- Vikas Shahu - DSE
- Sahil Mankar - DPE

## Problem Statement

The goal of this project is to build a model that can predict whether a new customer will purchase a car based on the social network ad dataset using the K Nearest Neighbors (KNN) algorithm. The dataset consists of information such as age, estimated salary, and whether the customer made a purchase or not. Our objective is to create a classifier that can accurately determine whether a customer will make a purchase based on their age and salary.

## Project Tasks

- Aditya Dwivedi (CDEA):
  - Developed a Flask API to integrate the KNN model with frontend.
  - Created endpoints to handle input and output data for new customers.
  - Connected the API to a SQLite database using the provided CSV file for storing and fetching customer data in realtime.
  - Created all the webpages using html css.
  - Implement additional features, such as variable K and precision of probability.
  - Added login and signup functionality by creating a Users table in the SQLite database.
  - Implemented session management using Flask and added a Logout button.
  - Hosted the website on Google Colab and tested it on multiple devices to ensure proper functionality.
  - Implement two-factor authentication using Discord.

## Installation

To set up the project, follow these steps:

1. Install the required Python libraries: `flask`, `sklearn`, `requests`. You can install them using pip:
   ```
   pip install flask sklearn requests
   ```

2. Run the `csv_to_db.py` script to create a SQLite database named `car_prediction.db`. This script will create the necessary database using the provided CSV file.

3. Create a `webhook_url.txt` file in the same directory as `authenticator.py` and add the webhook URL of your Discord channel as text. This webhook URL will be used to send verification codes during the login process.

## Usage

To use the project, follow these steps:

1. Ensure that the `car_prediction.db` database has been created by running the `csv_to_db.py` script and `webhook_url.txt` file contains your discord webhook link. 

2. Run the `lecun_api.py` script. This will start the Flask API and make the website accessible.

3. Open your web browser and navigate to `127.0.0.1:5001` to access the website. From there, you can input the age and salary of a new customer and obtain the predicted probability of the customer buying a car.

Please note that this `Aditya` branch reflects my individual contributions made for self-learning purposes. The `master` branch contains the final version of the project, which is the result of collaboration among our team members.
