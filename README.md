#Step0 Make sure everything is installed
1.python 3.7
Install the python installer downloaded from https://www.python.org/ftp/python/3.7.7/python-3.7.7-amd64.exe

2.pipenv
Run command below to install it
pip3 install pipenv 


#Step1 Make sure the settings is right
Open config.py 
1.Make sure the user info is valid to login SafeRide of staging environment
2.Make sure both Auth entry point and Vehicle entry point are for staging environment
3.Make sure the telematic_vehicle_id is a vehicle id which connects to a valid device in staging environment

#Step2 Install virtual environment with python version
pipenv install --python 3.7

#Step3 Activate the virtual environment and inside it
pipenv shell

#Step4 Check whether the python version is 3.7.7
python --version

#Step5 Run the test script
python app.py

#Step6 Exit the virtual environment
exit