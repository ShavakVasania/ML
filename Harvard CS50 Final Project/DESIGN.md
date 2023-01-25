# DESIGN - HOUSING PRICES
# Opening
I have always been amazed by the capabilites of AI and its applications and was shocked when I realised how much we use AI in our daily life. I saw this project as a way to start my journey in AI in python and it is this which inspired me to create this web application which makes use of a simple neural network to predict house prices along with other functionality.

# Back-end

## Data and SQL
The first step that I needed to take to kick off my project was to find actual data on houses and Airbnbs which I could use to create my web application. There is a well known machine learning website called Kaggle which has countless different datasets in many different areas and it is there where I got my data: Airbnbprices.csv and houseprices.csv.

I then needed to create a database system with this data which would allow the user to query into the database and find specific records. I did this using SQLite and here are the tables I created as well as their descriptions:

- users : this was where I held user information such as their username and their hashed password as well as their user_id.

- airbnb : this is where I held all the data in the csv file "Airbnbprice". Consisted of many listed Airbnbs that were available for rent and details about the Airbnb such as its location, the name of the owner, price per night etc

- houses : this is where I held all the data in the csv file "houseprices". Consists of many houses and the details about the house such as its buy price, the number of bedrooms, square footage etc

- selectAir : this is where I held any airbnbs that the user had saved so I can display the saved airbnbs to the user in the "log" route

- selectHouse: this is where I held any houses that the user had saved so I can display the saved houses to the user in the "log" route

These tables were quite easy to create as there is functionality within sqlite which makes importing csv files into the database very easy. For the select... tables, I simply had to get the id of the specified house/Airbnb from the user and copy that house/Airbnb and its details from the houses/airbnb table into the select... table. I also couldn't use the same table for the selected houses and Airbnbs as obviously they do not have the same field names and detail categories.

## Machine learning
For the prediction/customising part of my web application, I came up with two approaches to the problem which I will describe her:
- Multi-linear regression model : This model is the simpler of the two model and its just an extension to a single lienar regression model(line of best fit) as now I am providing multiple input values for a single output value. I first split my dataset into the target data(price) and the input data(the values I want to use to predict the target value). I then had to split the data into training and testing data using the funciton train_test_split in order to make sure the program is not overfitting and it is actually correctly(to a certain extent)predicting the house prices. I then fit the data to a Linear regression model and started making prediciton using the model. While this model was quite easy to create, the downside was that the accuracy with the test_data was not very high(about 64% accuracy) which led me to try and create a new model

- <p>Simple neural network model : This model was much tougher for me to implement as before this project I had only seen mentions of neural networks on the internet but I had no idea how they worked and what they actually did. After lots of research on what neural networks actually were and how they could be used in machine learning, I attempted to create my own one to predict house prices.</p> <p>The process started quite similarly to the linear regression model, I split my data into the target data and the input data. I then split the data into training data(to train the model), validating data(to optimize the model) and testing data(to provide a estimate of how effective the model is). The next step was one that took me a while to understand as it seemed quite unusual on why I had to do this step to make my NN effective. This step is the scaling of the data using a StandardScaler in order to kind of "squish" the data into a small range to make the training step easier. To understand why this makes it easier you have to understand how the optimizing part works in the NN. The optimizer, in simplest terms, randomly allocates values to "weights" within the model and keeps changing the value until the loss is minimized. If the data was not scaled, the weights would be changing very drastically, due to the large range in values, which woud make the learning process unstable and thus make the model less effective.</p> <p>The final step was to create the template of the nerual network(input layer, hidden layers, output layers and their activation functions) and finally fit the data to the NN(assigning a loss function of "mean_squared error" so the optimizer can figure out the weight value that results in the lowest loss). I was then able to test my model and I got a accuracy score of 74% which isn't very high but was better than my previous model.</p>




## Flask
The main file "app.py" contains routes which provide the functionality of my web application. Here is a description of each one:

- "/" - the GET request method simply displays to the user their saved houses and airbnbs in two seperate tables. The POST request method allows users to remove specific houses or airbnb from their saved houses and airbnbs

- "/customise" - this route takes input from the user on the details of a house and it runs the inputs through my trained neural network to create an estimated price which is then displayed to the user

- "/selectAirbnb" - this route takes the id of an airbnb as input from the user and copies that specific airbnb(and all its details) into the "selectAir" databse to be displayed in the "/" route

- "/selectHouse" - this route takes the id of a house as input from the user and copies that specific house(and all its details) into the "selectHouse" database to be displayed in the "/" route

- "/airbnb" - the POST request method takes maximum price, number of nights, neighbourhood and room type as input from the user and filters the airbnbs that are displayed to the user depending on these parameters. The GET request method simply displays the first 30 airbnbs to the user with no specifications on which airbnbs are displayed.

- "/houses" - the POST request method takes price, bedrooms, waterfront and number of views as input from the user and filters the houses that are displayed to the user depending on these parameters.  The GET request method simply displays the first 30 houses to the user with no specifications on which houses are displayed.

- "/login" - Takes a username and password from the user as input and checks the entered values against the "users" table. If there is a match for the username and the hashed password then access is given.

- "/logout" - ends the current users session allowing another user to login or register

- "/register" - takes a username, a password and a password confirmation as input from the user in order to make sure the user entered what they intended to enter(verify input). It then creates a new session for the user and redirects the user to the "/" route.

## Front-end
### All HTML files
- customise.html - to display to the user the inputs and finally the estimated price of the house
- houses.html - to display the available houses to the user depending on what the user enters into the filtering inputs. If no inputs then any type of house is displayed. Users can also input id of a house they like and save it on this page.
- index.html - to display their saved airbnbs and houses to the user in two seperate tables to make it clear which are the airbnbs and which ones are the houses. Has buttons next to each record allowing users to delete that record from their saved if they click it.
- layout.html - provides a consistent display to the user which basically makes the user experience much easier
- login.html
- register.html
- airbnbs.html - to display the available airbnbs to the user depending on what the user enters into the filtering inputs. If no inputs then any type of airbnb is displayed. Users can also input id of an airbnb they like and save it on this page.
- apology.html - rendered on user screen when there is an input error from the user

I made use of boostrap  when creating these files as it made the whole process of styling much easier because of the inbuilt functionality that boostrap has. I also have my own stylesheet "style.css" in which I have a few css selectors that I made use of. The most useful would be the one that seperated the inputs in customise.html evenly on the screen and allowed it to wrap around the screen instead of extending past the edge of the screen(using flexbox).




