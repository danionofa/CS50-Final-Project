# Hobby Hollow

Hobby Hollow is a web application for users to explore new interests based on movies and shows that they already enjoy. This is my documentation for Hobby Hollow.

Youtube video link: (https://youtu.be/0p8vfVi4O6c)

# Getting Started

Check if you have pip by running 
```bash
pip --version
```
If pip is not installed, you will get an error that looks like "pip not found". Install pip using this [Online Guide] (https://www.geeksforgeeks.org/download-and-install-pip-latest-version/).

## While in the hobbyhollow folder

Execute:
```bash
pip install -r requirements.txt
```

# Running Flask

## While in the final_project folder

Execute these three lines:
```bash
export FLASK_APP=hobbyhollow
export FLASK_ENV=development
flask run
```

Copy the address that is returned and open it in your browser and you should see the index page of the application.

Register for an account by clicking the "Register" button. You will see a success message on screen and be redirected to a login page after registering. Login with the same credentials that you registered with to access Hobby Hollow.

Once logged in, you will see your home page with the message "Upload your favorite movies and shows in the upload tab!" Navigate to the upload tab by clicking the 'upload' link in the message or using the navigation bar. 

Once you have reached the upload tab you can begin to populate your home page! Enter a movie or show title and specify its type to add a hobby. 
NOTE: MOVIES AND SHOWS ARE REFERRED TO AS HOBBIES
Continue uploading until your satisfied! Once you are ready to see your uploads, return back to the home page by clicking 'Hobby Hollow' in the navigation bar.

The home page will now show you all the hobbies you have uploaded with an image, a title, and a short description of each. On the home page you have the option to delete hobbies that you are no longer interested in by simply clicking the 'Delete' button on a card.

To see suggestions of titles to add to your home page based on titles you have uploaded, navigate to the 'Explore' tab. Here you will see a long list of movies and shows that are generated based on your own uploads. To add these to your home page, simply press the 'Add' button on the bottom of the card. Return back to your homepage to see all the suggestions you've added!

The 'Sources' tab gives credit to the database used to populate the home and explore pages.

To log out of the application, click "Log Out" in the top right corner of your browser.