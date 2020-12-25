## #Quickstart
In a seconds after you installed and init your project the project directory will be
generated with structure tree packages.
```
- your project
    - app
        -resources
    - db
        - model
        - version
    - config.ini
    - serve.py
    - env.py
    - *.py.mako
```

This is the core structure Metric framework for your project. The config.ini is contain
the basic configuration for your system. such as database, key, project name and more.
Before you going deeper, you have to re-assign your configuration in **config.ini**

## #Tutorial
Welcome to the Metric framework tutorial, in this topic we will demonstrate and guide you
to create a simple blog page using Metric framework. We assume you have Metric installed in
your environment. Let's get started to it

first, we need to init our application to be build
```shell
$ python -m metric init-app=my_website
```
Metric will directory and create your application, called **my_website**.
Then, you can go to your project directory and start build the things you need for example:
Model, Migration and Plantation