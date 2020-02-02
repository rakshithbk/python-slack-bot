# python-slack-bot
Pizza ordering Slack chatbot

### Slack App creation -
- Signup on Slack and build a [new app](https://api.slack.com/apps)
- Enable "Incoming Webhooks" 
- Enable "Interactive Components" and enter your servers address for "Request URL" (publicly accessible url where your python scripts are running). ex - `http://mychatbot.com/slack/message_action`
- In "OAuth and Permissions" provide these Scope element access -
  `chat:write`
  `incoming-webhooks`
- Add the app in your desired Channel.

Copy the Bot __User OAuth Access Token__ and replace it in the code.
### Python Requirements - 
`pip install flask pymongo slackclient`


If you are like me, running flask on Raspberry pi (or any local machine) that is being firewall/NATs, use **SSH Tunneling**.
I have used [this](https://localhost.run/) simple service that works without any installations.
