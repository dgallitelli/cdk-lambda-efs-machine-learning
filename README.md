# Using Amazon EFS with AWS Lambda to load a ML model

In this project, we will attach an Amazon EFS to an AWS Lambda. In the EFS, there is an XGBoost model (`model.tar.gz`), which will be loaded at runtime by the AWS Lambda. Since this does not require a download from Amazon S3, it has lower latency with respect to S3.

> Notes: if you don't know how to load the model manually to EFS, make sure to uncomment line 9 in the `predict.py` file adding your bucket and prefix pointing towards the `.tar.gz` file containing the model and the `bucket` line 22 in `stack.py`