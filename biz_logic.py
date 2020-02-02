
pizza_choices = [
    {
        "text": "Pepperoni :pizza:",
        "value": "pepperoni"
    },
    {
        "text": "Margherita :pizza:",
        "value": "margherita"
    },
    {
        "text": "Pineapple :pizza:",
        "value": "pineapple"
    },
    {
        "text": "Black Olives :pizza:",
        "value": "olive"
    },
    {
        "text": "Tomato :pizza:",
        "value": "tomato"
    },
    {
        "text": "Farm House :pizza:",
        "value": "farm_house"
    }

]

custom_choices = [
    {
        "text": "extra cheese :cheese_wedge:",
        "value": "Echeese"
    },
    {
        "text": "Thin crust",
        "value": "Tcrust"
    },
    {
        "text": "Vegan pizza",
        "value": "vegan"
    },
    {
        "text": "Gluten Free ",
        "value": "no_gluten"
    }
]


bot_intro = [
    {
        "fallback": "Upgrade your Slack client to use messages like these.",
        "color": "#3AA3E3",
        "attachment_type": "default",
        "callback_id": "order_track",
        "actions": [
            {
                "name": "order_track",
                "text": "YoYo Pizza",
                "type": "select",
                "options": [
                    {
                        "text": "Order :pizza:",
                        "value": "order"
                    },
                    {
                        "text": "Track your order",
                        "value": "track"
                    }
                ]
            }
        ]
    }
]

user_form = {
        "type": "modal",
        "callback_id": "user_details",
        "title": {
            "type": "plain_text",
            "text": "My App",
            "emoji": True
        },
        "submit": {
            "type": "plain_text",
            "text": "Submit",
            "emoji": True
        },
        "close": {
            "type": "plain_text",
            "text": "Cancel",
            "emoji": True
        },
        "blocks": [
            {
                "type": "input",
                "block_id": "name",
                "element": {
                    "type": "plain_text_input",
                    "action_id": "name",
                    "placeholder": {
                        "type": "plain_text",
                        "text": "please enter your name"
                    }
                },
                "label": {
                    "type": "plain_text",
                    "text": "Name"
                }
            },
            {
                "type": "input",
                "block_id": "number",
                "element": {
                    "type": "plain_text_input",
                    "action_id": "number",
                    "placeholder": {
                        "type": "plain_text",
                        "text": "10 digit mobile number"
                    }
                },
                "label": {
                    "type": "plain_text",
                    "text": "Mobile Number"
                }
            },
            {
                "type": "input",
                "block_id": "address",
                "element": {
                    "type": "plain_text_input",
                    "action_id": "address",
                    "multiline": True,
                    "placeholder": {
                        "type": "plain_text",
                        "text": "Enter your address"
                    }
                },
                "label": {
                    "type": "plain_text",
                    "text": "Address"
                }
            }
        ]
    }

track_order = {
    "type": "modal",
    "callback_id": "order_details",
    "title": {
        "type": "plain_text",
        "text": "My App",
        "emoji": True
    },
    "submit": {
        "type": "plain_text",
        "text": "Submit",
        "emoji": True
    },
    "close": {
        "type": "plain_text",
        "text": "Cancel",
        "emoji": True
    },
    "blocks": [
        {
            "type": "input",
            "block_id": "order_num",
            "element": {
                "type": "plain_text_input",
                "action_id": "order_num",
                "placeholder": {
                    "type": "plain_text",
                    "text": "please enter Order Number"
                }
            },
            "label": {
                "type": "plain_text",
                "text": "Order Number"
            }
        }
    ]
}

