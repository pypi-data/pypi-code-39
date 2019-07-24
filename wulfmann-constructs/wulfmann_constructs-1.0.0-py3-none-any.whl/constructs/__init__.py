from aws_cdk import (
    core,
    aws_lambda as lambda_,
    aws_s3 as s3
)

name = "constructs"

class Lambda(core.Construct):
    def __init__(self, scope, id, bucket_name, s3_key, function_name, handler, runtime, memory_size, timeout):
        super().__init__(scope, id)

        self.fn = lambda_.Function(
            self, 'Lambda',
            handler=handler,
            role=self.role,
            code=lambda_.S3Code(
                bucket=s3.Bucket.from_bucket_attributes(
                    self, 'Bucket',
                    bucket_name=bucket_name
                ),
                key=s3_key
            ),
            runtime=lambda_.Runtime(runtime),
            function_name=function_name,
            memory_size=memory_size,
            timeout=core.Duration.seconds(timeout)
        )
