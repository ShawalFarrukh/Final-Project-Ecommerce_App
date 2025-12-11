# The Dry Eye Shop
#### Video Demo: https://youtu.be/t7lgG-C8rBQ
## Description
The project that I have created for my CS50 final project is a mock E-commerce app + help and support website for patients suffering from dry eye disease. Dry Eye disease is a chronic eye disease affecting more and more people every day, with the growing use of digital screens in the world
I have an about section which describes the project and its purpose, and then prompts the user to visit the support page for more information on resources and information that helped me personally, without needing to create an account or log in.

## Inspiration

I contracted dry eye disease at the end of 2021 at age 24, and it has affected my life significantly. The disease is gravely misunderstood, and it took me a very long time to understand and improve my symptoms. I wanted to create a platform that can help other people with dry eye who are looking for answers. This platform aims to do that

## Technologies Used

For my project, when deciding on my technology stack, I decided to go with what I was familiar with, which was a lot of the technologies in CS50x. I used Flask as my microservice, where I wrote my routes in Python. I used SQLite for creating a database, creating tables and storing data in them, and also querying my tables in my code for things such as displaying products as well as inserting data, such as new order data for a user.
I’ve also incorporated libraries, including Werkzeug for password hashing, session for storing user sessions, as well as storing products in the cart, rather than storing the cart in the database to keep it lightweight, and since it did not make sense to maintain the cart for the user beyond the session. I’ve also used Jinja templating to render my HTML templates. I used the Bootstrap library for most of my frontend designing, since everything was pretty much available there, and I did not have to write those parts myself. Components such as tables, responsive navbar, logic buttons, etc, have all been used from Bootstrap. I did not want to write custom CSS, so as not to reinvent the wheel, I only did so to standardize the product images for my products page, since I could not figure that out in Bootstrap.

## Features

- Registering a new user
- Login authentication
- About section
- Support page 
- View Products
- Add to cart
- Continue Shopping
- Checkout 
- View Order history
- View Order detail 

## File Overview

### App.py
 Stores my main application written in Python and incorporating Flask, and stores all the routes
 
### Helpers.py 
Stores my two helper functions, login required which is a decorator I use on features which require the user to be logged in such as logout, and db connection which I call in app.py to open a connection to the DB, this was new to me and took some time to wrap my head around since we didn't need to do this bit in CS50, but now the the concepts of opening and closing a connection, as well as committing when making changes to the DB make sense to me. 

### Requirements.txt
Contains all the things required in order to set up my project, which can be installed with the command pip install. My requirements.txt initially included many packages because it was generated using pip freeze inside a virtual environment that contained preinstalled libraries from GitHub Codespaces. However, I later decided to reduce the clutter and only include the actual things required, which are just Flask, Flask-Session, and Werkzeug (For my password hashing, etc.) 

### Static/img
Contains the product images for my store

### Styles.css
Custom CSS, which contains a product-img class used for standardizing my product images.

### Db/app.db
Contains my SQLite database 

### DB/Schema.sql
Contains commands to create my tables

### Db/seed.sql
Contains Seed data to populate my tables and website 

### Templates
Contains all my HTML templates. One thing to note is that throughout my templates, I use url_for for things such as route URLs or images in case the URL is changed in the future.

### Installation
If running on a local machine; 
```
pip install -r  requirements.txt
Flask run 
```

If running on CS50 codespace:
```
pip install -r requirements.txt
export FLASK_APP=app.py
flask run --host=0.0.0.0 --port=8080
```

## Usage

- If a user is not registered and logged in, they can view the about page and the support page.
- A user can register by going to the register in the navbar or by clicking on register on the login page
- Register for a new account on the platform
- Log in with the credentials,
- Once logged in, the user can then view the dry eye products on the index page
- They can add one or more products to the cart 
- Proceed to checkout
- Once the order is complete, they will be taken to the order detail page for the current order
- View their complete order history by clicking on orders
- For each order, the user can click on the order detail to go into the details of each order
- Can click on the The Dry Eye Shop logo or click on the store in the navbar to go to the products page
- The user can click on logout on the navbar to Logout out of the app

## Challenges

Any difficulties you faced and how you overcame them.
Needless to say, even though the finance problem set in CS50 was challenging, creating an end-to-end project from scratch was significantly more challenging, even with AI access now enabled. Some features were easier than others, such as Login and Register. I chose to implement the same way as was done in finance for simplicity’s sake. 
However other features that i implemented for example the checkout function, where multiple steps were being perfomed from counting products in the cart using counter and querying and extracting the relevant products data from the database then creating a list of the products with the attributes then inserting into the orders and order items table, this took me a considerable amount to work with and understand using help from AI. 

I also implemented my project outside of the CS50 codespace, so that I don't get timeouts from the codespace, etc., but then, at the end, using git clone codespace, I duplicated the project in CS50’s codespace in order to submit the project.

## Acknowledgments

I received guidance from ChatGPT for debugging and architectural explanations as well as coding concepts since the course mentioned that we can use ChatGPT and other AI tools only for the final project, in hindsight I’ll be honest that since i was new to coding with only CS50 experience and despite prompting Chatgpt to give beginner friendly help, I believe it made things way more complicated than they needed to be where i often had to learn so many new concepts it was throwing at me, which is a good thing from a learning perspective but it took me very long to complete the project.
The code was implemented by me, and I made sure to completely understand any new concepts that ChatGPT introduced to me.

## Future Improvements

In the future, this can be converted from a mock e-commerce store to an actual store with a payment gateway integrated, a delivery solution implemented as well, and this being placed in an actual live environment 
