# my-retail

To run the sever locally:

* Create a virtualenv: `python3 -m venv env`
* Activate the virtualenv: 
`env\Scripts\activate.bat` (Windows)
`source env/bin/activate` (Mac OS)
* Install the requirements: `pip install -r requirements.txt`
* Run the server: `python app.py`
* Test the up endpoint at `/up`

To run the unit tests:
* From the root project directory run: `python -m unittest`

# Available Endpoints

* **URL**

  /products/<product_id>/

* **Supported methods:**
  
  `GET` | `PUT` | test3
 
