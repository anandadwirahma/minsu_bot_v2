from linebot.models import ConfirmTemplate
from linebot.models import MessageTemplateAction
from linebot.models import PostbackTemplateAction
from linebot.models import TemplateSendMessage

confirmations = [{
    "id":"example",
    "payload":TemplateSendMessage(
        alt_text='Confirm template',
        template=ConfirmTemplate(
            text='Are you sure?',
            actions=[
                PostbackTemplateAction(
                    label='postback',
                    text='postback text',
                    data='action=buy&itemid=1'
                ),
                MessageTemplateAction(
                    label='message',
                    text='message text'
                )
            ]
        )
    )
}]

def composeConfirm(alt_text, text, option1, option2):
    if option1['type'] == "postback":
        opt1_payload = PostbackTemplateAction(
                    label=option1['label'],
                    #text=option1['text'],
                    data=option1['data']
        )
    elif option1['type'] == "message":
        opt1_payload = MessageTemplateAction(
                    label=option1['label'],
                    text=option1['text']
        )

    if option2['type'] == "postback":
        opt2_payload = PostbackTemplateAction(
                    label=option2['label'],
                    #text=option2['text'],
                    data=option2['data']
        )
    elif option2['type'] == "message":
        opt2_payload = MessageTemplateAction(
                    label=option2['label'],
                    text=option2['text']
        )

    payload = TemplateSendMessage(
        alt_text=alt_text,
        template=ConfirmTemplate(
            text=text,
            actions=[opt1_payload, opt2_payload]
        )
    )
    return payload
