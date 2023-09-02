
#!/bin/bash

if [ $# -ne 3 ]; then
  echo "Usage: $0 <S3_BUCKET_NAME> <CLOUDFORMATION_TEMPLATE_NAME> <ACCOUNT_NUMBER>"
  exit 1
fi

# Assign arguments to variables
S3_BUCKET_NAME="$1"
CLOUDFORMATION_TEMPLATE_NAME="$2"
ACCOUNT_NUMBER="$3"

# Step 1: Create the CloudFormation Stack
stack_name="my-stack-$(date +%Y%m%d%H%M%S)"
aws cloudformation create-stack \
  --stack-name "$stack_name" \
  --template-body "file://tech-summit-2023-ml-pipeline-cfn-template.yml" \
  --parameters ParameterKey=S3BucketName,ParameterValue="$S3_BUCKET_NAME" \
  --capabilities "CAPABILITY_IAM" "CAPABILITY_NAMED_IAM"


# Wait for the stack creation to complete
aws cloudformation wait stack-create-complete \
  --stack-name "$stack_name"

# Step 2: Retrieve Outputs
outputs_json=$(aws cloudformation describe-stacks \
  --stack-name "$stack_name" \
  --query 'Stacks[0].Outputs')

cleaned_json=$(echo "$outputs_json" | tr -d '[:space:]')

# Extract ECS Task Definition ARN and Fargate Cluster Name
ECSTaskDefinitionArn=$(echo "$cleaned_json" | awk -F '[",]' '/"OutputKey":"FargateClusterName"/{print $39}' | tr -d '"')
FargateClusterName=$(echo "$cleaned_json" | awk -F '[:,]' '/"OutputKey":"FargateClusterName"/{print $11}' | tr -d '"')
ContainerImage=$(echo "$cleaned_json" | awk -F '[:,]' '/"OutputKey":"ContainerImage"/{print $4}' | tr -d '"')

echo "ECSTaskDefinitionArn: $ECSTaskDefinitionArn"

git clone https://github.com/zalandoresearch/fashion-mnist.git

aws s3 cp ./fashion-mnist/data/fashion s3://$S3_BUCKET_NAME/raw_data/ --recursive

cd tensorflow-pipeline-docker

# Build Docker image
docker build -t techsummit2023-ml-workshop .

# Authenticate and push the image to ECR

aws ecr get-login-password --region ap-southeast-2 | docker login --username AWS --password-stdin $ACCOUNT_NUMBER.dkr.ecr.ap-southeast-2.amazonaws.com

# Tag the image
docker tag techsummit2023-ml-workshop:latest $ContainerImage

# Push the image using the docker push command:
docker push techsummit2023-ml-workshop $ContainerImage


# Step 3: Run ECS Task
default_vpc_id=$(aws ec2 describe-vpcs --filters "Name=isDefault,Values=true" --query "Vpcs[0].VpcId" --output text)
default_public_subnet_id=$(aws ec2 describe-subnets --filters "Name=vpc-id,Values=$default_vpc_id" "Name=mapPublicIpOnLaunch,Values=true" --query "Subnets[0].SubnetId" --output text)
default_security_group_id=$(aws ec2 describe-security-groups --filters "Name=vpc-id,Values=$default_vpc_id" "Name=group-name,Values=default" --query "SecurityGroups[0].GroupId" --output text)

echo "Default Public Subnet ID: $default_public_subnet_id"
echo "Default Security Group ID: $default_security_group_id"

aws ecs run-task \
    --launch-type FARGATE \
    --cluster "$FargateClusterName" \
    --task-definition "$ECSTaskDefinitionArn" \
    --count 1 \
    --network-configuration "awsvpcConfiguration={subnets=[$default_public_subnet_id],securityGroups=[$default_security_group_id],assignPublicIp=ENABLED}" \
    --enable-execute-command \
    --enable-ecs-managed-tags

# Clean up: Delete the CloudFormation Stack (optional)
# aws cloudformation delete-stack --stack-name "$stack_name"

echo "ECS Task Started. Task Definition ARN: $ECSTaskDefinitionArn, Fargate Cluster Name: $FargateClusterName"

