from linebot.models import CarouselColumn
from linebot.models import CarouselTemplate
from linebot.models import MessageTemplateAction
from linebot.models import PostbackTemplateAction
from linebot.models import TemplateSendMessage
from linebot.models import URITemplateAction

carousels = [{
    "id" : "main_menu",
    "payload" : TemplateSendMessage(
        alt_text='Menu Utama',
        template=CarouselTemplate(
            columns=[
                CarouselColumn(
                    thumbnail_image_url='https://bangjoni.com/v2/carousel/zomato/indonesia.png',
                    title='Menu Product & Services',
                    text='Prodcut & Services',
                    actions=[
                        PostbackTemplateAction(
                            label='Pilih Category',
                            data='evt=category'
                        ),
                        PostbackTemplateAction(
                            label='Complain',
                            data='evt=complain'
                        ),
                        PostbackTemplateAction(
                            label='History Order',
                            data='evt=historyorder'
                        )
                    ]
                )
            ]
        )
    )
},
{
    "id" : "chart_confirm",
    "payload" : TemplateSendMessage(
        alt_text='Konfirmasi Keranjang Belanja',
        template=CarouselTemplate(
            columns=[
                CarouselColumn(
                    thumbnail_image_url='',
                    title='Konfirmasi Keranjang Belanja',
                    text='Ada yang mau dibeli lagii siiis ?',
                    actions=[
                        PostbackTemplateAction(
                            label='Kembali Ke Category',
                            data='evt=category'
                        ),
                        PostbackTemplateAction(
                            label='Kembali Ke Product',
                            data='evt=complain'
                        ),
                        PostbackTemplateAction(
                            label='Lihat Keranjang',
                            data='evt=historyorder'
                        )
                    ]
                )
            ]
        )
    )
}]

def composeCarousel(alt_text, columns):
    carousel_columns = []
    for column in columns:
        actions = []
        for action in column['actions']:
            if action['type'] == 'postback':
                actions.append(PostbackTemplateAction(label=action['label'], data=action['data']))
            elif action['type'] == 'message':
                actions.append(MessageTemplateAction(label=action['label'], text=action['text']))
            elif action['type'] == 'uri':
                actions.append(URITemplateAction(label=action['label'], uri=action['uri']))
        col = CarouselColumn(thumbnail_image_url=column['thumbnail_image_url'], title=column['title'], text=column['text'], actions=actions)
        carousel_columns.append(col)
    template = TemplateSendMessage(alt_text=alt_text, template=CarouselTemplate(columns=carousel_columns))
    return template