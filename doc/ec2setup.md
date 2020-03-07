# SCRIPT-ec2setup(ec2server)

[ec2setup](/ec2setup/)

This sub-project is what we plan to run on the remote AWS server. It should be able to:

1. keep track of `cleaned data` stored in `s3` by polling the bucket periodically or when it receives `refresh` requests from users;
2. compute the results when it receives users' requests for algorithm results of given parameters(inputs);
3. store all results to the `RDS` database and notify the frontend that the results are ready.

**However, none of these functionalities is fully implemented. Thus, I highly recommend to not continue to develop on current code. Please refer to [What can be improved](#what-can-be-improved) for more information.**

## What we have done

This sub-project hardcodes some important `s3 paths` and involve a lot of human interaction. And I think the only thing we did here is we wrote some code for storing data into the database.

## What can be improved

1. **I recommend to continue to develop based on [branch ec2_server](https://github.com/slacgismo/SCRIPT/tree/ec2_server/ec2server).** In this branch, I'm using `RabbitMQ` and `Celery`, with which the ec2server can respond to the frontend immediately without waiting for the computing for the algorithm results. If ec2server finds that the results have been cached in the database, it will retrieve results from database and send it back the the frontend.
2. Another issue is the way we notify the frontend(not implemented yet). I can come up with two solutions:
   1. frontend polls for updates periodically from the ec2server;
   2. ec2server sends an email to the user when the results are computed and stored in the database. Then, users can request for the second time and get the results.
3. The ec2server should also provide an endpoint for `refresh` so that the frontend can enforce the server to check for new data in `s3` buckets.
