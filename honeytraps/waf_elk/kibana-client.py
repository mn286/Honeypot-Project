#!.venv/bin/python3
# -*- coding: utf-8 -*-
from datetime import datetime
from elasticsearch import Elasticsearch
import json
import time
import os
import logging
from pymisp import PyMISP, PyMISPError

# Setting up logging
logging.basicConfig(level=logging.INFO, format='[%(asctime)s][%(levelname)s][%(name)s] %(message)s')
log = logging.getLogger("MispConnector")
handler = logging.FileHandler('/var/log/kibana-client.log')
handler.setLevel(logging.INFO)
# create a logging format
formatter = logging.Formatter('[%(asctime)s][%(levelname)s][%(name)s] %(message)s')
handler.setFormatter(formatter)
log.addHandler(handler)

misp_url = os.getenv("URL_MISP", None)
misp_key = os.getenv("MISP_KEY", None)
misp_verifycert = True if (os.getenv("MISP_VERIFYCERT", None) == "true") else False

if (misp_url is None):
    log.critical("MISP_URL was not set in env file, stopping Misp Push")
    exit

class MispEvent(object):
    #### Create an event on MISP

    ##Event consists of distribution, information, analysis and threat

    # The distribution setting used for the attributes and for the newly created event, if relevant. [0-3].

    distrib = 0

    # Used to populate the event info field if no event ID supplied.

    info = 'This is event generated from PyMISP'

    # The analysis level of the newly created event, if applicable. [0-2]

    analysis = 0

    # The threat level ID of the newly created event, if applicable. [1-4]

    threat = 1

    """docstring for MispEvent"""
    def __init__(self, distribution,info,analysis,threat):
        super(MispEvent, self).__init__()
        self.distrib = distribution
        self.info = info
        self.analysis = analysis
        self.threat = threat
        
# TODO: Switch to ExpandedPyMISP
def init(url, key):
    return PyMISP(url, key, misp_verifycert, 'json', debug=False)


def generate_event_info(json_log):
    attacker_ip_address = json.dumps(json_log['_source']['transaction']['remote_address'])
    transaction_time = json.dumps(json_log['_source']['transaction']['time'])
    audit_data = json.dumps(json_log['_source']['audit_data']['messages'])
    audit_data_producer = json.dumps(json_log['_source']['audit_data']['producer'])

    event_info = "Attack identified from the "+attacker_ip_address+" at timestamp "+transaction_time+"  "+audit_data+" This information is generated from "+audit_data_producer
    return event_info


def generate_misp_event(misp_event):
    misp = init(misp_url, misp_key)
    event = misp.new_event(misp_event.distrib, misp_event.threat, misp_event.analysis, misp_event.info)
    misp.add_tag(event, 'AutoGenerated', attribute=False)
    misp.add_tag(event, 'HoneytrapEvent', attribute=False)
    misp.add_tag(event, 'ModSecurity', attribute=False)
    log.debug(event)


def generate_misp_tags():
    misp = init(misp_url, misp_key)
    misp.new_tag(name='AutoGenerated', colour='#00ace6', exportable=True)
    misp.new_tag(name='HoneytrapEvent', colour='#581845', exportable=True)
    misp.new_tag(name='ModSecurity', colour='#a04000', exportable=True)



es = Elasticsearch()
logging.getLogger("elasticsearch").setLevel(logging.CRITICAL)

index_name = ""

watch_interval = 10  # seconds

for index in es.indices.get('*'):
    log.debug(index)
    index_str = str(index) 
    if index_str.find("filebeat-") != -1:
        log.debug("found it!")
        log.debug(index_str)
        index_name = index_str
        break

tagsGenerated = False
retry_interval = 1
while tagsGenerated == False:
    try:
        generate_misp_tags()
        tagsGenerated = True
    except PyMISPError as e:
        log.error(e)
        tagsGenerated = False
        if (retry_interval > 300):
            retry_interval = 256
        log.info("Retrying in " + str(retry_interval) + " seconds...")
        time.sleep(retry_interval)
        retry_interval = retry_interval*2

while True:
    #TODO: Fix Elasticsearch log pollution
    res = es.search(index=index_name,
                    body={'query':{'range':{
                           '@timestamp':{
                                    'gte':'now-'+str(watch_interval)+'s',
                                    'lt':'now'
                            }
                    }}
                    })

    log.debug('Got %d Hits:' % res['hits']['total']['value'])

    for hit in res['hits']['hits']:
        # print(hit)
        json_log = hit
        log.debug('Index is ' + json_log['_index'])
        misp_event_info = generate_event_info(json_log)
        misp_event_obj = MispEvent(0,misp_event_info,0,1)
        log.debug('=====================================================')
        try:
            generate_misp_event(misp_event_obj)
            log.info("New Events sent to MISP")
        except PyMISPError as e:
            log.error(e)
    time.sleep(watch_interval)