from aws_cdk import (
    aws_iam as iam,
    aws_ecr as ecr,
    aws_efs as efs,
    aws_ec2 as ec2,
    aws_lambda,
    aws_apigatewayv2 as apigw,
    core
)


class InferenceStack(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # ==================================================
        # =============== CFN PARAMETERS ===================
        # ==================================================

        name = f'lambda-efs-ml-demo'
        bucket = 'sagemaker*'

        # ==================================================
        # ================== ECR IMAGE =====================
        # ==================================================
        ecr_repository = ecr.Repository.from_repository_name(
            scope=self,
            id='repo',
            repository_name='xgboost-lambda'
        )

        ecr_image = aws_lambda.DockerImageCode.from_ecr(
            repository=ecr_repository,
            tag='latest'
        )

        # ==================================================
        # ==================== VPC =========================
        # ==================================================
        my_vpc = ec2.Vpc(self, 'efs_vpc')

        # ==================================================
        # =============== EFS FILE SYSTEM ==================
        # ==================================================
        efs_fs = efs.FileSystem(
            self, id='ml_file_system', vpc=my_vpc, encrypted=True
        )
        ap = efs_fs.add_access_point(
            'lambda_access_point', path='/model',
            create_acl=efs.Acl(owner_gid='1001', owner_uid='1001', permissions='750'),
            posix_user=efs.PosixUser(uid='1001', gid='1001')
        )

        # ==================================================
        # ================ LAMBDA FUNCTION =================
        # ==================================================
        lambda_function = aws_lambda.DockerImageFunction(
            self, id='lambda',
            function_name=name,
            code=ecr_image,
            memory_size=1024,
            timeout=core.Duration.seconds(45),
            vpc=my_vpc, 
            filesystem=aws_lambda.FileSystem.from_efs_access_point(ap, "/mnt/model")
        )
        lambda_function.add_to_role_policy(
            iam.PolicyStatement(actions=["s3:GetObject"],resources=[f"arn:aws:s3:::{bucket}"], effect=iam.Effect.ALLOW)
        )

        # ==================================================
        # ================== API GATEWAY ===================
        # ==================================================
        api = apigw.HttpApi(
            scope=self,
            id='api_gateway',
            api_name=name,
            cors_preflight={
                "allow_headers": ["Authorization"],
                "allow_methods": [apigw.HttpMethod.POST],
                "allow_origins": ["*"],
                "max_age": core.Duration.days(15)
            }
        )

        integration = apigw.CfnIntegration(
            scope=self,
            id='integration',
            api_id=api.http_api_id,
            integration_type='AWS_PROXY',
            integration_uri=lambda_function.function_arn,
            integration_method='POST',
            payload_format_version='2.0',
            # credentials_arn=lambda_function.role.role_arn,
        )

        apigw.CfnRoute(
            scope=self,
            id='route',
            api_id=api.http_api_id,
            route_key='POST /',
            target=f'integrations/{integration.ref}'
        )


app = core.App()
InferenceStack(app, "inference")

app.synth()
