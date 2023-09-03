Hi There,

Welcome to this Workshop for replatforming ML pipeline to Sagemaker Pipelines

Please clone this workshop 

- Create a S3bucket in your account
- run the command "chmod +x deploy-cfn-run-task.sh" in the root diretory
- run the bash script './deploy-cfn-run-task.sh' and then run pass the s3-bucket name, the stack-name and your AWS account number to this command. for eg - ./deploy-cfn-run-task techsummit2023mlops cfn-test-summit-cli-01 9707709xxxx 
- The above step will create a cloudformation template and build the docker container in the directory and push to ECR.
- A Fargate ECS cluster will also be created which will run a task to run the ML pipeline project as a standlone task in your accounts default VPC, Default Subnet with Default security group.
- So, please validate if they provide network connectivity to connect to public resources.
- The trained model and the checkpoints will be saved to your S3 bucket by the container task and then the task will be stopped.
- If you want to run the task again you can do so by running the "aws ecs run-task ...." command in the shell script.
- You should spend the initial 10-15 mins to understand this project and have taken note of the steps and resources being created.

- The below two diagrams/screenshots show the structure of the project.

![image](https://github.com/sumirk/ml-replatform-pipeline-workshop/assets/53355338/07ef5076-1ea8-45ab-a68e-a86a7555095e)


![image](https://github.com/sumirk/ml-replatform-pipeline-workshop/assets/53355338/c028f47a-4e45-4f24-9687-f2511275bbb9)


- After this step open Sagemaker Studio in other browser window if you already have Studio deployed and then use the system terminal to clone the below repository in your Sagemaker studio system terminal.

  - To open in browser - https://github.com/sumirk/ml-replatform-pipeline-sagemaker-workshop
  - Clone link - https://github.com/sumirk/ml-replatform-pipeline-sagemaker-workshop.git

- If you have completed the above steps - Congratulations !! you have completed the first section of this workshop. The fun begins now :)
  
- Follow the steps mentioned in the master.ipynb notebook in the root of the cloned repo in Sagemaker studio.
