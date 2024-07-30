import os
from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
    aws_s3 as s3,
    aws_lambda as lambda_,
    aws_iam as iam,
    CfnOutput, RemovalPolicy,
    Duration,
    aws_logs as logs
)
from constructs import Construct


class CdkEndpointStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # 1. Create a VPC with one public subnet and one private subnet
        vpc = ec2.Vpc(self, "MyVPC",
                      max_azs=1,
                      subnet_configuration=[
                          ec2.SubnetConfiguration(
                              name="Public",
                              subnet_type=ec2.SubnetType.PUBLIC,
                              cidr_mask=24
                          ),
                          ec2.SubnetConfiguration(
                              name="Private",
                              subnet_type=ec2.SubnetType.PRIVATE_ISOLATED,
                              cidr_mask=24
                          )
                      ]
                      )
        flow_log_group = logs.LogGroup(self, "VPCFlowLogs", retention=logs.RetentionDays.ONE_WEEK)
        vpc.add_flow_log("FlowLog", destination=ec2.FlowLogDestination.to_cloud_watch_logs(flow_log_group),
                         traffic_type=ec2.FlowLogTrafficType.ACCEPT)

        # 2. Create an S3 bucket
        bucket = s3.Bucket(self, "MyBucket",
                           bucket_name="s3endpointbeyondthecloud",
                           versioned=True,
                           encryption=s3.BucketEncryption.S3_MANAGED,
                           removal_policy=RemovalPolicy.DESTROY  # Use with caution in production
                           )

        # 3. Create a Lambda function in the private subnet
        lambda_function = lambda_.Function(self, "MyLambdaFunction",
                                           function_name="s3-endpoint",
                                           runtime=lambda_.Runtime.PYTHON_3_11,
                                           handler="index.lambda_handler",
                                           code=lambda_.Code.from_asset("module_lambda"),
                                           vpc=vpc,
                                           vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE_ISOLATED),
                                           timeout=Duration.seconds(5)
                                           )

        # 4. Create S3 VPC endpoint
        s3_endpoint = vpc.add_gateway_endpoint("S3Endpoint",
                                               service=ec2.GatewayVpcEndpointAwsService.S3
                                               )

        # 5. Create associated route and security groups
        # The VPC endpoint automatically adds the necessary route to the route tables
        # Create a security group for the Lambda function
        lambda_sg = ec2.SecurityGroup(self, "LambdaSecurityGroup",
                                      vpc=vpc,
                                      description="Security group for Lambda function",
                                      allow_all_outbound=True
                                      )

        # 6. Give associated permissions to the Lambda function to list down S3 bucket data
        bucket.grant_read(lambda_function)

        # Output the VPC ID, S3 bucket name, and Lambda function name for reference
        CfnOutput(self, "VpcId", value=vpc.vpc_id)
        CfnOutput(self, "BucketName", value=bucket.bucket_name)
        CfnOutput(self, "LambdaFunctionName", value=lambda_function.function_name)
        CfnOutput(self, "VPCFlowLogGroup", value=flow_log_group.log_group_name)
