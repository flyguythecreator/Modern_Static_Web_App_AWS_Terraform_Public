import json
import logging
import os
import traceback
import boto3

# region Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

logger = logging.getLogger()

if logger.hasHandlers():
    # The Lambda environment pre-configures a handler logging to stderr. If a handler is already configured,
    # `.basicConfig` does not execute. Thus we set the level directly.
    logger.setLevel(LOG_LEVEL)
else:
    logging.basicConfig(level=LOG_LEVEL)


# endregion

client = boto3.client('ssm')
response = client.get_parameter(
    Name=os.environ['ssm_path'],
    WithDecryption=False
)

def build_response(http_code, body):
    return {
        "headers": {
            "Cache-Control": "no-cache, no-store",
            "Content-Type": "application/json",
        },
        "statusCode": http_code,
        "body": body,
    }


def lambda_handler(event, context):
    logger.info("API event:")
    logger.info(event)
    try:
        response = {
            "text": "Example response from authenticated api",
            "userPoolId": "",
            "userPoolClientId": "",
            "identityPoolId": "",
            "allowGuestAccess": "",
            "signUpVerificationMethod": "",
            "loginWith": {
                "oauth": {
                    "domain": "",
                    "scopes": "",
                    "redirectSignIn": "",
                    "redirectSignOut": "",
                    "responseType": "",
                },  
            },
        }
        return build_response(200, json.dumps(response))
    except Exception as ex:
        logger.error(traceback.format_exc())
        return build_response(500, "Server Error")


if __name__ == "__main__":
    example_event = {
        "type": "REQUEST",
        "methodArn": "arn:aws:execute-api:us-east-1:123456789012:abcdef123/test/GET/request",
        "resource": "/request",
        "path": "/request",
        "httpMethod": "GET",
        "headers": {
            "X-AMZ-Date": "20170718T062915Z",
            "Accept": "*/*",
            "HeaderAuth1": "headerValue1",
            "CloudFront-Viewer-Country": "US",
            "CloudFront-Forwarded-Proto": "https",
            "CloudFront-Is-Tablet-Viewer": "false",
            "CloudFront-Is-Mobile-Viewer": "false",
            "User-Agent": "...",
        },
        "queryStringParameters": {"QueryString1": "queryValue1"},
        "pathParameters": {},
        "stageVariables": {"StageVar1": "stageValue1"},
        "requestContext": {
            "path": "/request",
            "accountId": "123456789012",
            "resourceId": "05c7jb",
            "stage": "test",
            "requestId": "...",
            "identity": {
                "apiKey": "...",
                "sourceIp": "...",
                "clientCert": {
                    "clientCertPem": "CERT_CONTENT",
                    "subjectDN": "www.example.com",
                    "issuerDN": "Example issuer",
                    "serialNumber": "a1:a1:a1:a1:a1:a1:a1:a1:a1:a1:a1:a1:a1:a1:a1:a1",
                    "validity": {
                        "notBefore": "May 28 12:30:02 2019 GMT",
                        "notAfter": "Aug  5 09:36:04 2021 GMT",
                    },
                },
            },
            "resourcePath": "/request",
            "httpMethod": "GET",
            "apiId": "abcdef123",
        },
    }
    response = lambda_handler(example_event, {})
    print(json.dumps(response))
    # lambda_handler()
