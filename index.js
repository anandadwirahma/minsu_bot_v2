var express = require('express');
var path = require('path');
var mysql = require('mysql');
var redis = require('redis');
var bodyParser = require('body-parser');
var fs = require('fs');
var MongoClient = require('mongodb').MongoClient;
// var formidable = require('formidable');
var fileUpload = require('express-fileupload');
// var multipart = require('connect-multiparty');
// var multipartMiddleware = multipart();
var randomstring = require("randomstring");
var dateformat = require('dateformat');
var dateandtime = require('date-and-time');
var app = express();
var myConnection = require('express-myconnection')
var request = require('request');
var math = require('math');
var datediff = require('date-diff');
var cryptoJs = require('crypto-js');
var passphrase = 'fcf8afd67e96fa3366dd8eafec8bcace';
querystring = require('querystring');
var mail = require('./mail.js');
var sendmail = new mail();
//keyevent/jenengOA/botid
app.use(fileUpload());
app.use('/static', express.static('public'));
app.use(bodyParser.json({
    verify(req, res, buf) {
        req.rawBody = buf
    }
}))

var id = '';
var channel_id = "1529346409";
var user_id = '';
// app.use(multer({
//     dest: “./uploads/”
// }));


// create application/json parser
var jsonParser = bodyParser.json();
// create application/x-www-form-urlencoded parser
var urlencodedParser = bodyParser.urlencoded({extended: false});
var dbOptions = {
    host: "localhost",
    user: "root",
    password: "cikapali99",
    port: "3306",
    database: "keyeventdb",
    multipleStatements: "true"
}
app.use(myConnection(mysql, dbOptions, 'pool'))
// var conMysql = mysql.createConnection({
//   host: "127.0.0.1",
//   user: "dashkeyevent",
//   // password: "",
//   // database: "keyevent_dashboard"
//   password: "P@ssw0rd",
//   database: "keyeventdb"
// });

// var pool = mysql.createPool({
//     connectionLimit: 100, //important
//     host: '127.0.0.1',
//     user: 'dashkeyevent',
//     password: 'P@ssw0rd',
//     database: 'keyeventdb',
//     debug: false
// });

const client = redis.createClient({
    host: '127.0.0.1',
    port: '6379',
    db: 0
});

var urlmongo = "mongodb://127.0.0.1:27017/";


app.get('/index', function (req, res) {
    console.log("get " + req.query.id);
    id = req.query.id;
    res.sendFile(path.join(__dirname + '/views/advanced.html'));
})

app.get('/credentials', function (req, res) {
    console.log("get " + req.query.id);
    id = req.query.id;
    res.sendFile(path.join(__dirname + '/views/credentials.html'));
})

app.get('/index/getDataForEdit', function (req, res) {
    req.getConnection(function (error, conMysql) {
        var sql = "select * from scheduleevent where botid = '" + id + "'";
        console.log(sql);
        conMysql.query(sql, function (err, rows, fields) {
            res.send(JSON.stringify(rows));
        });
    });
    // conMysql.end();
})

app.get('/index/getDataForNew', function (req, res) {
    req.getConnection(function (error, conMysql) {
        botid = randomstring.generate(8);
        query = "select 1 as is_exists_botid from scheduleevent where botid ='" + botid + "'"
        conMysql.query(query, function (err, result, fields) {
            if (err)
                throw err;
            console.log(result);
            obj = {
                "botid": botid
            }
            if (result.length == 0) {
                res.send(JSON.stringify(obj));
            }
        });
    })
    // conMysql.end();
})

app.get('/credentials/getDataForCredentials', function (req, res) {
    req.getConnection(function (error, conMysql) {
        // clientid = req.query.clientid
        console.log(req.query);
        var userId = req.query.userId;
        var query = '';
        console.log("userid " + userId)
        if (userId == 'U7dea8fc4e85f49172f676a1ccda03d47' ||
                userId == 'U758b28fa3daca940be355d129991d571' ||
                userId == 'Udc4f4a48817d72704830430a7bd09e6a') {
            query = "select clientid,channelname,channelsecret, channeltoken from credentials";
        } else {
            //not super user
            query = "select clientid,channelname,channelsecret, channeltoken from credentials where channelname ='" + req.query.company_name + "'";
        }
        console.log("query " + query)
        conMysql.query(query, function (err, result, fields) {
            if (err)
                throw err;
            console.log(result);

            if (result.length > 0) {
                var obj = [];
                for (var i = 0; i < result.length; i++) {
                    obj.push({
                        no: i + 1,
                        clientid: result[i].clientid,
                        channelname: result[i].channelname,
                        channelsecret: result[i].channelsecret,
                        channeltoken: result[i].channeltoken
                    })
                }
            }
            console.log("obj " + obj);
            res.send(JSON.stringify(obj));
        });
    });
    // conMysql.end();
})

