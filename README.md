# Fight Predictor App

This is a web app used to predict the results of UFC fights. The front end uses the [React.js web framework](https://reactjs.org/), and the back end uses [Fast API web framework](https://fastapi.tiangolo.com/) along with the [Uvicorn server implementation](https://www.uvicorn.org/). 

### Prediction Model

The data used to train the model is found at http://www.ufcstats.com/statistics/events/completed and was scraped using the [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) python library. Different fighter skills were calculated using the ELO rating system, and rating values were fed as input to a Logistic Regression Classifier. This classifier achieved an accuracy of 59% when predicting the result of a fight, only having access to data available at the time of the fight. Note, there is still room for improvement, and it is not recommended to place bets on fights based on this predictor.

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

## Web page screenshots

![plot1](https://github.com/gussily/fight_predictor_app/blob/master/img/fp_1.PNG?raw=true)

![plot2](https://github.com/gussily/fight_predictor_app/blob/master/img/fp_2.PNG?raw=true)

