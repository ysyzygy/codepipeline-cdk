

## Prerequisites

### Local env:

###### AWS CodeCommit
Setup for HTTPS connections to AWS CodeCommit with git-remote-codecommit
https://docs.aws.amazon.com/codecommit/latest/userguide/setting-up-git-remote-codecommit.html

To install git-remote-codecommit
```
pip install git-remote-codecommit
```

Check your gitconfig: https://docs.aws.amazon.com/codecommit/latest/userguide/setting-up-https-unixes.html#setting-up-https-unixes-credential-helper
```
git config --global credential.helper '!aws codecommit credential-helper $@'
git config --global credential.UseHttpPath true
```

Connect to the CodeCommit console and clone the repository
```
git clone codecommit://MyDemoRepo my-demo-repo
```
You need assume a role with permissions otherwise an 403 will be thrown.

###### AWS CDK
Set up your workstation with your AWS credentials

```
$ aws configure
$ npm install -g aws-cdk
```
Test the installation by issuing cdk --version

The Python package installer, pip, and virtual environment manager, virtualenv, are also required.
```
python -m ensurepip --upgrade
python -m pip install --upgrade pip
python -m pip install --upgrade virtualenv
```

Managing AWS Construct Library modules
```
pip install aws_cdk.aws_codedeploy aws_cdk.aws_lambda aws_cdk.aws_codebuild aws_cdk.aws_codepipeline
pip install aws_cdk.aws_codecommit aws_cdk.aws_codepipeline_actions
```

## You should explore the contents of this project.

The `cdk.json` file tells the CDK Toolkit how to execute your app.

This project is set up like a standard Python project.  The initialization process also creates
a virtualenv within this project, stored under the .env directory.  To create the virtualenv 
it assumes that there is a `python3` executable in your path with access to the `venv` package.
If for any reason the automatic creation of the virtualenv fails, you can create the virtualenv
manually once the init process completes.

To manually create a virtualenv on MacOS and Linux:

```
$ python3 -m venv .env
```

After the init process completes and the virtualenv is created, you can use the following
step to activate your virtualenv.

```
$ source .env/bin/activate
```

If you are a Windows platform, you would activate the virtualenv like this:

```
% .env\Scripts\activate.bat
```

Once the virtualenv is activated, you can install the required dependencies.

```
$ pip install -r requirements.txt
```

At this point you can now synthesize the CloudFormation template for this code.

```
$ cdk synth
```

You can now begin exploring the source code, contained in the hello directory.
There is also a very trivial test included that can be run like this:

```
$ pytest
```

To add additional dependencies, for example other CDK libraries, just add to
your requirements.txt file and rerun the `pip install -r requirements.txt`
command.

## Useful commands

 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation
