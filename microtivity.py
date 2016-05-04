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
    spreadsheetFeed = "https://spreadsheets.google.com/feeds/list/1bM_2amIChF2cn29b3AyF1x5TVVy4e_95TvkbpnEVRFc/ojh9cqh/public/values?alt=json"
    response = urllib.urlopen(spreadsheetFeed)
    spreadsheetData = json.loads(response.read())
    #pprint(spreadsheetData)
    messages = []
    for entry in spreadsheetData["feed"]["entry"]:
        try:
            timestamp = datetime.strptime(entry["gsx$timestamp"]["$t"], '%m/%d/%Y %H:%M:%S')
        except ValueError:
            timestamp = datetime.fromtimestamp(0)
        channel = entry["gsx$channel"]["$t"]
        text = entry["gsx$text"]["$t"]
        messages.append(Message(timestamp, channel, text))
    return messages

def sendToSlack(sc, messages):
    for m in messages:
        sc.api_call("chat.postMessage", channel=m.channel, text=m.text, username="workflowbot", icon_emoji=":robot_face:")

def main():
    parser = argparse.ArgumentParser(description="Forward notifications from Google spreadsheet to Slack")
    parser.add_argument('token', nargs=1, help="Slack authentication test token; to get yours, go to https://api.slack.com/docs/oauth-test-tokens")
    args = parser.parse_args()

    sc = SlackClient(args.token)

    previousMessages = getFromSpreadsheet()
    while True:
        time.sleep(2)
        try:
            latestMessages = getFromSpreadsheet()
            newMessages = [m for m in latestMessages if m not in previousMessages]
            if len(newMessages) > 0:
                print "sending new messages " + str(newMessages)
                sendToSlack(sc, newMessages)
            previousMessages = latestMessages
        except:
            traceback.print_exc()
            # but keep running

main()