app.get('/credentials/getToken', function (req, res) {
    var date = new Date();
    console.log("get token " + req);
    var paramCode = req.query.code;
    var param = {
        grant_type: 'authorization_code',
        code: paramCode,
        redirect_uri: 'https://bangjoni.com/line/keyevent/list',
        client_id: '1559791567',
        client_secret: 'a9c9a3dcc5ab5638f2d89e4460d33b0b'
    };

    function updateStatus(nonce, userid, jsonData, res) {
        req.getConnection(function (error, conMysql) {
            sql = "select 1 from users where userid = '" + userid + "' AND is_active = 0;";
            console.log(sql);
            conMysql.query(sql, function (err, result, fields) {
                if (err)
                    throw err;
                console.log(err);
                if (result.length > 0) {
                    console.log('not active user');
                    sql = "update users SET userid = '" + userid + "' , is_active = 1 WHERE nonce ='" + nonce + "' AND is_active = 0;";
                    console.log(sql);
                    conMysql.query(sql, function (err, result, fields) {
                        if (err)
                            throw error;
                        console.log('affectedRows : ', result.affectedRows)
                        if (result.affectedRows == 0) {
                            console.log('401')
//                            res.sendFile(path.join(__dirname + '/views/401.html'));
                            res.send("401");
                        } else {
                            res.send(jsonData);
                        }
                    })
                } else {
                    res.send(jsonData);
                }
            })
        })
    }

    request.post({
        headers: {'content-type': 'application/x-www-form-urlencoded'},
        url: 'https://api.line.me/oauth2/v2.1/token',
        form: param
    }, function (error, response, body) {
        console.log(body);
        var payload = JSON.parse(body);
        if ("access_token" in payload) {
            var str = payload.id_token;
            var data = str.split(".");
            var header = data[0];
            var payload = data[1];
            var signature = data[2];

            var decode = new Buffer(payload, 'base64');

            // console.log(payload);
            // console.log(decode.toString());

            var parse = JSON.parse(decode.toString());
            console.log("respon login = ", parse);
//            var jsonData = {
//                name: parse.name,
//                photo: parse.picture,
//                // id_channel: parse.aud,
//                id_channel: channel_id,
//                code: paramCode,
//                userId: parse.sub,
//                exp: parse.exp,
//                nonce: parse.nonce
//            }

            console.log("channel id ori " + parse.aud);
            // channel_id = parse.aud;
            user_id = parse.sub;

//            client.set(key = 'keyeventbot/profile/' + paramCode + "/" + dateformat(date, "isoDate"), value = JSON.stringify(jsonData));
            // client.set(key='keyeventbot/profile/'+parse.aud+"/"+parse.sub ,value=JSON.stringify(jsonData));

//            res.send(jsonData);
//            updateStatus(parse.nonce, parse.sub, jsonData, res);


            req.getConnection(function (error, conMysql) {
                var sql = '';
                var sql2 = '';
                if (user_id == 'U7dea8fc4e85f49172f676a1ccda03d47' ||
                        user_id == 'U758b28fa3daca940be355d129991d571' ||
                        user_id == 'Udc4f4a48817d72704830430a7bd09e6a') {
                    sql = "select clientid,channelname from credentials";
                    sql2 = "select clientid,channelname from credentials";
                } else {
                    //not super user
                    sql = "update users SET userid = '" + parse.sub + "' WHERE nonce ='" + parse.nonce + "' AND is_active = 0;";
                    console.log(sql);
                    conMysql.query(sql, function (err, result, fields) {
                        if (err)
                            throw error;
                        console.log('affectedRows : ', result.affectedRows);
                    });
                    
                    sql2 = "select a.clientid,a.channelname from credentials a, users b where a.`channelname` = b.`company_name`" +
                            "and b.`company_name` = (select company_name from users where userid = '" + user_id + "') group by a.clientid";
                }
                console.log(new Date(), sql2);
                conMysql.query(sql2, function (err, result, fields) {
                    console.log("result = "+result);
                    console.log("fields = "+fields);
                    var channelid = [];
                    for (var i = 0; i < result.length; i++) {
                        channelid.push(result[i].clientid);
                    }

                    var jsonData = {
                        name: parse.name,
                        photo: parse.picture,
                        // id_channel: parse.aud,
                        id_channel: channelid,
                        company_name: result[0].channelname,
                        code: paramCode,
                        userId: parse.sub,
                        exp: parse.exp,
                        nonce: parse.nonce
                    }
                    console.log("jsonData", jsonData);
                    client.set(key = 'keyeventbot/profile/' + paramCode + "/" + dateformat(date, "isoDate"), value = JSON.stringify(jsonData));
                    updateStatus(parse.nonce, parse.sub, jsonData, res);
                })

            });
        } else {
            client.get('keyeventbot/profile/' + paramCode + "/" + dateformat(date, "isoDate"), function (err, reply) {
                if (reply == null) {
                    res.send("null");
                } else {
                    var now = Math.floor(Date.now() / 1000);
                    var datRepl = JSON.parse(reply);
                    if (now > datRepl.exp) {
                        res.send("null");
                    } else {
                        // console.log("reply")
                        // channel_id = datRepl.id_channel;
                        user_id = datRepl.userId;
                        res.send(reply);
                    }

                }
            })
        }
    });
})

