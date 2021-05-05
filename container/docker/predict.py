import os
import json
import xgboost
import pandas as pd
import pickle as pkl
from utils import extract_model

# LOAD MODEL (uncomment next line if the EFS is empty and the model is in S3 - run once, then comment again)
# extract_model('s3://{bucket}/{prefix}/model.tar.gz', '/mnt/model')
model = pkl.load(open('/mnt/model/xgboost-model', 'rb'))


def handler(event, context):
    # TRANSFORM DATA
    body = json.loads(event['body'])
    df = pd.DataFrame(body, index=[0])
    data = xgboost.DMatrix(df.values)

    # PREDICT
    prediction = model.predict(data)

    return {
        'prediction': str(prediction)
    }
