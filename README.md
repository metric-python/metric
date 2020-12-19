## #Metric Framework
Metric is framework built for web application development with elegant, structured, and
simple. Metric provide not just only core tools for web application development, but it
also built-in with rich resources for any purpose, allowing you to focus with your idea
and expand it without worries.

If you're new to python or python3 you don't have to worry, Metric will help you to grow,
expand and focused with your idea.

## #Installation
Metric is only available on python3, so you can start your own project with virtualenv
or by using system python. For virtualenv you can follow this steps
```shell
# install the virtualenv
$ python3 -m pip install virtualenv

# creating your virtualenv
$ python3 -m virtualenv metric-env

# change source to virtualenv
$ source metric-env/bin/activate

# add wheel and metric to your virtualenv
$ pip install wheel
$ pip install metric
```

Or, if you prefer with github repository follow this guidance

```shell
# clone from github
$ git clone https://github.com/kzulfazriawan/metric

# build
$ python3 setup.py build sdist bdist_wheel

# install
$ python3 setup.py install
```

After the installation you can see the list of all available command from metric and
create your own project with Metric, by running the **init-app**
```shell
# showing all available command from Metric
$ python -m metric

# starting your own project
$ python -m metric init-app=blog
```

Congratulations!, Now you have a project called blog.