<h1 align="center">Enabled</h1>
<h2 align="center"></h2>

View live site [here.](https://bit.ly/3IvP6Mw)

<h4 align="center"><img src="" alt="site image"></h4>

# User Experience (UX) 

## Brief

The local authorities Aids & Adaptations service, which provides equipment and in-home adaptations to vulnerable disabled and elderly residents within the borough, are looking for a solution to improve information sharing between service departments. The current service is spread across multiple authority departments and agencies, all using different software packages for their needs but which don’t communicate with each other. Thus, being reliant on the use of email, chat services (such as MS Teams), and telephone to request and share information relating to orders being requested.

The service provider is asking for a software solution that will enable better access to information and more effective communication between departments. They wish to start with the Minor Works ordering service and, later, on appraisal, expand the system to be used by other services.

## User Stories
### Regular Staff User Goals
A regular staff user should be able to:
  - log in securely
  - view their own details and change their password
  - easily and intuitively navigate the site
  - search for and view customers details
  - add and amend customers details easily
  - create Minor Works orders easily and intuitively
  - view and amend Minor Works orders
  - add and update notes on Minor Works orders
  - delete orders only if created by them

### Admin User Goals
In addition to regular staff users, an admin user should be able to:
  - manage user accounts by being able to:
    - create new users
    - search and view user details
    - amend user details
    - delete user accounts
  - delete customer accounts


## Design
### Colour Scheme:
  - Shades of blue and grey as is common within corporate colour schemes

### Typography:
  - Google Fonts
    - Main text - [Montserrat](https://bit.ly/3MgPTDs)
    - Logo - [Caveat](https://bit.ly/35dPf90)

### Imagery
  - Font Awesome for icons used throughout - [link](https://bit.ly/3tfSjJN)
  - Image on login/welcome page taken from [Clarion Housing](https://bit.ly/3tdXhXn) website (result of Google image search)

### Wireframes

Wireframes for desktop, tablet and mobile views created using Balsamiq.

PDF links here:
  - [Desktop]()
  - [Tablet]()
  - [Mobile]()

## Features

### Implemented
Base features:
  - Login/Welcome page which features an image and some text
  - Navbar, and side nav in mobile/tablet view, consistent throughout the site
  - Nav and side nav reveal 'Adaptations' link and 'Options' drop down menu only when user is logged in
  - Drop down in navbar features 'My Account' and 'Logout' options, plus 'Manage Users' is displayed for Admin only
  - Log out redirects user back to Log in page
  - Footer, to display consistently throughout the site, featuring copyright and social media links

Adaptations:
  - Collapsible that reveals 'Search Customer' feature, 'Create New Customer' form and 'Results' to show the results of the customer search
  - Button in 'Results', revealed with search result, directs user to 'Customer Details' showing more information about the customer
  - Buttons within 'Customer Details' view direct user to 'Edit Customer', 'View Orders, 'Create Order, and 'Back to Search'
  - Edit Customer displays a form to edit customers details with 'Confirm Edit' and 'Return' buttons. A 'Delete Customer' button is revealed only to the Admin user
  - View Orders displays an overview of all the orders created for that customer as well as 'View' and 'Edit' buttons
    - View directs the user to a more detailed view of the order
    - Edit directs the user to a form whereby they can change any details of the order, including add notes. If the user created the order, they can also delete it from here.
  - Create Order displays a form for the user to create a new order for the customer

My Account:
  - Button to reveal session users details
  - Button to direct user to 'Change Password'
  - Change Password page displays form to let the user change their password

Manage Users (Admin user only feature):
  - Collapsible showing 'Search Users' search bar, 'Create New User' form and 'Results' displaying the search results and 'Edit User' button
  - Edit User button directs the Admin user to a form where they can edit the users details or delete the user - delete user function is not available on the Admin account information preventing Admin from being deleted

### Future features
Adaptations:
  - Ability to created multiple notes on work orders which are datetime stamped and show which user each one was created by
  - Datetime stamp each order when it is created and amended
  - Addition of Major Works orders
  - Addition of Customer Assessments

My Account:
  - Additional check on password change to confirm new password match
  - Stronger password criteria (capital letters, numbers, special characters etc.)

Manage Users:
  - Additional user information such as phone number, service area/department
  - Users password reset function

General:
  - Notification alerts to let users know their orders have been updated with new notes, order completed etc.
  - Customer portal to allow customers to keep track of orders on their account


## Database Design

MongoDB is used to store the data set out in three collections:
  - Customers
    - _id
    - first_name
    - last_name
    - dob
    - gender
    - address_street
    - address_city
    - address_county
    - postcode
    - tenure
    - phone
    - email
    - created_by
    - amended_by

  - Jobs
    - _id
    - first_name
    - last_name
    - dob
    - gender
    - address_street
    - address_city
    - address_county
    - postcode
    - tenure
    - phone
    - email
    - keysafe
    - keysafe_text
    - int_grab
    - int_grab_text
    - ext_grab
    - ext_grab_text
    - drop_rail
    - drop_rail_text
    - newel
    - newel_text
    - stair_rail
    - stair_rail_text
    - handrail
    - handrail_text
    - step
    - step_text
    - ramp
    - ramp_text
    - shower
    - shower_text
    - other
    - other_text
    - ref_name
    - team
    - ref_email
    - ref_phone
    - is_urgent
    - due_date
    - created_by
    - amended_by
    - comp_date
    - is_comp
    - notes

  - Users
    - _id
    - username
    - password
    - employee_name
    - employee_email


## Technologies Used

### Languages:
  - HTML 5
  - CSS 3
  - Javascript (JQuery)
  - Python

### Frameworks, libraries and programmes:
  - Materialize - used to create layout
  - JQuery - for JS functions
  - Pip - to install required dependencies
  - Git & Github - for version control and code storing
  - Balsamiq - for wireframes
  - Heroku - to deploy live site

### Database Technologies
  - Flask-PyMongo to connect Python/Flask app to MongoDB
  - MongoDB - to store database contents

### Workspace
  - Gitpod - VSCode based virtual IDE

## Testing

Description of testing process.

The deployed website was also tested using Chrome, Edge and Firefox as well as on mobile (using Chrome for Android)

- ### User stories' testing:
    - 
        - 
    - 
        - 
    - 
        - 
    - 
        - 
    - 
        - 
    - 
        - 
    - 
        - 

- ### Validator testing:
    - HTML - [W3C Validator](https://bit.ly/3vkSIx1) - valid
    - CSS - [(Jigsaw) validator](https://bit.ly/3nMSs4G) - valid
    - Javascript - [JSHint](https://bit.ly/3jRVMKH) - valid
    - Python - [Pep8](https://bit.ly/33VMJDA) - valid

- ### Additional testing:
    Black box testing was also carried out on the final deployed website.
    
    All tests passed. Results can be viewed [here]()

- ### Bugs
    - 
    - 

## Deployment
### Heroku
  - Site deployed to Heroku using the following process:



## Credits

### Content:
- Minor Works Order form based on the actual form used by Sandwell Council Aids & Adaptations service - example form [here](docs/readme_items/minor_works_form.pdf)
 
### Media:
- Welcome/Login page image taken from [Clarion Housing](https://bit.ly/3tdXhXn)

### Acknowledgements:
- Sean, Ger and Oisin from Code Institute Tutor Support

