# Mindicador

Mindicator is an application created with rest api to extract values ​​from the https://mindicador.cl/ page that delivers the main economic indicators for Chile, for example:

- Unidad de fomento (UF):
- Euro:
- Dolar
- Indice de valor promedio (IVP):
- Bitcoin


And many more..

# Installation

##### Open your terminal and go to your development folders and create a folder with the name you prefer

#### Clone the repository

`git clone https://github.com/SebastianFL25/Indicador.git`

`git clone git@github.com:SebastianFL25/Indicador.git`

#### Activate the virtual environment
In Mac or Linux
`$ source env/bin/activate`

In Windows
`$ env\Scripts\activate.`

## Start the project in docker

### Active your postgrest

##### If you don't have docker you can install it in
##### [Docker](https://www.docker.com/ "Docker")

####Activate docker from the app

##### In your directory in the cloned repository run:
`docker-compose up`

#### Wait for the process to finish, for everything to load and django to start running, cut the project by pressing: 

`ctrl c`

##### And you execute

    docker-compose run web python manage.py makemigrations
##### Then

    docker-compose run web python manage.py migrate

##### And finally you raise the docker compose again

`docker-compose up`

# Using mindicator

#### Open postman or your browser and active postgrest

##### First you need to create a user in
	
    http://0.0.0.0:8000/users/create/
    
    #With postman select the post method and in the body select form-data and write the following fields: 
    
    username = your_username
    password= your_password
    email=your_email
	

##### Log in with your user

    http://0.0.0.0:8000/users/login/
    
    #POST METHOD
	
    #Send your :
    
    username=your_created_user
    password=your_created_password
	
They will return a token to access the views and one to refresh the token when the access token expires.

#### Para utilizar la vista de obtener tokens por mes y fecha especifica 

    http://0.0.0.0:8000/unit/obtent/
    
	#GET METHOD
	
	#Before using the url you must add the access_token in Authorization next to Params in the postman interface, when you click it add the token specifically in Bearer Token
	
    #You can send a specific date with its indicator type by Query params in postman
     
    #Keys:
    
    #Send for example:
    
    indicator = dolar
    
    #Two forms for send date
    
    #It will bring all the values of the dollar to Chilean pesos for that month
    date = 2024-1
    
    #It will bring a specific day
    date 2024-2-1
    
It should be noted that if you have already searched for the data, when you call it again it will only be displayed and it will not be saved in the database again.

#### To see the data stored or that we are already looking for, we can use the url

    http://0.0.0.0:8000/unit/list/
    
	#GET METHOD
	
    #We must also use the token_access to be able to access
    
    #We can observe the values ​​of the indicators by month and date range, obviously those that we have already stored
    
    #We must send in Query params For example:
    
    #If they are all the values ​​of an indicator for a specific month
    
    indicator= dolar
    date = 2024-2
    
    #If it is a range of values ​​by dates
    
    indicator=dolar
    start_date=2024-2-1
    end_date=2024-2-6
    
#### Finally, to refresh the token_acce you must search for your refresh_token and send it to the url

    http://0.0.0.0:8000/users/refresh/
    
    #Select POST method, use the body and send
    
    refresh = token_refresh