# opal-api
Backend of Opal software

1. `pip3 install fastapi`
2. `pip3 install "uvicorn[standard]"

> To run: `python -m uvicorn main:app --reload`

## FastApi
This application runs the [FastApi](https://fastapi.tiangolo.com/) framework. 
It provides an interactive doc for our own application. To access it:
1. Run the application
2. Go to `localhost:8000/docs` or `localhost:8000/redoc`