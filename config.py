from common.ssm import SSM


slack_token = SSM(f"/customer-success/tpa/slack-apm-bot/prod/slack.token").secret
