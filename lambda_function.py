import json
import os
import urllib.request 

def lambda_handler(event, context):
    # event is already a Python dict from API Gateway
    issue_url = None

    if "issue" in event and "html_url" in event["issue"]:
        issue_url = event["issue"]["html_url"]
    
    if not issue_url:
        return {"status": "no issue url found", "event": event}
    
    payload = {
        "text": f"Issue Created: {issue_url}"
    }

    data = json.dumps(payload).encode("utf-8")
    
    slack_url = os.environ.get("SLACK_URL")

    req = urllib.request.Request(
        slack_url,
        data=data,
        headers={"Content-Type": "application/json"}
    )

    resp = urllib.request.urlopen(req)
    resp_body = resp.read().decode("utf-8")
    
    return {
        'status': "ok",
        'slack_response': resp_body
    }
