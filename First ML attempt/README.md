# USER MANUAL - HOUSING PRICES
I have created a web application using python which allows users to search for airbnbs and houses as well as customise their own house and get an estimated price. The web application uses the python library Flask to run and users need to login or register to access the web application. I wanted to make a web application like this to improve my knowledge on machine learning(neural networks) as well as improve my profficiency in developing a web application.

Libraries/Software used:
- sqlite3
- Tensorflow (machine learning library)
- Pickle
- Sklearn (machine learning library)
- Pandas (Data analysis library)
- Numpy (makes handling array easier)

# The Workings
### Registration
All users are required to register by inputting a username and a password. The user is then required to enter their password again to make sure they entered what they wanted to enter.

### Sessions
If the user has already registered, they have created a session that is "attatched" to himself/herself. The user can now log in with their username and password and their specific session will be identified. They will then be able to access any homes or Airbnbs they saved.

### Data and SQL
There are two csv files containing all the information on the Airbnbs and the houses. These csv files are loaded into SQLite databases to make it easier to filter out certain records. There are 5 SQLite databases: two for all the Airbnbs and houses, two for the saved Airbnbs and houses and finally one to keep track of the usernames and passwords(hashed) of every user.

### Filtering
The web application allows users to view all the possible houses or, if they want, select certain filters to change the houses that are displayed to ones that they like/can afford etc. This functionality is available for the Airbnbs and the houses, however, the filters are different on each one as the csv files containing the house/airbnb data have diffrent field names.

### Saving
On the same page as the filter, there is an input area where users can input the id of any house/airbnb they like below and save it for later. If users want to view all the houses or airbnbs that they saved, they can click "Added" in the navbar and it will lead them to a page with two tables, one for saved houses and one for saved airbnbs with all of their details.

### Predicting prices
I also implemented a neural network with a tensorflow backend that takes as input 14 features about a house including bedrooms, bathrooms, sqft of living area and sqft lot etc and estimates a minimum price required for a house with these attributes. The user must enter values for all the fields and an estimate will be calculated.

# Improvements
- Could use a better/different ML model to possibly gain a higher accuracy score
- Allow users to change account details
- Increase number of attributes user can enter for an estimate of price

# How to run
This is a flask application so all you need to do is go into the "project" directory in an IDE and in the terminal window run "flask run" then click the url that shows up on the screen. The neural network template and all its weights are already stored in a HDF5 file called "neuralnetwork.h5" and the scaler used in app.py(allows user input to be inputted into the ML model)is stored in "scaler.pkl". You will also have to insert your own API key to get the program to run. Run the command "export API_KEY=(insert API key here)" in the command terminal to insert the API key.

## Video
Here is the link to my video:
https://youtu.be/-zTPylNDjKo