app.get('/credentials/getRole', function (req, res) {
    var code = req.query.code;
    client.keys('*' + code + '*', function (err, reply) {
        if (err)
            throw err;
        key = reply[0]
        console.log(key);
        client.get(key, function (err, reply) {
            dataProfile = JSON.parse(reply);
            console.log(dataProfile);
            req.getConnection(function (error, conMysql) {
                sql = "select role from users where userid = '" + dataProfile.userId + "'";
                console.log(sql);
                conMysql.query(sql, function (err, result, fields) {
                    if (err)
                        throw err;
                    console.log(result);
                    console.log(result[0].role);
                    role = result[0].role;
                    res.send(role.toString());
                })
            })
        })
    })
});

app.get('/credentials/auth', function (req, res) {
    url = req.url;
    key = url.substr(url.indexOf('=') + 1, url.length);
    key = cryptoJs.AES.decrypt(key, passphrase);
    key = key.toString(cryptoJs.enc.Utf8);
    console.log(key);
    role = key.substr(0, 1);
    time = convert_time(key.substr(1, 14));
    nonce = key.substr(15, key.length);
    diff = new datediff(dateandtime.addHours(new Date, 7), time);
    console.log('debug mode', key, role, time, nonce, diff)
    url_redirect = 'https://access.line.me/oauth2/v2.1/authorize?scope=openid%20profile&response_type=code&state=12345abcde&redirect_uri=https://bangjoni.com/line/keyevent/list&nonce=' + nonce + '&client_id=1559791567'
    if (math.abs(diff.minutes()) <= 100) {
        res.writeHead(301, {Location: url_redirect})
        res.end();
    } else {
        res.send('Your link has been expired , please contact your administrator');
    }
});

app.get('/credentials/notAuth', function (req, res) {
    res.sendFile(path.join(__dirname + '/views/401.html'));
});

function convert_time(time) {
    // console.log(time)
    year = time.substring(0, 4)
    month = time.substring(4, 6)
    day = time.substring(6, 8)
    hour = time.substring(8, 10)
    minutes = time.substring(10, 12)
    second = time.substring(12, 14)
    time = year + '-' + month + '-' + day + 'T' + hour + ':' + minutes + ':' + second
    console.log("Jam Fbm : " + time.toString());
    return new Date(time)
}

app.get('/credentials/usermanage', function (req, res) {
    res.sendFile(path.join(__dirname + '/views/users.html'));
})

