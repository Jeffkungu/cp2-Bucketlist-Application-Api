# cp2-Bucketlist-Application-Api
[![Coverage Status](https://coveralls.io/repos/github/Jeffkungu/cp2-Bucketlist-Application-Api/badge.svg?branch=develop)](https://coveralls.io/github/Jeffkungu/cp2-Bucketlist-Application-Api?branch=develop)
{<img src="https://coveralls.io/repos/github/Jeffkungu/cp2-Bucketlist-Application-Api/badge.svg?branch=develop" alt="Coverage Status" />}[https://coveralls.io/github/Jeffkungu/cp2-Bucketlist-Application-Api?branch=develop]


According to Merriam-Webster Dictionary, a Bucket List is a list of things that one has not done before but wants to do before dying. This app creates an API for an online Bucket List service using Flask.

#### GETTING STARTED:

1. Clone Repo:

    ```
    $ git clone https://github.com/Jeffkungu/cp2-Bucketlist-Application-Api.git
    ```
2. Navigate to local directory.

    ```
    $ cd cp2-Bucketlist-Application-Api
    ```
3. Create a virtualenvironment(assuming you have virtualenvwrapper).

    ```
    $ mkvirtualenv -p python3 venv
    ```
4. Install all app requirements

    ```
    $ pip install -r requirements.txt
    ```

5. Create the database and run migrations

    ```
    $ python manage.py create_db [name]
    ```

**To run migrations**:
   `$ python manage.py db init`

   `$ python manage.py db migrate`

   `$ python manage.py db upgrade`

Don't forget to set your APP_SETTINGS to set your app configurations, you can choose from:
    - development
    - testing
    - production
    - staging
    #e.g.
    `$ export APP_SETTINGS='development`

 6. All done! Now, start your server by running `python manage.py runserver`. For best experience, use a GUI platform like [postman](https://www.getpostman.com/) to make requests to the api.

### Endpoints

Here is a list of all the endpoints in bucketlist app.

Endpoint | Functionality| Access
------------ | ------------- | -------------
POST /api/v1/auth/login |Logs a user in | PUBLIC
POST /api/v1/auth/register | Registers a user | PUBLIC
POST /api/v1/bucketlists/ | Creates a new bucket list | PRIVATE
GET /api/v1/bucketlists/ | Lists all created bucket lists | PRIVATE
GET /api/v1/bucketlists/id | Gets a single bucket list with the suppled id | PRIVATE
PUT /api/v1/bucketlists/id | Updates bucket list with the suppled id | PRIVATE
DELETE /api/v1/bucketlists/id | Deletes bucket list with the suppled id | PRIVATE
POST /api/v1/bucketlists/id/items/ | Creates a new item in bucket list | PRIVATE
PUT /api/v1/bucketlists/id/items/item_id | Updates a bucket list item | PRIVATE
DELETE /api/v1/bucketlists/id/items/item_id | Deletes an item in a bucket list | PRIVATE

### Features:
* Search by name
* Pagination
* Token based authentication
### Searching

You can search bucketlists or items using the parameter `q` in the GET request method.
Example:

`GET http://localhost:/bucketlists/3/items?q=Sarova`

This request will return all items in a bucketlist with id 3 having the name `Sarova`.

### Pagination

It is possible to limit the count of bucketlist data displayed using the parameter `limit` in the GET request method.

Example:

`GET http://localhost:/api/v1/bucketlists?limit=3`

It is also possible to set the record we would like to start viewing from.

Example:

`GET http://localhost:/api/v1/bucketlists?page=10`

### Sample GET response
After a successful resgistration and login, you will receive an athentication token. Pass this token in your request header.
Below is a sample of a GET request for bucketlist

```
{
  "id": 14,
  "name": "Travelling",
  "items": [],
  "date_created": "Fri, 15 May 2017 08:50:00 GMT",
  "date_modified": "Wed, 27 May 2017 18:00:00 GMT",
  "created_by": "4"
}

```

### Testing
The application tests are based on python’s unit testing framework unittest.
To run tests with nose, run `nosetests` or `python manage.py test`
