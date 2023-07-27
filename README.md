# certificate-maker

## Description
This is a certificate maker app  built on Django. It takes data{ recipient name, date, details(reason for the certification) and signature} and 
returns a certificate. 

### Dependencies

* Django
* Python version 3.10.6


### Executing program

On the terminal execute the below command to create the projects' working directory and move into that directory.

 
```python
$ mkdir app
cd app
```

In the projects' working directory execute the below command to create a virtual environment for our project. Virtual environments make it easier to manage packages for various projects separately.

 
```python
$ py -m venv venv
```

To activate the virtual environment, execute the below command.

```python
$ source venv/Scripts/activate
```
Clone this repository in the projects' working directory by executing the command below.

```python
$ git clone https://github.com/ajaoooluseyi/certificate-maker.git
$ cd certificate-maker

```

To install all the required dependencies execute the below command.

```python
$ pip install -r requirements.txt
```

To run the app, navigate to the app folder in your virtual environment and execute the command below
```python
$ python manage.py migrate

$ python manage.py runserver
```