app.post('/credentials/insertUser', urlencodedParser, function (req, res) {
    console.log("req.body " + req.body);

    var reqBody = req.body;
    if ("data_users" in reqBody) {
        var reqBody = JSON.parse(reqBody.data_users);
        console.log(reqBody);
        var role = reqBody.cmbRole;
        var email = reqBody.inputEmail;
        var nonce = randomstring.generate(16);
        var company_name = reqBody.inputCompany;

        req.getConnection(function (error, conMysql) {
            if (error)
                throw error;
            var sql = "insert into users(email,role,is_active,nonce,company_name) values('" + email + "','" + role + "',0,'" + nonce + "','" + company_name + "')";
            conMysql.query(sql, function (err, result, fields) {
                if (err) {
                    throw err;
                } else {
                    console.log(result);

                    //send email
                    var to = [];
                    to.push(email);
                    var base_url = "https://bangjoni.com/line/keyevent/credentials/auth";
                    var time = dateformat(dateandtime.addHours(new Date(), 7), 'yyyymmddHHMMss');
//                    var key = crypter.encrypt(role + time + nonce);
                    var key = cryptoJs.AES.encrypt(role + time + nonce, passphrase);
                    var url_auth = base_url + '?key=' + key.toString();

                    sendmail.sendEmail(to, "Activation", url_auth);

                    var sql = "select email,role,is_active,company_name from users ";
                    conMysql.query(sql, function (err, result, fields) {
                        if (err)
                            throw err;
                        var obj = [];
                        for (var i = 0; i < result.length; i++) {
                            var stat = result[i].status;
                            if (stat == 0) {
                                stat = "Not Active";
                            } else {
                                stat = "Active";
                            }
                            obj.push({
                                no: i + 1,
                                email: result[i].email,
                                role: result[i].role,
                                company_name: result[i].company_name,
                                status: stat
                            });
                        }


                        res.send(JSON.stringify(obj));
                    })
                }
            })
        });
    }
})

app.get('/credentials/getUsers', function (req, res) {
    req.getConnection(function (error, conMysql) {
        if (error)
            throw error;
        var userid = req.query.userId;
        var sql = '';
        if (userid == 'U7dea8fc4e85f49172f676a1ccda03d47' ||
                userid == 'U758b28fa3daca940be355d129991d571' ||
                userid == 'Udc4f4a48817d72704830430a7bd09e6a') {
            sql = "select nonce,email,role,is_active,company_name from users";
        } else {
            //not super user
            sql = "select nonce,email,role,is_active,company_name from users where company_name = '" + req.query.company_name + "'";
        }
        conMysql.query(sql, function (err, result, fields) {
            if (err)
                throw err;
            var obj = [];
            for (var i = 0; i < result.length; i++) {
                var stat = result[i].is_active;
//                console.log("stat",stat);
                if (stat == 0) {
                    stat = "Not Active";
                } else {
                    stat = "Active";
                }
                obj.push({
                    no: i + 1,
                    email: result[i].email,
                    role: result[i].role,
                    company_name: result[i].company_name,
                    status: stat,
                    nonce: result[i].nonce
                });
            }
            res.send(JSON.stringify(obj));
        });
    })
})

app.get('/list', function (req, res) {
    // console.log("//list get code " + req.query.code);
    res.sendFile(path.join(__dirname + '/views/list.html'));
})

app.get('/list/getData', function (req, res) {
    var channelId = req.query.channelId;
    req.getConnection(function (error, conMysql) {
        if (error)
            throw error;
        var sql = "select a.botid,a.event_name,a.start_time,a.end_time,b.`right_key`,b.`wrong_key`,b.`right_key_not_coupon`,b.total_ticket_counter,b.win_ticket,b.user_participant,a.channelid,b.total_request from scheduleevent a, `counterstatistic` b where b.`botid` = a.`botid` and a.channelid = '" + channelId + "'";
        conMysql.query(sql, function (err, result, fields) {
            if (err)
                throw err;
            console.log(result);
            var obj = [];
            for (var i = 0; i < result.length; i++) {
                obj.push({
                    botid: result[i].botid,
                    event_name: result[i].event_name,
                    start_time: result[i].start_time,
                    end_time: result[i].end_time,
                    right_key: result[i].right_key,
                    wrong_key: result[i].wrong_key,
                    right_key_not_coupon: result[i].right_key_not_coupon,
                    total_ticket_counter: result[i].total_ticket_counter,
                    win_ticket: result[i].win_ticket,
                    user_participant: result[i].user_participant,
                    channelid: result[i].channelid,
                    total_request: result[i].total_request
                });
            }
            // console.log(obj);
            res.send(JSON.stringify(obj));
        });
    })

})

