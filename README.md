
This script runs forever, transferring notifications from the microtovity todo spreadsheet (on the slack notifications tab) to Slack itself.

To run it:

1. Install the Slack API library for Python:

        sudo pip install slackclient

2. [Get a Slack authentication token](https://api.slack.com/docs/oauth-test-tokens)

3. Run the script passing your token on the command line:

        ./microtivity.py xoxp-3131...e08a2

