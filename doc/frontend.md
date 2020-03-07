# Frontend Design

[frontend](/frontend/)

The frontend will be running on your local machine and provide a web-based UI for exploring the data and requesting algorithm results.

## What we have done

The webserver is implemented using [React](https://reactjs.org/). And a Dockerfile is provided for dockerization.

The UI and functionalities are basically implemented. Although our current frontend are using the real REST APIs provided by the [webserver](/webserver/), it's not well-tested.

## What can be improved

1. There is no unit test for the frontend. **However, it's quite important to have unit tests for development.**
2. We only tested it using hardcoded dummy data. However, current integration with webserver is not tested using real data. Thus, we cannot guarantee it works.
3. Although webserver is started and it initializes the tables in the database, it will not initialize any data. Thus, the response from the webserver might be empty. And it will result in a critical issue that the frontend will have some `TypeErrors` of "attribute undefined" because the frontend doesn't check if the response is empty. That's also the reason why I highly recommend to add unit tests.
4. Currently, functionalities of communicating with [ec2server](/doc/ec2setup.md) is not implemented.
