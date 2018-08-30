import json
import os
import sys
from StringIO import StringIO

# import logging
import gevent.monkey
import redis
from flask import Flask, request
from gevent import pywsgi
from rivescript import RiveScript

from models.redis_storage import RedisSessionStorage

gevent.monkey.patch_all()


rs = RiveScript(session_manager=RedisSessionStorage(),)

#-- In windows --#
full_path = os.path.realpath(__file__)
rs.load_directory(os.path.dirname(full_path)+"/rivescript/")
#-- In unix command --#
#rs.load_directory("/home/luky/nanda_titip/bjtech_bbmbot/rivescript")

rs.sort_replies()

redisconn = redis.StrictRedis()

if __name__==  "__main__":
    print "--- Rivescript NLP is online ---"

    app = Flask(__name__)

    @app.route('/reply', methods=['POST'])
    def reply():
        content = request.get_json()
        print "Incoing Message In Rivescript -->> ", content
        return rs.reply(content['msisdn'], content['ask'])

    @app.route('/trigger', methods=['POST'])
    def trigger():
        content = request.get_json()
        print "trigger:", content
        rs.stream(content['trigger'])
        rs.sort_replies()

        trigger = redisconn.get("trigger")
        if trigger is not None:
            lasttrigger = json.loads(trigger)
            lasttrigger[len(lasttrigger)] = content['trigger']
            redisconn.set("trigger", json.dumps(lasttrigger))
        else:
            lasttrigger = {}
            lasttrigger[0] = content['trigger']
            redisconn.set("trigger", json.dumps(lasttrigger))
        return "OK"

    @app.route('/getvar', methods=['POST'])
    def getvar():
        content = request.get_json()
        print "getvar:", content
        return rs.get_uservar(content['msisdn'], content['param'])

    @app.route('/setvar', methods=['POST'])
    def setvar():
        content = request.get_json()
        print "setvar:", content
        rs.set_uservar(content['msisdn'], content['param'], content['value'])
        return "OK"

    @app.route('/checkscript', methods=['POST'])
    def checkscript():
        content = request.get_json()
        print "checkscript:", content
        old_stdout = sys.stdout
        sys.stdout = mystdout = StringIO()
        rss = RiveScript()
        rss.load_file(content['filename'])
        print "OK"
        sys.stdout = old_stdout
        print "----->", mystdout.getvalue()
        rss = None
        return mystdout.getvalue()

    @app.route('/updatescript', methods=['POST'])
    def updatescript():
        content = request.get_json()
        print "updatescript", content
        reloadRive()
        return "OK"

    #thread.start_new_thread(start_scheduler, ())


    print "starting gevent wsgi..."
    pywsgi.WSGIServer(('', 3020), app).serve_forever()
