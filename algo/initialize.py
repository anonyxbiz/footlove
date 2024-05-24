# /algo/initialize.py
import os, asyncio as a, base64, json as j, json_stream as j_s
from bottle import Bottle, route, run, request, static_file, response as r, post, get, put, delete, template, redirect, HTTPResponse, abort, hook
import argparse
from threading import Thread
import requests as rqs
from datetime import datetime as dt
from cryptography.fernet import Fernet
from sys import exit

p = print

parser = argparse.ArgumentParser()
parser.add_argument('-arg', "--arg",)    
args = parser.parse_args()

app_info = {'title': 'Wazingapi', 'web_app_url': 'https://example.com'}

csrf_key = 'UKP89oA1T_01-jcheufpv9Y3JaeX1Se03n1u7Qq9gjY'

class Error(Exception):
    def __init__(self, e=None, location=None, status=403):
        self.errors = {
            'status': status,
            'error': str(e),
            'location': location
        }
        p(self.errors)
        abort(403, self.errors)
    
    def __str__(self):
        abort(403, self.errors)