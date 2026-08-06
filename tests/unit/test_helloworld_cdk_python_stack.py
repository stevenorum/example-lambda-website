import aws_cdk as core
import aws_cdk.assertions as assertions

from helloworld_cdk_python.helloworld_cdk_python_stack import HelloworldCdkPythonStack

# example tests. To run these tests, uncomment this file along with the example
# resource in helloworld_cdk_python/helloworld_cdk_python_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = HelloworldCdkPythonStack(app, "helloworld-cdk-python")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
