# Teams Vid

> **⚠️ ARCHIVED**: This repository is archived and no longer maintained. Azure Media Services Video Indexer, which this project relied upon, has been retired by Microsoft.

> **🏆 Hackathon Winner**: This project was a winning entry in the COVID-19 hackathon. [View on Devpost](https://devpost.com/software/teamsvid-covid-connection)

This web application intends to demonstrate how people could record themselves on the fly, to stay in sync with their teams, wherever they may be.

## Software Installation

1. Create a separate Python environment for your installation, and activate it. You have two options:

   a. *Use a Conda distribution*

      If you are using a distribution of conda, you may want to create a new conda environment, rather than use venv:

      `conda create --name teamsvid python=3.9 -y`

   b. *Use a Python virtual environment*

      On Windows, you may need to use `python` command where there are references to the `python3` command.

      On linux, you may need to run `sudo apt-get install python3-venv` first.

   ```bash
   $ python3 -m venv env
   $ source env/bin/activate
   $ pip3 install -r requirements-dev.txt
   ```


2. Install the required dependencies in your new Python environment.

   ```bash
   $ pip3 install -r requirements-dev.txt
   ```
   The `requirements.txt` file can be used alone if you don't intend to develop further.
3. Create an Azure Blob storage resource and update a `.env` file from template if developing locally.
4. [Create an Azure App Service with a Python Linux plan](https://docs.microsoft.com/en-us/azure/developer/python/tutorial-deploy-app-service-on-linux-03), and deploy the `webapp` folder.
5. [Set the *Azure Startup Command* on your Azure App Service](https://docs.microsoft.com/en-us/azure/app-service/configure-language-python#customize-startup-command) to `gunicorn -c gunicorn_config.py app:app`.
6. [Set the Azure App Service settings](https://docs.microsoft.com/en-us/azure/app-service/configure-common#configure-app-settings) for your blob storage, matching the names you used on your local `.env` file, or [use the extension in VS code](https://docs.microsoft.com/en-us/azure/developer/python/tutorial-deploy-app-service-on-linux-03#optional-upload-an-environment-variable-definitions-file).

# Credit
* Bootstrap - Utilising [Themestr](https://www.themestr.app) tool for a quick way to set up bootstrap.
* Favicon generated using the following graphics from Twitter Twemoji:
   - Graphics Title: 1f427.svg
   - Graphics Author: Copyright 2020 Twitter, Inc and other contributors (https://github.com/twitter/twemoji)
   - Graphics Source: https://github.com/twitter/twemoji/blob/master/assets/svg/1f427.svg
   - Graphics License: CC-BY 4.0 (https://creativecommons.org/licenses/by/4.0/)
