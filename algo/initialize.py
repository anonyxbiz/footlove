# /algo/initialize.py
import os, asyncio as a, base64, json as j, json_stream as j_s, time
from bottle import Bottle, route, run, request, static_file, response as r, post, get, put, delete, template, redirect, HTTPResponse, abort, hook
from threading import Thread
import requests as rqs
from datetime import datetime as dt
from sys import exit
from difflib import get_close_matches

p = print

with open('env.json', 'r') as f:
    env = j.load(f)
    
csrf_key = env[0]["key"]

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
        p(self.errors)
        abort(403, self.errors)