# Table of Contents:

- [Requirements](#-Requirements)
        - [Packages](##-Packages)
        - [Additional Software](##-Additional-Software)
- [Installation Guide](#-Installation-Guide)
        -[1. Clone the repository](##-1.-Clone-the-repository)
        - [2. Setting up your virtual environment](##-2.-Setting-up-your-virtual-environment)
        - [3. Installing the packages](##-3.-Installing-the-packages)
        - [4. Installing PostgreSQL](##-4.-Installing-PostgreSQL)
        - [5. Setting up the database](##-5.-Setting-up-the-database)
        - [6. Configuring your environment variables](##-6.-Configuring-your-environment-variables)
        - [7. Populating the database](##-7.-Populating-the-database)
        - [8. Starting the Flask server](##-8.-Starting-the-Flask-server)

# Requirements
- Python3
- Windows or MacOS
- A potato PC

## Packages
The following packages required for this application to work and have been used to create the framework for managing routes and handling server responses:

| Name | Description | Link |
|------|-------------|------|
| Flask | A web application framework for creating RESTful APIs. | https://flask.palletsprojects.com/en/stable/ |
| SQL Alchemy | A Python SQL toolkit and Object Relational Mapper. Used to access SQL commands using Python. | https://www.sqlalchemy.org/ |
| Marshmallow | Object Relational Mapper used to convert objects and data into Python data types. | https://marshmallow.readthedocs.io/en/latest/# |
| Psycopg2 | PostgreSQL adapter for Python. Used mainly for its error handling. | https://www.psycopg.org/ |
| dotenv | For loading in environment variables and settings found in key value pairs in .env files | https://github.com/theskumar/python-dotenv |
| pip | Python package installer | https://github.com/pypa/pip |

## Additional Software

| Name | Description | Link |
|------|-------------|------|
| PostgreSQL | Open source object relational database system | https://www.postgresql.org/ |


# Installation Guide
## 1. Clone the repository

1. Open the command line terminal
2. Clone the github repository

        git clone https://github.com/macfluffy/Assessment-3.git

3. Open the project folder

        cd Assessment-3

## 2. Setting up your virtual environment

It is recommend that you setup your virtual environment in the project folder first before installing the packages.

1. Set up the virtual environment inside the project folder

        python3 -m venv .venv

2. Open up your virtual environment

        source .venv/bin/activate

## 3. Installing the packages

This step requires you to be in your virtual environment (see 1. Setting up your environment).

1. Install the latest version of the Python package manager

        python -m pip install --upgrade pip

2. Install the packages using the requirements list

        pip install -r requirements.txt


## 4. Installing PostgreSQL
This is the database that houses all of our data.

1. Install PostgreSQL

<b>For MacOS Systems:</b>

        brew install postgresql


<b>For Windows / Ubuntu systems: </b>

        sudo apt update
        sudo apt install postgresql

## 5. Setting up the database

1. Open PostgreSQL

<b>For MacOS Systems:</b>

        brew services start postgresql

<b>For Windows / Ubuntu systems: </b>

        sudo -u postgres psql

2. Create the database owner. 

> ⚠️Replace the everything inside and including the [ ] brackets

        CREATE USER [insert owner username] WITH PASSWORD [insert password];

3. Create the database

> ⚠️Replace the everything inside and including the [ ] brackets. Make sure to note your password as this will be used to setup your environment

        CREATE DATABASE [insert database name] OWNER [insert owner username];

4. Exit the PostgreSQL database by entering `\q`

## 6. Configuring your environment variables

1. Create a `.env` file inside your project folder
2. Open the `.envexample` inside the project folder
3. Copy the following line into the `.env` file from the `.envexample` file:

        DATABASE_URI = database+driver://username:password@server:port/databasename

4. Replace the following values in the variable `DATABASE_URI` in your `.env` file:

| Before | After |
|--------|-------|
| `database` | `postgresql` |
| `driver` | `psycopg2` |
| `username` | <i>Insert the database owner's username</i> |
| `password` | <i>Insert the password for the database owner</i> |
| `server` | `localhost` |
| `port` | `5432` <i>(This is the default port for PostgreSQL)</i> |
| `databasename` | <i>Insert the name of the database entered in PostgreSQL</i> |

5. Save the changes

## 7. Populating the database
> ⚠️The following steps require you to be in your virtual environment

1. In the command line enter the following to create the tables:

        flask db create

2. Enter the following to seed the tables:

        flask db seed

## 8. Starting the Flask server

1. In the command line enter

        flask run