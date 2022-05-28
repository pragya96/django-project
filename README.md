# django-project
To set up the project:
1. Clone the repository:
`git clone https://github.com/pragya96/django-project.git`
2. Create and activate a virtual environment 
3. Install all libraries from "requirements.txt":
`pip install -r requirements.txt`
4. Navigate to the folder containing "manage.py":
 `cd django_project`
5. Make migrations:
`python manage.py makemigrations`
6. Migrate:
`python manage.py migrate`
7. Create a super user:
`python manage.py createsuperuser` 
8. Run the server:
`python manage.py runserver`
9. You can now access the project on your localhost "http://127.0.0.1:8000"

## Recommendations for the future
There are many improvements that can be made to this project to enhance the user experience in the future. 

##### Map representation
One of the ways to improve the user experience is to add fields to the store model which allows in saving the coordinates of the store. With the help of this field, a map representation can be created with pins showing the different locations available for the stores. This map can also be used to find stores with a particular category of products. The pins on the map showing the location can also display a number showing the number of results found for a selected category. 

##### Many-to-many product to store relationship
Any of the products can be available in multiple stores. To depict this, a many-to-many relationship can be created between a product and stores. The relationship can be created using a through model where the number of quantity of products available in each store can be saved. This feature would contribute to the map representation of the available products and allow customers to search all the stores where a particular product is available. 

##### Product delete option
The admin users can be given a product delete option in the table with excel-like editing option to delete a product if they want to remove from the database. 

##### Customer Interface
The application can be improved by customizing the design of the interface.
