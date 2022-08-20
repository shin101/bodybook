## Bodybook


### 1. What goal will your website be designed to achieve? 
I will be creating a new social media site called Bodybook that will be the next facebook
i will be creating a simple frontend page that, once a user logs in, uses a random user generator API to mimic your current (and fake) friends on friends list to look like you have more friends than you do IRL. It will look something like this : ![schema](https://github.com/shin101/bodybook/blob/main/friendlist.png?raw=true)


There will be a sign up, login and log out functionality. Users will also be able to post a status update on their Bodybook feed.

### What kind of users will visit your site? 
Age group will be similar to that of LinkedIn users. Target audience is adults

### What data do you plan on using? 
API: https://randomuser.me/documentation
APP DB: PostgreSQL
[WTForms - alchemy](https://wtforms-alchemy.readthedocs.io/en/latest/ )

### What does your database schema look like? 
![schema](https://github.com/shin101/bodybook/blob/main/Bodybook_schema.png?raw=true)


### Is there any sensitive information you need to secure? 
Login, password, authentication. Users must be logged in to see posts. Passwords will be stored with Flask Bcrypt. I will also be using the [Flask-Login add-on](https://flask-login.readthedocs.io/en/latest/) 


### What functionality will your app include? 
Signup, login, log out, view friends, post

### What will the user flow look like? 
Landing page that shows a sign up page as well as a log in link in the nav bar for existing users. 
Once a user is logged in they will be taken to a page where they can view their own profile. From this page there are links to check their friend list as well as make a post. 

### What features make your site more than CRUD? Do you have any stretch goals?
May add a delete and add friend feature. Add access feature so that user's page can only be accessed once you are friends with the individual
