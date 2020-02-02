from flask import Flask, request, make_response, Response
from pymongo import MongoClient
from biz_logic import *
import json
import slack

SLACK_BOT_TOKEN = "xoxb-REPLACE_YOUR_SECRET_KEY_HERE"
slack_client = slack.WebClient(token=SLACK_BOT_TOKEN)

app = Flask(__name__)

client = MongoClient()
db = client.yoyoDB
collection_orders = db.orders

ORDERS = {}


@app.route('/')
def default():
    return "working good", 200


slack_client.chat_postMessage(
    channel='CT2MF9BU1',
    text="Howdy user, craving some pizza? :pizza:",
    attachments=bot_intro
)


@app.route("/slack/message_actions", methods=["POST"])
def message_actions():

    form_json = json.loads(request.form["payload"])
    print(form_json)

    if form_json['type'] == 'interactive_message':
        if form_json['callback_id'] == 'order_track':
            step_1(form_json)
        elif form_json['callback_id'] == 'pizza_selection':
            pizza_customization(form_json)
        elif form_json['callback_id'] == 'custm_details':
            get_user_details(form_json)

    elif form_json['type'] == 'view_submission':
        if form_json['view']['callback_id'] == 'user_details':
            finalize_order(form_json)
        elif form_json['view']['callback_id'] == 'order_details':
            show_order(form_json)

    # Send an HTTP 200 response with empty body so Slack knows we're done here
    return make_response("", 200)


def step_1(form):
    # Check to see what the user's selection was and update the message accordingly
    selection = form["actions"][0]["selected_options"][0]["value"]

    if selection == "order":
        new_order(form['user']['id'])
        text = 'Check your DM and respond to proceed'
    else:
        get_order_num(form)
        text = 'Your order details are DM\'ed'

    response = slack_client.chat_postMessage(
        channel=form["channel"]['id'],
        text=text
    )


def new_order(user):
    ORDERS[user] = {}
    slack_client.chat_postMessage(
        channel=user,
        text="Select your :pizza:",
        attachments=[
            {
                "fallback": "Upgrade your Slack client to use messages like these.",
                "color": "#3AA3E3",
                "attachment_type": "default",
                "callback_id": "pizza_selection",
                "actions": [
                    {
                        "name": "order_track",
                        "text": "select your :pizza:",
                        "type": "select",
                        "options": pizza_choices
                    }
                ]
            }
        ]
    )


def pizza_customization(form):
    user = form['user']['id']
    ORDERS[user]['pizza'] = form["actions"][0]["selected_options"][0]["value"]
    print("orders - " + str(ORDERS))
    slack_client.chat_postMessage(
        channel=user,
        text="How do you want your :pizza:",
        attachments=[
            {
                "fallback": "Upgrade your Slack client to use messages like these.",
                "color": "#3AA3E3",
                "attachment_type": "default",
                "callback_id": "custm_details",
                "actions": [
                    {
                        "name": "order_track",
                        "text": "customize it..",
                        "type": "select",
                        "options": custom_choices
                    }
                ]
            }
        ]
    )
    if form["actions"][0]["selected_options"][0]["value"] == 'pineapple':
        attachments = [
            {
                "text": "Pineapple pizza ?",
                "image_url": "https://media.giphy.com/media/l4Ki2obCyAQS5WhFe/giphy.gif"
            }
        ]
    else:
        attachments = [{"text": "nice choice"}]
    response = slack_client.chat_update(
        channel=form["channel"]["id"],
        ts=form["message_ts"],
        attachments=attachments
    )


def get_user_details(form):
    user = form['user']['id']
    ORDERS[user]['custom'] = form["actions"][0]["selected_options"][0]["value"]
    print("orders - " + str(ORDERS))
    open_modal = slack_client.views_open(
        trigger_id=form["trigger_id"],
        view=user_form
    )
    response = slack_client.chat_update(
        channel=form["channel"]["id"],
        ts=form["message_ts"],
        text='...',
        attachments=[]  # empty `attachments` to clear the existing massage attachments
    )


def finalize_order(form):
    user = form['user']['id']
    name = form['view']['state']['values']['name']['name']['value']
    number = form['view']['state']['values']['number']['number']['value']
    address = form['view']['state']['values']['address']['address']['value']
    ORDERS[user]['details'] = {}
    ORDERS[user]['details']['name'] = name
    ORDERS[user]['details']['number'] = number
    ORDERS[user]['details']['address'] = address
    print("orders - " + str(ORDERS))
    data_to_write = {'$set': ORDERS[user]}
    collection_orders.update_one({'user': user}, data_to_write, upsert=True)
    text = 'all done. Sit back and relax, your pizza is on its way.\n Here is your *Order Number - '+str(user) + '*'
    response = slack_client.chat_postMessage(
        channel=user,
        text=text,
        attachments=[]  # empty `attachments` to clear the existing massage attachments
    )
    ORDERS.pop(user)
    print(ORDERS)


def get_order_num(form):
    open_modal = slack_client.views_open(
        trigger_id=form["trigger_id"],
        view=track_order
    )


def show_order(form):
    order_num = form['view']['state']['values']['order_num']['order_num']['value']
    # order_data = collection_orders.find_one({'user': form['user']['id']})
    order_data = collection_orders.find_one({'user': order_num})
    if order_data:
        text = 'Hi ' + str(order_data['details']['name']) + ', here are your order details - \n' \
            + 'Order Number - *' + str(order_data['user']) + '*\n' + 'Pizza - *' + str(order_data['pizza']) + '*\n' \
            + 'additional details - *' + str(order_data['custom']) + '*\n'  \
            + '*Your Pizza in on your way, ETA - 10 mins*'

    else:
        text = 'Order Number not found,\n check and try again...'

    response = slack_client.chat_postMessage(
        channel=form['user']['id'],
        text=text,
        attachments=[]  # empty `attachments` to clear the existing massage attachments
    )


if __name__ == '__main__':
    app.run()
