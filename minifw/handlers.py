import re
import time
import json
import logging
import hashlib
import base64
import asyncio
from minifw.core import framewk
from minifw.models import User


@framewk.get('/')
async def index(request):
    #users = await User.find_all()
    return {
        '__template__': 'test.html',
        'users': None
    }