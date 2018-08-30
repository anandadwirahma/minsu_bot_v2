from gevent import pywsgi
from flask import Flask, render_template, request, redirect
from milki_tasks import doworker,doworker_postmsg

#- import logging
import gevent.monkey
import json
gevent.monkey.patch_all()


if __name__ == "__main__":
    print "--- Line Milki Bot is Online ---"

    app = Flask(__name__)

    @app.route('/linemilki', methods=['POST'])
    def postwebhook():
        content = request.get_json()
        print content
        doworker.delay(content)
        return "OK"

    @app.route('/milkipostmsg', methods=['POST'])
    def postmsg():
        content = request.get_json()
        print content
        doworker_postmsg.delay(content)
        return ""


    print "starting gevent wsgi..."
    pywsgi.WSGIServer(('', 8020), app).serve_forever()
