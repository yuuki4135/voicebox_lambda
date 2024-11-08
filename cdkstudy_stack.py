from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_apigateway as apigw,
    Duration,
)
from constructs import Construct

class CdkstudyStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Dockerイメージを使用したLambda関数の作成
        my_lambda = _lambda.DockerImageFunction(
            self,
            "CdkstudyLambdaSugimotoContainer",  # 識別子を変更
            code=_lambda.DockerImageCode.from_image_asset(
                "lambda",  # Dockerfile.lambdaが存在するディレクトリ
                file="Dockerfile.lambda"
            ),
            timeout=Duration.minutes(5),  # タイムアウトを5分に変更
            memory_size=2048,  # メモリを2GBに増やす
            architecture=_lambda.Architecture.X86_64,  # アーキテクチャを明示的に指定
        )

        # API Gatewayの作成とLambda統合
        api = apigw.RestApi(
            self,
            "CdkstudyApi",
            rest_api_name="Cdkstudy API",
            description="This is a simple API Gateway with Lambda integration",
            deploy_options=apigw.StageOptions(
                stage_name="api",  # prodからapiに変更
            )
        )

        # プロキシ統合の設定
        api.root.add_proxy(
            any_method=True,  # すべてのHTTPメソッドを許可
            default_integration=apigw.LambdaIntegration(my_lambda)
        )
