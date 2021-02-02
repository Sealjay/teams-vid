# Teams Vidd
This web application intends to demonstrate how people could record themselves on the fly, to stay in sync with their teams, wherrer they may be.

## Software Installation

1. Create a Python virtualenv, activate it, and install dependencies:

   - on windows, you may need to use `python` command where there are references to the `python3` command,
   - on macos/linux, you may need to run sudo apt-get install python3-venv first.)

   ```bash
   $ python3 -m venv env
   $ source env/bin/activate
   $ pip3 install -r requirements-dev.txt
   ```

   - if you are using a distribution of conda, you may want to create a new conda environment, rather than use venv `conda create --name teamsvid python=3.9 -y`