app.get('/list/delete', function (req, res) {
    // try {
    req.getConnection(function (error, conMysql) {
        data = req.query;
        channelid = data.channelid;
        botid = data.botid;
        console.log(channelid, botid)
        sql = "DELETE FROM scheduleevent where botid = '" + botid + "';DELETE FROM counterstatistic where botid = '" + botid + "';COMMIT;"
        console.log(sql);
        conMysql.query(sql, function (err, result, fields) {
            console.log(err);
            console.log(result);
            if (err)
                throw err;
            key = [
                'keyeventbot/schedule/' + channelid,
                'keyeventbot/coupon/' + botid,
                'keyeventbot/counter/' + botid + '/right_key',
                'keyeventbot/counter/' + botid + '/wrong_key',
                'keyeventbot/counter/' + botid + '/right_key_not_coupon',
                'keyeventbot/counter/' + botid + '/win_ticket',
                'keyeventbot/counter/' + botid + '/total_ticket_counter',
                'keyeventbot/counter/' + botid + '/total_request',
                "keyeventbot/userwinlose/" + channelid
            ]

            for (i = 0; i < key.length; i++) {
                client.del(key[i])
            }
            res.sendStatus(200);
        })
    })
    // } catch (error) {
    // 	res.sendStatus(404);
    // }
})

app.get('/credentials/deleteUser', function (req, res) {
    req.getConnection(function (err, conMysql) {
        if (err)
            throw err;
        nonce = req.query.nonce;
        sql = "delete from users where nonce = '" + nonce + "'";
        console.log("query del user", sql);
        conMysql.query(sql, function (err, result, fields) {
            if (err)
                throw err;
            console.log("result delete user", result);

            res.sendStatus(200);
        })
    })
})

app.get('/list/getEventExisting', function (req, res) {
    var channelId = req.query.channelId;
    console.log("evtEx " + channelId);
    client.get('keyeventbot/schedule/' + channelId, function (err, reply) {
        // console.log(reply);
        var rest = JSON.parse(reply);
        if (rest) {

            if (rest.limit_sum == "2") {
                var end_time_event = rest.end_time;
                console.log(end_time_event);
                var now = dateformat(dateandtime.addHours(new Date(), 7), 'dd-mm-yyyy HH:MM:ss');
                console.log(now)
                if (end_time_event >= now) {
                    res.send('exist');
                } else {
                    res.send('empty');
                }
            } else {
                client.get('keyeventbot/counter/' + rest.botid + '/total_ticket_counter', function (err, reply) {
                    if (reply > 0) {
                        res.send('exist');
                    } else {
                        res.send('empty');
                    }
                })
            }

        } else {
            res.send('empty');
        }
    });
});

app.get('/', function (req, res) {
    res.send('Hello World');
})

app.get('/test', function (req, res) {
    res.send('ntaab tenan');
})



app.post('/fileupload', function (req, res) {
    console.log(req);
    console.log(req.body);
    console.log(req.files.path);
    res.status(200);
})

