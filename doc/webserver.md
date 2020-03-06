# Webserver Design

[webserver](/webserver/)

The webserver will be running on your local machine and providing REST APIs for the [frontend](/doc/frontend.md). It serves as a bridge between the frontend and the database. In other word, it (1) receives requests from the frontend web application and (2) translate the request to database queries and (3) format the data received from the database and (4) respond the formatted data to the frontend.

Also, it can serve static files, such as [script_and_upload_files.py](/webserver/script/static/split_and_upload_files.py), for the frontend.

## What we have done

The webserver is implemented using [Python Django REST Framework](https://www.django-rest-framework.org/) and [PostgreSQL](https://www.postgresql.org/) as backend. And a Dockerfile is provided for dockerization.

The key part of the webserver sub-project is [models](/webserver/script/models/), where the database schema is defined. At the very beginning, we just wanted to store some [basic data](/webserver/script/models/data.py) such as county info in the database. However, we wanted to cache the computed algorithm results for better performance later. Thus, we just simply defined some schema for [algorithm results](/webserver/script/models/algorithms.py) and [algorithm config](/webserver/script/models/config.py). Then, for a given config from user inputs, which consists of a set of parameters, we can retrieve the `id` of the config. And with this config `id`, we can retrieve algorithm results.

Another trick I want to mention is that to have a simpler schema design, we are using a single `JSONField` to store most results.

## What can be improved

1. Because we haven't fully understood the algorithms, we don't know if our design for algorithm results are good. That's also another reason why we decided to use a single `JSONField`. But feel free to change it if you have better idea.
