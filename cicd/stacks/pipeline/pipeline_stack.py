from aws_cdk import (core, aws_codebuild as codebuild,
                     aws_codecommit as codecommit,
                     aws_codepipeline as codepipeline,
                     aws_codepipeline_actions as codepipeline_actions,
                     aws_iam as iam)
from string import Template


class PipelineStack(core.Stack):
    """A root construct which represents a codepipeline CloudFormation stack."""

    def __init__(self, scope: core.Construct, id: str, repo_name:str, pipeline: dict,props: dict,  template: Template,
                 **kwargs) -> None:
        """Creates a new pipeline stack.

        :param scope: Parent of this stack, usually an ``App`` or a ``Stage``, but could be any construct.
        :param id: The construct ID of this stack.
         If ``stackName`` is not explicitly defined,
          this id (and any parent IDs) will be used to determine the physical ID of the stack.
        :param props: Environment properties
        :param kwargs: Optional Keyword arguments
        """
        super().__init__(scope, id, stack_name=id, description=pipeline["description"], **kwargs)


        code = codecommit.Repository.from_repository_name(self, repo_name, repo_name)

        build_image = codebuild.LinuxBuildImage.STANDARD_5_0
        iam_role_name = template.substitute(name=pipeline['role_name'])
        iam_role = iam.Role(self, iam_role_name,
                            role_name=iam_role_name,
                            assumed_by=iam.ServicePrincipal("codebuild.amazonaws.com"),
                            managed_policies=[
                                iam.ManagedPolicy.from_aws_managed_policy_name({cdk_policy})]
                            )
        iam_role.assume_role_policy.add_statements(
            iam.PolicyStatement(
                effect=iam.Effect.ALLOW,
                actions=["sts:AssumeRole"],
                principals=[iam.ServicePrincipal("codepipeline.amazonaws.com")]))

        source_account_id = pipeline['source_account_id']
        target_account_id = pipeline['account_id']
        env = pipeline['environment']



        cdk_build_name = template.substitute(name=props['codebuild_buildstage']['name'])
        cdk_build = codebuild.PipelineProject(
            self, cdk_build_name,
            project_name=cdk_build_name,
            description=template.substitute(name=props['codebuild_buildstage']['description']),
            build_spec=codebuild.BuildSpec.from_source_filename(
                'cicd/build_specs/build.yml'),
            environment=codebuild.BuildEnvironment(build_image=build_image),
            role=iam_role)


        cdk_test_resourcename = template.substitute(name=props['codebuild_test_resourcestage']['name'])
        cdk_test = codebuild.PipelineProject(
            self, cdk_test_resourcename,
            project_name=cdk_test_resourcename,
            build_spec=codebuild.BuildSpec.from_source_filename('cicd/build_specs/test_cicd.yml'),
            environment=codebuild.BuildEnvironment(build_image=build_image),
            environment_variables={
                'AWS_ACCOUNT': codebuild.BuildEnvironmentVariable(value=source_account_id),
                'CDKENV': codebuild.BuildEnvironmentVariable(value=env),
            },
            description=template.substitute(name=props['codebuild_test_resourcestage']['description']),
            timeout=core.Duration.minutes(pipeline['timeout_minutes']),
            role=iam_role
        )

        cdk_deploy_resourcename = template.substitute(name=props['codebuild_deploy_resourcestage']['name'])
        cdk_deploy = codebuild.PipelineProject(
            self, cdk_deploy_resourcename,
            project_name=cdk_deploy_resourcename,
            build_spec=codebuild.BuildSpec.from_source_filename('cicd/build_specs/deploy_cicd.yml'),
            environment=codebuild.BuildEnvironment(build_image=build_image),
            environment_variables={
                'AWS_ACCOUNT': codebuild.BuildEnvironmentVariable(value=source_account_id),
                'CDKENV': codebuild.BuildEnvironmentVariable(value=env)
            },
            description=template.substitute(name=props['codebuild_deploy_resourcestage']['description']),
            timeout=core.Duration.minutes(pipeline['timeout_minutes']),
            role=iam_role
        )

        cdk_test_name = template.substitute(name=props['codebuild_test_accountstage']['name'])
        test_app = codebuild.PipelineProject(
            self, cdk_test_name,
            project_name=cdk_test_name,
            build_spec=codebuild.BuildSpec.from_source_filename('cicd/build_specs/test_app.yml'),
            environment=codebuild.BuildEnvironment(build_image=build_image),
            environment_variables={
                'AWS_ACCOUNT': codebuild.BuildEnvironmentVariable(value=target_account_id),
                'CDKENV': codebuild.BuildEnvironmentVariable(value=env)
            },
            description=template.substitute(name=props['codebuild_test_accountstage']['description']),
            timeout=core.Duration.minutes(pipeline['timeout_minutes']),
            role=iam_role
        )

        cdk_deploy_name = template.substitute(name=props['codebuild_deploy_accountstage']['name'])
        deploy_app = codebuild.PipelineProject(
            self, cdk_deploy_name,
            project_name=cdk_deploy_name,
            build_spec=codebuild.BuildSpec.from_source_filename('cicd/build_specs/deploy_app.yml'),
            environment=codebuild.BuildEnvironment(build_image=build_image),
            environment_variables={
                'AWS_ACCOUNT': codebuild.BuildEnvironmentVariable(value=target_account_id),
                'CDKENV': codebuild.BuildEnvironmentVariable(value=env),
                'S3_BUCKET': codebuild.BuildEnvironmentVariable(value='project-bucket')
            },
            description=template.substitute(name=props['codebuild_deploy_accountstage']['description']),
            timeout=core.Duration.minutes(pipeline['timeout_minutes']),
            role=iam_role
        )

        source_output = codepipeline.Artifact()
        cdk_build_output = codepipeline.Artifact(template.substitute(name=pipeline['artifact_name']))

        pipeline_name = template.substitute(name=pipeline["pipeline_name"])
        codepipeline.Pipeline(
            self, pipeline_name,
            pipeline_name=pipeline_name,
            role=iam_role,
            stages=[
                codepipeline.StageProps(stage_name="Source",
                                        actions=[
                                            codepipeline_actions.CodeCommitSourceAction(
                                                action_name="Source",
                                                repository=code,
                                                branch=pipeline['branch'],
                                                output=source_output,
                                                role=iam_role)]),
                codepipeline.StageProps(stage_name="Build",
                                        actions=[
                                            codepipeline_actions.CodeBuildAction(
                                                action_name="Build",
                                                project=cdk_build,
                                                input=source_output,
                                                outputs=[cdk_build_output],
                                                role=iam_role)]),
                codepipeline.StageProps(stage_name="Diff_Cicd",
                                        actions=[
                                            codepipeline_actions.CodeBuildAction(
                                                action_name="Diff_Cicd",
                                                project=cdk_test,
                                                input=source_output,
                                                role=iam_role
                                            )]),
                codepipeline.StageProps(stage_name="Deploy_Cicd",
                                        actions=[
                                            codepipeline_actions.CodeBuildAction(
                                                action_name="Deploy_Cicd",
                                                project=cdk_deploy,
                                                input=source_output,
                                                role=iam_role
                                            )
                                        ])
            ]
        )
