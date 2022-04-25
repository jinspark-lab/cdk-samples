import { Duration, Stack, StackProps } from 'aws-cdk-lib';
import { Construct } from 'constructs';
import * as ecs from 'aws-cdk-lib/aws-ecs';
import * as ecr from 'aws-cdk-lib/aws-ecr';
import * as codecommit from 'aws-cdk-lib/aws-codecommit';
import * as codebuild from 'aws-cdk-lib/aws-codebuild';
import * as codepipeline from 'aws-cdk-lib/aws-codepipeline';
import * as codepipelineActions from 'aws-cdk-lib/aws-codepipeline-actions';
import { EcsApplication } from 'aws-cdk-lib/aws-codedeploy';
// import * as sqs from 'aws-cdk-lib/aws-sqs';

// CI/CD Pipeline from CodeCommit -> CodeBuild -> ECR
export class ContainerCicdStack extends Stack {
  constructor(scope: Construct, id: string, props?: StackProps) {
    super(scope, id, props);

    // The code that defines your stack goes here
    

    const containerRepo = new ecr.Repository(this, 'MyContainerRepo', {
      // imageScanOnPush: true
    });


    const pipeLine = new codepipeline.Pipeline(this, 'MyPipeline', {
      pipelineName: 'MyPipeline'
    });

    // Source
    const repository = new codecommit.Repository(this, 'MyCodeRepo', {
      repositoryName: 'MyCodeRepo',
      description: 'My Code Repository'
    });

    const sourceOutput = new codepipeline.Artifact();
    const sourceAction = new codepipelineActions.CodeCommitSourceAction({
      actionName: 'CodeCommit',
      repository: repository,
      branch: 'master',   //or main
      output: sourceOutput
    });
    pipeLine.addStage({
      stageName: 'Source',
      actions: [sourceAction],
    });
    //

    // Build
    const project = new codebuild.Project(this, 'MyCodeBuild', {
      source: codebuild.Source.codeCommit({ repository }),
      buildSpec: codebuild.BuildSpec.fromSourceFilename('./buildspec.yaml'),
      environment: {
        privileged: true
      },
      environmentVariables: {
        ecr: {
          value: containerRepo.repositoryUri
        },
        tag: {
          value: 'cdk'
        }
      }
    });

    containerRepo.grantPullPush(project);

    const buildOutput = new codepipeline.Artifact();
    const buildAction = new codepipelineActions.CodeBuildAction({
      actionName: 'CodeBuild',
      project: project,
      input: sourceOutput,
      outputs: [buildOutput],
      // executeBatchBuild: true,
      // combineBatchBuildArtifacts: true
    });
    pipeLine.addStage({
      stageName: 'Build',
      actions: [buildAction],
    });
  }
}
