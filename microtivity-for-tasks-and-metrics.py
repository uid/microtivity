#!/usr/bin/python
import json, urllib, time, sys, traceback
from datetime import datetime
from slackclient import SlackClient
from pprint import pprint
import argparse



class Message:
    # timestamp: datetime
    # channel: string starting with "#"
    # text: string
    def __init__(self, timestamp, channel, text):
        self.timestamp = timestamp
        self.channel = channel
        self.text = text

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return "Message(" + repr(self.timestamp) + ", " + repr(self.channel) + ", " + repr(self.text) + ")"

# Fetches the slack notifications tab of the spreadsheet and returns
# a list of Messages.
def getFromSpreadsheet():
    spreadsheetFeed = "https://spreadsheets.google.com/feeds/list/1bM_2amIChF2cn29b3AyF1x5TVVy4e_95TvkbpnEVRFc/omo90wc/public/values?alt=json"
    response = urllib.urlopen(spreadsheetFeed)
    spreadsheetData = json.loads(response.read())
    
    # pprint(spreadsheetData)

    users = {}
    inprogress = set()
    messages = []
    for entry in spreadsheetData["feed"]["entry"]:
        user = entry["gsx$sendto"]["$t"]
        user_id = entry["gsx$userid"]["$t"]
        task = entry["gsx$microtaskormetricquestion"]["$t"]
        state = entry["gsx$state"]["$t"]

        if user not in users.keys() and state == 'send':
            users[user] = dict(state=state, task=task, user_id=user_id)


    pprint(users)

    for user in users:
        sendDirectMessageToSlack(sc, users[user]['user_id'], users[user]['task'])

    # for user in users:
    #     pprint(user)
    #     if user != 'inprogress':
    #         messages.append(Message(channel=user['user_id'], message=user['task']))
    # pprint(messages)

    # messages = []
    # 
    #     try:
    #         timestamp = datetime.strptime(entry["gsx$timestamp"]["$t"], '%m/%d/%Y %H:%M:%S')
    #     except ValueError:
    #         timestamp = datetime.fromtimestamp(0)
    #     channel = entry["gsx$channel"]["$t"]
    #     text = entry["gsx$text"]["$t"]
    #     messages.append(Message(timestamp, channel, text))
    return "messages"

def sendToSlack(sc, messages):
    for m in messages:
        sc.api_call("chat.postMessage", channel=m.channel, text=m.text, username="workflowbot", icon_emoji=":robot_face:")

def sendDirectMessageToSlack(sc, userId, text):
    openIM = sc.api_call("im.open", user=userId);
    channel = openIM["channel"]["id"]
    sc.api_call("chat.postMessage", channel=channel, text=text, username="workflowbot", icon_emoji=":robot_face:")
    

def main():
    parser = argparse.ArgumentParser(description="Forward notifications from Google spreadsheet to Slack")
    parser.add_argument('token', nargs=1, help="Slack authentication test token; to get yours, go to https://api.slack.com/docs/oauth-test-tokens")
    args = parser.parse_args()

    global sc 
    sc = SlackClient(args.token)

    previousMessages = getFromSpreadsheet()
    # while True:
    #     time.sleep(2)
    #     try:
    #         latestMessages = getFromSpreadsheet()
    #         newMessages = [m for m in latestMessages if m not in previousMessages]
    #         if len(newMessages) > 0:
    #             print "sending new messages " + str(newMessages)
    #             # sendToSlack(sc, newMessages)
    #         previousMessages = latestMessages
    #     except:
    #         traceback.print_exc()
    #         # but keep running

main()

