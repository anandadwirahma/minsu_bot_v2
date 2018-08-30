from linebot.models import BaseSize
from linebot.models import ImagemapArea
from linebot.models import ImagemapSendMessage
from linebot.models import MessageImagemapAction
from linebot.models import URIImagemapAction

imagemaps = [
    {
        "id":"example",
        "payload": ImagemapSendMessage(
            base_url='https://example.com/base',
                alt_text='this is an imagemap',
                base_size=BaseSize(height=1040, width=1040),
                actions=[
                    URIImagemapAction(
                        link_uri='https://example.com/',
                        area=ImagemapArea(
                            x=0, y=0, width=520, height=1040
                        )
                    ),
                    MessageImagemapAction(
                        text='hello',
                        area=ImagemapArea(
                            x=520, y=0, width=520, height=1040
                        )
                    )
                ]
            )
    },{
        "id":"pulsa",
        "payload": ImagemapSendMessage(
            base_url='https://bangjoni.com/pulsa_images/pulsa1',
                alt_text='Rich Menu Pulsa',
                base_size=BaseSize(height=701, width=1040),
                actions=[
                    MessageImagemapAction(
                        text='lima ribu',
                        area=ImagemapArea(
                            x=0, y=0, width=346, height=350
                        )
                    ),
                    MessageImagemapAction(
                        text='sepuluh ribu',
                        area=ImagemapArea(
                            x=346, y=0, width=693, height=350
                        )
                    ),
                    MessageImagemapAction(
                        text='dua puluh ribu',
                        area=ImagemapArea(
                            x=693, y=0, width=1040, height=350
                        )
                    ),
                    MessageImagemapAction(
                        text='dua puluh lima ribu',
                        area=ImagemapArea(
                            x=0, y=350, width=346, height=701
                        )
                    ),
                    MessageImagemapAction(
                        text='lima puluh ribu',
                        area=ImagemapArea(
                            x=346, y=350, width=693, height=701
                        )
                    ),
                    MessageImagemapAction(
                        text='seratus ribu',
                        area=ImagemapArea(
                            x=693, y=350, width=1040, height=701
                        )
                    )
                ]
            )
    },{
        "id":"pulsa_xl",
        "payload": ImagemapSendMessage(
            base_url='https://bangjoni.com/pulsa_images/pulsaxl1',
                alt_text='Rich Menu Pulsa',
                base_size=BaseSize(height=701, width=1040),
                actions=[
                    MessageImagemapAction(
                        text='lima ribu',
                        area=ImagemapArea(
                            x=0, y=0, width=346, height=350
                        )
                    ),
                    MessageImagemapAction(
                        text='sepuluh ribu',
                        area=ImagemapArea(
                            x=346, y=0, width=693, height=350
                        )
                    ),
                    MessageImagemapAction(
                        text='tidak tersedia',
                        area=ImagemapArea(
                            x=693, y=0, width=1040, height=350
                        )
                    ),
                    MessageImagemapAction(
                        text='dua puluh lima ribu',
                        area=ImagemapArea(
                            x=0, y=350, width=346, height=701
                        )
                    ),
                    MessageImagemapAction(
                        text='lima puluh ribu',
                        area=ImagemapArea(
                            x=346, y=350, width=693, height=701
                        )
                    ),
                    MessageImagemapAction(
                        text='seratus ribu',
                        area=ImagemapArea(
                            x=693, y=350, width=1040, height=701
                        )
                    )
                ]
            )
    },{
        "id":"bjpay_register",
        "payload": ImagemapSendMessage(
            base_url='https://www.bangjoni.com/line_images/bjpay_register2',
                alt_text='Rich Menu BJPay Register',
                base_size=BaseSize(height=466, width=1040),
                actions=[
                    MessageImagemapAction(
                        text='bjpay register',
                        area=ImagemapArea(
                            x=0, y=0, width=1040, height=466
                        )
                    )
                ]
            )
    },{
        "id":"bjpay_deposit",
        "payload": ImagemapSendMessage(
            base_url='https://www.bangjoni.com/line_images/bjpay_deposit',
                alt_text='Rich Menu BJPay Deposit',
                base_size=BaseSize(height=466, width=1040),
                actions=[
                    MessageImagemapAction(
                        text='va permata',
                        area=ImagemapArea(
                            x=0, y=0, width=346, height=466
                        )
                    ),
                    MessageImagemapAction(
                        text='transfer mandiri',
                        area=ImagemapArea(
                            x=346, y=0, width=693, height=466
                        )
                    ),
                    MessageImagemapAction(
                        text='transfer bca',
                        area=ImagemapArea(
                            x=693, y=0, width=1040, height=466
                        )
                    )
                ]
            )
    },{
        "id":"payment_tiketux",
        "payload": ImagemapSendMessage(
            base_url='https://www.bangjoni.com/line_images/payment_tiketux1',
                alt_text='Rich Menu Payment Tiketux',
                base_size=BaseSize(height=701, width=1040),
                actions=[
                    MessageImagemapAction(
                        text='atm',
                        area=ImagemapArea(
                            x=0, y=0, width=347, height=232
                        )
                    ),
                    MessageImagemapAction(
                        text='kartu kredit',
                        area=ImagemapArea(
                            x=347, y=0, width=692, height=232
                        )
                    ),
                    MessageImagemapAction(
                        text='cimb clicks',
                        area=ImagemapArea(
                            x=692, y=0, width=1040, height=232
                        )
                    ),
                    MessageImagemapAction(
                        text='mandiri ecash',
                        area=ImagemapArea(
                            x=0, y=232, width=347, height=463
                        )
                    ),
                    MessageImagemapAction(
                        text='mandiri clickpay',
                        area=ImagemapArea(
                            x=347, y=232, width=692, height=463
                        )
                    ),
                    MessageImagemapAction(
                        text='bca klikpay',
                        area=ImagemapArea(
                            x=692, y=232, width=1040, height=463
                        )
                    ),
                    MessageImagemapAction(
                        text='tcash',
                        area=ImagemapArea(
                            x=0, y=463, width=347, height=701
                        )
                    ),
                    MessageImagemapAction(
                        text='xl tunai',
                        area=ImagemapArea(
                            x=347, y=463, width=692, height=701
                        )
                    ),
                    MessageImagemapAction(
                        text='indomaret',
                        area=ImagemapArea(
                            x=692, y=463, width=1040, height=701
                        )
                    )
                ]
            )
    },{
        "id":"payment_tiketdotcom",
        "payload": ImagemapSendMessage(
            base_url='https://www.bangjoni.com/line_images/payment_tiketux1',
                alt_text='Rich Menu Payment Tiketdotcom',
                base_size=BaseSize(height=701, width=1040),
                actions=[
                    MessageImagemapAction(
                        text='atm',
                        area=ImagemapArea(
                            x=0, y=0, width=346, height=230
                        )
                    ),
                    MessageImagemapAction(
                        text='kartu kredit',
                        area=ImagemapArea(
                            x=346, y=0, width=692, height=230
                        )
                    ),
                    MessageImagemapAction(
                        text='cimb clicks',
                        area=ImagemapArea(
                            x=692, y=0, width=1040, height=230
                        )
                    ),
                    MessageImagemapAction(
                        text='mandiri ecash',
                        area=ImagemapArea(
                            x=0, y=230, width=346, height=466
                        )
                    ),
                    MessageImagemapAction(
                        text='mandiri clickpay',
                        area=ImagemapArea(
                            x=346, y=230, width=692, height=466
                        )
                    ),
                    MessageImagemapAction(
                        text='bca klikpay',
                        area=ImagemapArea(
                            x=692, y=230, width=1040, height=466
                        )
                    )
                ]
            )
    },{
        "id":"payment_token",
        "payload": ImagemapSendMessage(
            base_url='https://bangjoni.com/pln_images/pln1',
                alt_text='Rich Menu Payment Token PLN',
                base_size=BaseSize(height=701, width=1040),
                actions=[
                    MessageImagemapAction(
                        text='dua puluh',
                        area=ImagemapArea(
                            x=0, y=0, width=720, height=350
                        )
                    ),
                    MessageImagemapAction(
                        text='lima puluh',
                        area=ImagemapArea(
                            x=720, y=0, width=1040, height=350
                        )
                    ),
                    MessageImagemapAction(
                        text='seratus',
                        area=ImagemapArea(
                            x=0, y=350, width=720, height=351
                        )
                    ),
                    MessageImagemapAction(
                        text='dua ratus',
                        area=ImagemapArea(
                            x=720, y=350, width=1040, height=351
                        )
                    )
                ]
            )
    }
]