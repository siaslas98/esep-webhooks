import json
import os
import urllib.request 

def lambda_handler(event, context):

    # Parse GitHub webhook if wrapped by API Gateway
    if "body" in event and isinstance(event["body"], str):
        try:
            event = json.loads(event["body"])
        except:
            pass   
    
    # Only react when an issue is created (opened)
    if event.get("action") != "opened":
        return {
        "statusCode": 200,
        "body": json.dumps({"status": "ignored"})
    }

    issue_url = None

    if "issue" in event and "html_url" in event["issue"]:
        issue_url = event["issue"]["html_url"]
    
    if not issue_url:
        return {
            "statusCode": 200,
            "body": json.dumps({"status": "no issue url found"})
        }
    
    payload = {
        "text": f"Issue Created: {issue_url}"
    }

    slack_url = os.environ.get("SLACK_URL")
    data = json.dumps(payload).encode("utf-8")

    req = urllib.request.Request(
        slack_url,
        data=data,
        headers={"Content-Type": "application/json"}
    )

    resp = urllib.request.urlopen(req)
    resp_body = resp.read().decode("utf-8")
    
    return {
        "statusCode": 200,
        "body": json.dumps({
            "status": "ok",
            "slack_response": resp_body
        })
    }