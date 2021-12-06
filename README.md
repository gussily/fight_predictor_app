# Fight Predictor App

This is a web app used to predict the results of UFC fights.

## Back end Setup

After cloning/unpacking the source code, the first step is to set up our virtual environment. 

```console
$ cd backend
$ python3.9 -m venv venv
$ source venv/bin/activate
$ export PYTHONPATH=$PWD
```

Next we install the necessary requirements. This may take a few minutes.
```console
(venv)$ pip install -r requirements.txt
```

Now we run our backend. This will run on your localhost in port 8000.

```console
(venv)$ python main.py
```

## Front end Setup

First, in a new terminal, let's navigate to the front end folder and setup our node packages. Make sure you have node an npm downloaded on your machine. Instructions can be found here: https://docs.npmjs.com/downloading-and-installing-node-js-and-npm

```console
$ cd frontend
$ npm install
```

Now, to launch our app, simply run the following. This should open a webpage on port 3000

```console
$ npm start
```
