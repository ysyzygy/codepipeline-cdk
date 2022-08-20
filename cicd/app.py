#!/usr/bin/env python3

import os
import json
from string import Template
from aws_cdk import core

from stacks.pipeline.pipeline_stack import PipelineStack

if 'env' in os.environ.keys():
    cdk_env = os.environ['CDKENV']
else:
    cdk_env = 'dev'

json_properties = "resources/" + cdk_env + '.properties.json'
f = open(json_properties, 'r')
properties = json.load(f)
f.close()
tags = properties['project']['tags']
project_name = properties['project']['name']
pipelines = properties['pipelines']
##name: functional name to identify a resource created by aws cdk
template = Template(project_name + '-$name')
app = core.App()


for pipeline in pipelines:
    template2 = Template(project_name +"-"+ pipeline["environment"]+ '-$name')
    PipelineStack(app,
                  template2.substitute(name=pipeline['pipeline_stack_name']),
                  template.substitute(name=properties['repo_name']),
                  pipeline=pipeline,
                  props=properties,
                  template=template2,
                  tags=tags)
app.synth()
