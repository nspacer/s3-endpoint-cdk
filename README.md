# VPC Lambda S3 Stack

 

This CDK stack creates an AWS infrastructure setup that includes a VPC, S3 bucket, and Lambda function with the necessary configurations to allow the Lambda function to access the S3 bucket securely.

 

## Stack Components

 

1. **VPC**: Creates a VPC with one public subnet and one private subnet.

2. **S3 Bucket**: Creates a versioned S3 bucket with server-side encryption.

3. **Lambda Function**: Deploys a Lambda function in the private subnet of the VPC.

4. **S3 VPC Endpoint**: Adds an S3 VPC Endpoint to allow private access to S3 from within the VPC.

5. **Security Group**: Creates a security group for the Lambda function.

6. **IAM Permissions**: Grants the Lambda function read access to the S3 bucket.

 

## Prerequisites

 

- AWS CDK installed and configured

- Python 3.9 or later

- AWS CLI configured with appropriate credentials

 

## Deployment

 

1. Clone this repository

2. Navigate to the project directory

3. Create a virtual environment:

python -m venv .venv source .venv/bin/activate # On Windows, use .venv\Scripts\activate

4. Install the required dependencies:

pip install -r requirements.txt

5. Synthesize the CloudFormation template:

cdk synth

6. Deploy the stack:

cdk deploy

 

## Lambda Function

 

The Lambda function code should be placed in a `lambda` directory in the root of your project. The `index.py` file should contain a `handler` function that will be invoked by AWS Lambda.

 

## Cleanup

 

To avoid incurring unnecessary costs, remember to destroy the stack when you're done:

cdk destroy

 

## Security Considerations

 

- The S3 bucket is set to be destroyed when the stack is destroyed. Be cautious with this setting in production environments.

- Ensure that your AWS credentials are kept secure and not shared or committed to version control.

- Review and adjust the IAM permissions and security group rules as needed for your specific use case.

 

## Outputs

 

After deployment, the CDK will output the following information:

- VPC ID

- S3 Bucket Name

- Lambda Function Name

 

You can use these outputs to reference the created resources in other parts of your your application or for manual testing.
 

 
