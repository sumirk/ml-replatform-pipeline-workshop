Hi There,

Welcome to this Workshop for replatforming ML pipeline to Sagemaker Pipelines

Please clone this workshop 

- Create a S3bucket in yoru account
- run the command "chmod +x deploy-cfn-run-task.sh" in the root diretory
- run the bash script './deploy-cfn-run-task.sh' and then run pass the s3-bucket name and the stack-name and your AWS account number to this command. for eg - ./deploy-cfn-run-task techsummit2023mlops cfn-test-summit-cli-01 9707709xxxx 
- The above step will create a cloudformation template and build the docker container and push to ECR.
- A ECS cluster will also be created which will run a task to run the ML pipeline project in the ECS Fargate cluster as a standlone task.
- The trained kmodel and the checkpoints will be saved to your S3 bucket.
- The next steps would be to go through the notebook files and spend the time in re-platforming the solution to Sagemaker.
