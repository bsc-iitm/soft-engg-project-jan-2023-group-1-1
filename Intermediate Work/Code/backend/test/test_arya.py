## TicketAll, GetResolutionTimes, ResolutionTimes, FlaggPostAPI
# GET: Check Status Code and Key-Value Pairs
# POST/PATCH: Check Status Code, GET Request and Check Key-Value Pairs
# DELETE: Delete Request, Get Status Code, GET Request and raise Error/not 200 status code

import requests
from flask import json
#import db models here
import sys
import os

SCRIPT_DIRP = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIRP))