app.post('/index/submit', urlencodedParser, function (req, res) {
    console.log("submit " + channel_id);
    console.log("get " + id);
    console.log()
    // if (!req.files.file.name.toLowerCase().endsWith(".csv")) {
    // 	res.send('Wrong file format');
    // 	return;
    // }
    var reqBody = req.body;
    console.log(reqBody);
    if ("stat_data" in reqBody) {
        var reqBody = JSON.parse(reqBody.stat_data);
        console.log(reqBody.inputBotId);
        console.log(req.body);

        //=============start=============
        var botId = reqBody.inputBotId;
        var type = reqBody.inputType;
        var eventName = reqBody.inputEventName;
        var periodEvent = reqBody.eventtime;
        var splitPeriod = periodEvent.split(' - ');
        var startDate = splitPeriod[0];
        var endDate = splitPeriod[1];
        var abuseCheck = reqBody.r1;
        var limitSum = reqBody.r2;
        var caseSensitive = reqBody.r3;
        var msgForPhone = reqBody.editPhone;
        var msgNonWinner = reqBody.editNonWinner;
        var msgDuplicate = reqBody.editDuplicate;
        var msgKeyword = reqBody.editKeyword;
        var msgKeywordMiss = reqBody.editKeywordMiss;
        var msgExCupon = reqBody.editExCupon;
        var msgForWinner = reqBody.editForWinner;
        var msgForNoEvent = reqBody.editForNoEvent;
        var uploadCSV = reqBody.dataUpload;
        var winProb = reqBody.inputWinProb;
        var channelId = reqBody.cmbChannel;
        if (winProb == '') {
            winProb = uploadCSV;
        }

        percentageWinProb = winProb / uploadCSV;


        var jsonValSchedule = {
            "botid": botId,
            "type": "ADVANCE KEYWORD INPUT",
            "event_name": eventName,
            "start_time": startDate,
            "end_time": endDate,
            "abuser_check": abuseCheck,
            "limit_sum": limitSum,
            "is_key_sensitive": caseSensitive,
            "mf_phone": msgForPhone,
            "mf_nonwinner": msgNonWinner,
            "mf_duplicate_entry": msgDuplicate,
            "keyword": msgKeyword,
            "mf_keyword_mistake": msgKeywordMiss,
            "mf_exhausted_coupon": msgExCupon,
            "mf_winner": msgForWinner,
            "mf_no_event": msgForNoEvent,
            "win_probability": parseFloat(percentageWinProb).toFixed(2),
            "limit_amount": 100,
            "l_start_time": startDate.substr(11, 9),
            "l_end_time": endDate.substr(11, 9),
            "total_coupon": uploadCSV,
            "channel_id": channelId
        }

        var jsonValCounter = {
            "botid": botId,
            "right_key": 0,
            "wrong_key": 0,
            "right_key_not_coupon": 0,
            "win_ticket": 0,
            "total_ticket_counter": uploadCSV
        }

        // stringCSVParser(uploadCSV,botId);
        client.set(key = 'keyeventbot/schedule/' + channelId, value = JSON.stringify(jsonValSchedule));
        // client.set(key='keyeventbot/counter/'+channel_id,value=JSON.stringify(jsonValCounter));
        
        console.log("===========================================================> SUBMIT_START:" + id)
        if (id == null) {
            console.log("===========================================================> SUBMIT_INSERT_EVENT id:")
            console.log(req.files.file);

            req.getConnection(function (error, conMysql) {
                var sql = "insert into scheduleevent(botid,type,event_name,abuser_check,limit_sum,is_key_sensitive,mf_phone,mf_nonwinner,mf_duplicate_entry,keyword,mf_keyword_mistake,mf_exhausted_coupon,mf_winner,win_probability,mf_no_event,start_time,end_time,l_start_time,l_end_time,jml_coupon,channelid) " +
                        "values('" + botId + "','" + type + "','" + eventName + "'," + abuseCheck + "," + limitSum + "," + caseSensitive + ",'" + msgForPhone + "','" + msgNonWinner + "','" + msgDuplicate + "','" + msgKeyword + "','" + msgKeywordMiss + "','" + msgExCupon + "','" + msgForWinner + "'," + winProb + ",'" + msgForNoEvent + "'," +
                        "DATE_FORMAT(STR_TO_DATE('" + startDate + "','%d-%m-%Y %H:%i:%s'),'%Y-%m-%d %H:%i:%s'),DATE_FORMAT(STR_TO_DATE('" + endDate + "','%d-%m-%Y %H:%i:%s'),'%Y-%m-%d %H:%i:%s')," +
                        "DATE_FORMAT(STR_TO_DATE('" + startDate + "','%d-%m-%Y %H:%i:%s'),'%Y-%m-%d %H:%i:%s'),DATE_FORMAT(STR_TO_DATE('" + endDate + "','%d-%m-%Y %H:%i:%s'),'%Y-%m-%d %H:%i:%s')," + uploadCSV + ",'" + channelId + "');insert into counterstatistic(botid,right_key,wrong_key,right_key_not_coupon,last_update_date,win_ticket,total_ticket_counter,user_participant) values('" + botId + "',0,0,0,now(),0," + uploadCSV + ",0);";
                console.log("=========================================================>sql = " + sql);
                // Mysql(sql);
                conMysql.query(sql, function (err, result, fields) {
                    if (err) {
                        console.log("===========================================================> SUBMIT_INSERT_EVENT_MYSQL_ERR id:" + botId)
                        throw err
                    } else {
                        console.log("===========================================================> SUBMIT_INSERT_EVENT_MYSQL_SUCCESS id:" + botId)
                        console.log(result)
                    }

                    csvdata = req.files.file.data;
                    csvdata = csvdata.toString('utf-8');
                    if (csvdata.indexOf('\r\n') >= 0) {
                        csvdata = csvdata.split('\r\n');
                    } else if (csvdata.indexOf('\r') >= 0) {
                        csvdata = csvdata.split('\r');
                    } else if (csvdata.indexOf('\n') >= 0) {
                        csvdata = csvdata.split('\n');
                    }
                    date_start = new Date
                    console.log(date_start.toString() + ' build array mongodb');
                    console.log("csvdata", csvdata);
                    for (var i = 0; i < csvdata.length; i++) {
                        if (csvdata[i] != null) {
                            console.log("content", csvdata[i]);
                            client.rpush('keyeventbot/coupon/' + botId, csvdata[i]);
                        }
                    }

                });
                client.set(key = 'keyeventbot/counter/' + botId + "/right_key", value = "0");
                client.set(key = 'keyeventbot/counter/' + botId + "/wrong_key", value = "0");
                client.set(key = 'keyeventbot/counter/' + botId + "/right_key_not_coupon", value = "0");
                client.set(key = 'keyeventbot/counter/' + botId + "/win_ticket", value = "0");
                client.set(key = 'keyeventbot/counter/' + botId + "/total_ticket_counter", value = uploadCSV);
                console.log("===========================================================> SUBMIT_INSERT_EVENT_DATA_SAVED id:" + botId)
                res.send('Data Saved!!');
            })

        } else {
            //edit data exiting
            // conMysql.connect();
            console.log("===========================================================> SUBMIT_EDIT_EVENT id:" + id)
            var sql = "update scheduleevent set start_time = DATE_FORMAT(STR_TO_DATE('" + startDate + "','%d-%m-%Y %H:%i:%s'),'%Y-%m-%d %H:%i:%s')," +
                    "end_time = DATE_FORMAT(STR_TO_DATE('" + endDate + "','%d-%m-%Y %H:%i:%s'),'%Y-%m-%d %H:%i:%s'),l_start_time = DATE_FORMAT(STR_TO_DATE('" + startDate + "','%d-%m-%Y %H:%i:%s'),'%Y-%m-%d %H:%i:%s')," +
                    "l_end_time = DATE_FORMAT(STR_TO_DATE('" + endDate + "','%d-%m-%Y %H:%i:%s'),'%Y-%m-%d %H:%i:%s'),mf_phone = '" + msgForPhone + "'," +
                    "mf_nonwinner = '" + msgNonWinner + "',mf_duplicate_entry = '" + msgDuplicate + "',keyword = '" + msgKeyword + "',mf_keyword_mistake = '" + msgKeywordMiss + "'," +
                    "mf_exhausted_coupon = '" + msgExCupon + "',mf_winner = '" + msgForWinner + "', mf_no_event = '" + msgForNoEvent + "' " +
                    "where botid = '" + id + "'";
            console.log("==========================================================> sql = " + sql);
            req.getConnection(function (error, conMysql) {
                conMysql.query(sql, function (err, result, fields) {
                    if (err)
                        throw err;
                    console.log("===========================================================> SUBMIT_EDIT_EVENT_MYSQL_SUCCESS id:" + id)
                    console.log(result);
                    // callback(null,fields);
                });
            });
            console.log("===========================================================> SUBMIT_EDIT_EVENT_DATA_SUCCESS id:" + id)
            res.send('Edit Data Success!!');
        }
    } else {
        var reqBody = JSON.parse(reqBody.cred_data);
        console.log(reqBody);

        var clientid = reqBody.channelid
        var channelName = reqBody.channelName
        var channelToken = reqBody.channelToken
        var channelSecret = reqBody.channelSecret
        dataChannel = {
            'channelName': channelName,
            'channelToken': channelToken,
            'channelSecret': channelSecret
        }
        client.set(key = 'keyeventbot/credentials/' + clientid, value = JSON.stringify(dataChannel));
        sql = "INSERT INTO credentials \
            (clientid, channeltoken, channelsecret,channelname) \
            VALUES('" + clientid + "','" + channelToken + "','" + channelSecret + "','" + channelName + "') \
            ON DUPLICATE KEY UPDATE \
            clientid = '" + clientid + "', channeltoken = '" + channelToken + "', channelsecret ='" + channelSecret + "', channelname ='" + channelName + "'"
        req.getConnection(function (error, conMysql) {
            conMysql.query(sql, function (err, result) {
                if (err)
                    throw err;
                console.log("Result: " + JSON.stringify(result));
            });
        });
        res.send('Data Saved!!');
    }

})

var server = app.listen(8011, function () {
    var host = server.address().address
    var port = server.address().port

    console.log("Example app listening at http://%s:%s", host, port)
})
