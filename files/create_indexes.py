#!/usr/bin/env python
import datetime
import uuid
import hashlib
import sys

INDEX_VER = 101
import pymongo

client = pymongo.MongoClient(host='mongo')
#client = pymongo.MongoClient(host='172.18.0.2')
indexes = [
  "alerts",
  "filters",
  "flow",
  "dns",
  "certs",
  "watchlist",
  "signatures",
  "sessions",
  "keys",
  "users"
]

db = client.minerva
for i in indexes:
    try:
        db.create_collection(i)
    except Exception as e:
        continue
try:
    db.alerts.create_index([("MINERVA_STATUS", pymongo.ASCENDING),("timestamp", pymongo.ASCENDING),("alert.severity", pymongo.DESCENDING),("src_ip", pymongo.ASCENDING),("src_port", pymongo.ASCENDING),("dest_ip", pymongo.ASCENDING),("dest_port", pymongo.ASCENDING),("proto", pymongo.ASCENDING),("alert.signature", pymongo.ASCENDING),("alert.category", pymongo.ASCENDING),("alert.signature_id", pymongo.ASCENDING),("alert.rev", pymongo.ASCENDING),("alert.gid", pymongo.ASCENDING),("sensor", pymongo.ASCENDING)],name="alert-search-%i" % INDEX_VER)
    expiredDays = 10
    expiredSeconds = int(expiredDays) * 86400
    db.alerts.ensure_index("timestamp",name="alert-expired-%i" % INDEX_VER, expireAfterSeconds=expiredSeconds)

except:
    pass

try:
    db.flow.create_index([("src_ip", pymongo.ASCENDING),("src_port", pymongo.ASCENDING),("dest_ip", pymongo.ASCENDING),("dest_port", pymongo.ASCENDING),("proto", pymongo.ASCENDING),("netflow.start", pymongo.ASCENDING),("netflow.end", pymongo.ASCENDING),("sensor", pymongo.ASCENDING)],name="flow-search-%i" % INDEX_VER)
    
    expiredflowDays = 10
    flowexpiredSeconds = int(expiredflowDays) * 86400
    
    db.flow.ensure_index("timestamp",name="flow-expired-%i" % INDEX_VER,expireAfterSeconds=flowexpiredSeconds)
    
except:
    pass

try:
    db.dns.create_index([("src_ip", pymongo.ASCENDING),("src_port", pymongo.ASCENDING),("dest_ip", pymongo.ASCENDING),("dest_port", pymongo.ASCENDING),("proto", pymongo.ASCENDING),("timestamp", pymongo.ASCENDING),("sensor", pymongo.ASCENDING),("dns.type", pymongo.ASCENDING),("dns.rrtype", pymongo.ASCENDING),("dns.rcode", pymongo.ASCENDING),("dns.rrname", pymongo.ASCENDING),("dns.rdata", pymongo.ASCENDING)],name="dns-search-%i" % INDEX_VER)
    
    expireddnsDays = 10
    dnsexpiredSeconds = int(expireddnsDays) * 86400
    
    db.dns.ensure_index("timestamp",name="dns-expired-%i" % INDEX_VER, expireAfterSeconds=dnsexpiredSeconds)

except:
    pass
    
try:
    expiredTempHours = 24
    expiredTempSeconds = expiredTempHours * 3600
    
    db.filters.ensure_index("temp_timestamp", name="temp-expired-%i" % INDEX_VER, expireAfterSeconds=expiredTempSeconds)
    
    sessionMinutes = 30
    sessionTimeout = int(sessionMinutes) * 60
    
    db.sessions.ensure_index("last_accessed",name="session-expired-%i" % INDEX_VER, expireAfterSeconds=sessionTimeout)
    
    db.keys.ensure_index("timestamp",name="key-expired-%i" % INDEX_VER,expireAfterSeconds=3600)
except:
    pass

try:
    session_salt = uuid.uuid4().hex
    user_name = 'admin'
    admin_pw = 'changeme'
    password_salt = uuid.uuid4().hex
    admin_hashedPW = hashlib.sha512(str(admin_pw) + str(password_salt)).hexdigest()
    admin_user = db.users.find_one({"USERNAME": user_name})
    
    if not admin_user or admin_user is None:
        db.users.insert(
            {
                "USERNAME" : user_name,
                "user_admin" : "true",
                "ENABLED" : "true",
                "SALT": password_salt,
                "PASSWORD" : admin_hashedPW,
                "console" : "true",
                "date_modified" : datetime.datetime.utcnow(),
                "sensor_admin" : "true",
                "responder" : "true",
                "event_filters": "true",
                "server_admin" : "true",
                "date_created" : datetime.datetime.utcnow(),
                "PASSWORD_CHANGED": datetime.datetime.utcnow(),
            })
except:
    pass

sys.exit(0)
