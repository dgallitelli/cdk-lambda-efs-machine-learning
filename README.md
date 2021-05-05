# Using Amazon EFS with AWS Lambda to load a ML model

In this project, we will attach an Amazon EFS to an AWS Lambda. In the EFS, there is an XGBoost model (`model.tar.gz`), which will be loaded at runtime by the AWS Lambda. Since this does not require a download from Amazon S3, it has lower latency with respect to S3.

> Notes: if you don't know how to load the model manually to EFS, make sure to 

### To deploy

1. Run `sh build_and_push <name-of-your-liking>` in the `container` folder 
    a.  in my case, the image name is `xgboost-lambda`. If you change it, change line 30 in `stack.py`
2. You can use an existing EC2 / Cloud9 / SageMaker Notebook to mount the EFS partition and upload the model. Instead, if you want the Lambda to load the model to the EFS: 
    a. upload the model to S3 with `aws cp model.tar.gz s3://{bucket}/{prefix}/` 
    b. uncomment line 9 in the `predict.py` file adding your bucket and prefix pointing towards the `.tar.gz` file containing the model 
    c. change the `bucket` line 22 in `stack.py` with your bucket
3. Run `pip install -r requirements.txt` then `cdk deploy` in the `stack` folder
    a. if you don't have CDK installed, run `npm install -g aws-cdk@latest`
4. Run `test.py` from the `test` folder
5. Remember to change back the `predict.py` file and then redeploy your stack