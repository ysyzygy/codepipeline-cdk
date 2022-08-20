import setuptools


with open("README.md") as fp:
    long_description = fp.read()


setuptools.setup(
    name="project-name",
    version="0.0.1",

    description="Pipeline CDK Python app",
    long_description=long_description,
    long_description_content_type="text/markdown",

    author="ysyzygy",

    package_dir={"": "stacks"},
    packages=setuptools.find_packages(where="stacks"),

    install_requires=[
        "aws-cdk.core",
        "aws-cdk.aws_codebuild",
        "aws-cdk.aws_codecommit",
        "aws-cdk.aws_codepipeline",
        "aws-cdk.aws_codepipeline_actions",
        "aws-cdk.aws_ec2",
        "aws-cdk.aws_events",
        "aws-cdk.aws_events_targets",
        "aws-cdk.aws_iam",
        "aws-cdk.aws_lambda",
        "aws-cdk.aws_s3",
    ],

    python_requires=">=3.6",

    classifiers=[
        "Development Status :: 4 - Beta",

        "Intended Audience :: Developers",

        "License :: OSI Approved :: Apache Software License",

        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",

        "Topic :: Software Development :: Code Generators",
        "Topic :: Utilities",

        "Typing :: Typed",
    ],
)
