from linebot.models import ButtonsTemplate
from linebot.models import MessageTemplateAction
from linebot.models import PostbackTemplateAction
from linebot.models import TemplateSendMessage
from linebot.models import URITemplateAction

imgbuttons = [{
    "id":"example",
    "payload": TemplateSendMessage(
        alt_text='Buttons template',
        template=ButtonsTemplate(
            thumbnail_image_url='https://example.com/image.jpg',
            title='Menu',
            text='Please select',
            actions=[
                PostbackTemplateAction(
                    label='postback',
                    text='postback text',
                    data='action=buy&itemid=1'
                ),
                MessageTemplateAction(
                    label='message',
                    text='message text'
                ),
                URITemplateAction(
                    label='uri',
                    uri='http://example.com/'
                )
            ]
        )
    )
},{
    "id":"bjpay_register",
    "payload": TemplateSendMessage(
        alt_text='Register BJPAY',
        template=ButtonsTemplate(
            thumbnail_image_url='https://bangjoni.com/v2/carousel/greetings/bjpay.png',
            title='Register BJPAY',
            text='Buat BJPAY biar kamu gampang transaksinya',
            actions=[
                MessageTemplateAction(
                    label='Register',
                    text='bjpay register'
                )
            ]
        )
    )
},{
    "id":"uber_after_auth",
    "payload": TemplateSendMessage(
        alt_text='Uber',
        template=ButtonsTemplate(
            thumbnail_image_url='https://bangjoni.com/v2/carousel/images/uber.png',
            title='Pesen Uber',
            text='Account Uber kamu udah terhubung',
            actions=[
                MessageTemplateAction(
                    label='Lanjut Pesen',
                    text='uber'
                )
            ]
        )
    )
##--- DEV TIKET.COM 5 DES ---##
},{
    "id":"button_pp",
    "payload":TemplateSendMessage(
        alt_text="Button PP",
        template=ButtonsTemplate(
            thumbnail_image_url='',
            title='Pesen Pesawat',
            text='Untuk PP atau sekali jalan',
            actions=[
                MessageTemplateAction(
                    label='Pulang Perga',
                    text='pulang pergi'
                ),
                MessageTemplateAction(
                    label='Sekali Jalan',
                    text='sekali jalan'
                )
            ]
        )
    )
},{
    "id":"dwp ticket 2day",
    "payload":TemplateSendMessage(
        alt_text="Button DWP",
        template=ButtonsTemplate(
            # thumbnail_image_url='https://bangjoni.com/v2/carousel/greetings/bjpay.png',
            title='Ticket 2 Day Pass',
            text='Untuk 2 hari',
            actions=[
                # MessageTemplateAction(
                #     label='GA Early Entry',
                #     text='GA Early Entry'
                # ),
                MessageTemplateAction(
                    label='GA',
                    text='GA'
                ),
                MessageTemplateAction(
                    label='VIP Gold',
                    text='VIP Gold'
                )
            ]
        )
    )
},{
    "id":"dwp ticket ga early",
    "payload":TemplateSendMessage(
        alt_text="Button DWP",
        template=ButtonsTemplate(
            # thumbnail_image_url='https://bangjoni.com/v2/carousel/greetings/bjpay.png',
            title='GA Early Entry (Entry Before 7pm)',
            text='Presale 1 1000k (incl tax) Presale 2 1125k (incl tax)',
            actions=[
                MessageTemplateAction(
                    label='Presale 1',
                    text='presale 1'
                ),
                MessageTemplateAction(
                    label='Presale 2',
                    text='Presale 2'
                )
            ]
        )
    )
},{
    "id":"dwp ticket ga",
    "payload":TemplateSendMessage(
        alt_text="Button DWP",
        template=ButtonsTemplate(
            # thumbnail_image_url='https://bangjoni.com/v2/carousel/greetings/bjpay.png',
            title='GA',
            text='Presale 2 1150k,Presale 3 1275k,Presale 4 1400k',
            actions=[
                MessageTemplateAction(
                    label='Presale 2',
                    text='presale 2'
                ),
                MessageTemplateAction(
                    label='Presale 3',
                    text='Presale 3'
                ),
                MessageTemplateAction(
                    label='Presale 4',
                    text='Presale 4'
                )
            ]
        )
    )
},{
    "id":"dwp ticket vip",
    "payload":TemplateSendMessage(
        alt_text="Button DWP",
        template=ButtonsTemplate(
            # thumbnail_image_url='https://bangjoni.com/v2/carousel/greetings/bjpay.png',
            title='VIP Gold',
            text='Presale 2500k (incl tax) Normal 2875k (incl tax)',
            actions=[
                MessageTemplateAction(
                    label='Presale 1',
                    text='presale 1'
                ),
                MessageTemplateAction(
                    label='Presale 2',
                    text='Presale 2'
                )
            ]
        )
    )
}]
##---------------------------##
def compose_img_buttons(alt_text, thumbnail_url, title, description, actions):
    img_actions = []
    for action in actions :
        if action['type'] == 'postback':
            img_actions.append(PostbackTemplateAction(label=action['label'], data=action['data']))
        elif action['type'] == 'message':
            img_actions.append(MessageTemplateAction(label=action['label'], text=action['text']))
        elif action['type'] == 'uri':
            img_actions.append(URITemplateAction(label=action['label'], uri=action['uri']))
    return TemplateSendMessage(
        alt_text=alt_text,
        template=ButtonsTemplate(
            thumbnail_image_url=thumbnail_url,
            title=title,
            text=description,
            actions=img_actions
        ))