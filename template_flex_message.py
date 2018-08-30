

def flextemplateReceipt(msisdn, contentitem1, contentitem2, footer):

    data = {
        "to": msisdn,
        "messages": [{
            "type": "flex",
            "altText": "Order Receipt",
            "contents": {
                "type": "bubble",
                "styles": {
                    "footer": {
                        "separator": True
                    }
                },
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [{
                        "type": "text",
                        "text": "RECEIPT",
                        "weight": "bold",
                        "color": "#1DB446",
                        "size": "sm"
                    },
                        {
                        "type": "text",
                        "text": "Minsu Store",
                        "weight": "bold",
                        "size": "xxl",
                        "margin": "md"
                    },
                        {
                        "type": "text",
                        "text": "JL.Tebet Dalam 3A, Depok, Jakarta",
                        "size": "xs",
                        "color": "#aaaaaa",
                        "wrap": True
                    },
                        {
                        "type": "separator",
                        "margin": "xxl"
                    },
                        {
                        "type": "box",
                        "layout": "vertical",
                        "margin": "xxl",
                        "spacing": "sm",
                        "contents": [
                            #** Area for Content Item 1 **#
                            contentitem1,
                            {
                                "type": "separator",
                                "margin": "xxl"
                            },
                            #** Area for Content Footer Item 2 **#
                            contentitem2,
                            {
                                "type": "box",
                                "layout": "horizontal",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": "TOTAL",
                                        "size": "sm",
                                        "color": "#555555"
                                    },
                                    {
                                        "type": "text",
                                        "text": "$7.31",
                                        "size": "sm",
                                        "color": "#111111",
                                        "align": "end"
                                    }
                                ]
                            }
                        ]
                    },
                    {
                        "type": "separator",
                        "margin": "xxl"
                    },
                    #** Area for Content Footer **#
                    footer
                ]}
            }
        }]
    }

    return data
