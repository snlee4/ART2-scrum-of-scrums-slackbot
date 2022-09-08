from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from slack_bolt.adapter.socket_mode import SocketModeHandler
from config import slack_token
from slack_sdk.http_retry.builtin_handlers import RateLimitErrorRetryHandler


# SLACK MESSAGING DOCS
# https://api.slack.com/methods/chat.postMessage
# THREADING SPECIFIC: https://api.slack.com/messaging/sending#threading

# TODO: find out what responses Slack returns for status codes
# TODO: add retries - done

def post_initial_message(channel_id):
    client = WebClient(token=slack_token)
    INITIAL_MESSAGE = "<!here> *Scrum of Scrums:* Please review your Program Board and respond on your team's thread with :white_check_mark: or :x: regarding the status of each item. If you add an :x: please provide additional explanation.\nIf further discussion is needed with another team, please let us know how we can support and use the SoS time to discuss.\nReminder that you can view the <https://indd.adobe.com/view/aff7a463-c66e-4467-bb5d-403f365c2996|JIRA Align Reference Guide> *(Program board Page 16)*"
    response = client.chat_postMessage(
        channel=channel_id,
        text=INITIAL_MESSAGE
    )
    if response['ok'] == False:
            print(f"Post failed, initial message not sent")
            print(response)
            exit()


# initialize client with token

### verify post_parent_message has replaced post_initial_message in below 

def post_parent_message(channel_id, teams): 
    client = WebClient(token=slack_token)
    list_of_slack_messages = []
    for team in teams:
        PARENT_MESSAGE = f"{team}"
        response = client.chat_postMessage(
            channel=channel_id,
            text=PARENT_MESSAGE
        )
        if response['ok'] == False:
            print(f"Post failed, {team} message not sent")
            print(response)
            exit()
        parent_message_ts = response['ts']
        list_of_slack_messages.append(parent_message_ts)
    return list_of_slack_messages


# example response from postMessage endpoint
#
# {'ok': True, 'channel': 'C03JV0H88F8', 'ts': '1655915055.960099', 'message': {'bot_id': 'B03K3UJU8QL', 'type': 'message', 'text': 'Hello world!', 'user': 'U03JLUDHE8P', 'ts': '1655915055.960099', 'app_id': 'A03K156JS1Z', 'team': 'TPN9PB5PB', 'bot_profile': {'id': 'B03K3UJU8QL', 'app_id': 'A03K156JS1Z', 'name': 'SoS Test', 'icons': {'image_36': 'https://a.slack-edge.com/80588/img/plugins/app/bot_36.png', 'image_48': 'https://a.slack-edge.com/80588/img/plugins/app/bot_48.png', 'image_72': 'https://a.slack-edge.com/80588/img/plugins/app/service_72.png'}, 'deleted': False, 'updated': 1654804460, 'team_id': 'TPN9PB5PB'}, 'blocks': [{'type': 'rich_text', 'block_id': '9f4', 'elements': [{'type': 'rich_text_section', 'elements': [{'type': 'text', 'text': 'Hello world!'}]}]}]}}
#
#


def threaded_messages(channel_id, list_of_slack_messages):
    client = WebClient(token=slack_token)
    for message_ts in list_of_slack_messages:
        thread_messages = ['*Features*','*Dependencies*','*Program Objectives*']
        for text in thread_messages:
            response = client.chat_postMessage(
                channel=channel_id,
                thread_ts=message_ts,
                text=text
            )
        # This handler does retries when HTTP status 429 is returned
        from slack_sdk.http_retry.builtin_handlers import RateLimitErrorRetryHandler
        rate_limit_handler = RateLimitErrorRetryHandler(max_retry_count=1)

        # Enable rate limited error retries as well
        client.retry_handlers.append(rate_limit_handler)


