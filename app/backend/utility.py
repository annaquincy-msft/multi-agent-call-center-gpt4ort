import yaml  
from typing import Any  
import os  
from sqlalchemy.ext.declarative import declarative_base  
from sqlalchemy.orm import sessionmaker, relationship  
from datetime import datetime  
import random  
from dotenv import load_dotenv  
from openai import AsyncAzureOpenAI  
from pathlib import Path  
import json  
from scipy import spatial  # for calculating vector similarities for search  
# Load YAML file  
import yaml
# Load YAML file  
import asyncio
import time
import aiohttp
import urllib.request  
import json  
import os  
import ssl  
import os
import redis
import pickle
import base64
from typing import Dict
import logging
# Configure logging  
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")  
logger = logging.getLogger(__name__)  

def load_entity(file_path, entity_name):  
    with open(file_path, 'r') as file:  
        data = yaml.safe_load(file)  
    for entity in data['agents']:  
        if entity.get('name') == entity_name:  
            return entity  
    return None  
  
# Load environment variables  
load_dotenv(override=True)  
async_client = AsyncAzureOpenAI(  
    api_key=os.environ.get("AZURE_OPENAI_API_KEY"),  
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),  
    azure_endpoint=os.environ.get("AZURE_OPENAI_ENDPOINT"),  
) 
INTENT_SHIFT_API_KEY = os.environ.get("INTENT_SHIFT_API_KEY")
INTENT_SHIFT_API_URL = os.environ.get("INTENT_SHIFT_API_URL") 
INTENT_SHIFT_API_DEPLOYMENT=os.environ.get("INTENT_SHIFT_API_DEPLOYMENT")
AZURE_OPENAI_4O_MINI_DEPLOYMENT=os.environ.get("AZURE_OPENAI_4O_MINI_DEPLOYMENT")
  
def allowSelfSignedHttps(allowed):  
    if allowed and not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None):  
        ssl._create_default_https_context = ssl._create_unverified_context  
  
allowSelfSignedHttps(True)  
  
async def detect_intent(conversation): 
    # detect inteent with gpt40
    messages = [
        {"role": "system", "content": "You are an intent classification assistant for a voice AI system that handles patient support related to Cologuard, a colorectal cancer screening test.\n\nYour task is to classify the user's input into one of the following four intents. Only choose one.\n\nINTENT OPTIONS:\n\n1. kit_shipping_agent\n→ The user is asking about when their Cologuard kit will arrive, if it's been shipped, or if they haven't received it yet.\n\n2. kit_return_agent\n The user wants to return a Cologuard kit, schedule a UPS pickup, check status of a scheduled pickup, or find a nearby UPS drop-off location.\n\n3. results_agent\n The user is asking for their Cologuard test results, wants to understand their result, or is authorizing you to share it with them.\n\n4. general_questions_agent\n The user is asking general questions about Cologuard that are not specific to their personal order, return, or result.\nExamples: 'How does Cologuard work?' 'Is it covered by insurance?'\nYou should only return information that comes from the official Cologuard website.\n\nRESPONSE FORMAT:\n\nReturn only the matching intent name (no explanation). One of:\n\n- kit_shipping_agent\n- kit_return_agent\n- results_agent\n- general_questions_agent"},
        {"role": "user", "content": conversation}
    ]
    response = await async_client.chat.completions.create(
        model=AZURE_OPENAI_4O_MINI_DEPLOYMENT,
        messages=messages,
        max_tokens=20
    )
    intent = response.choices[0].message.content.strip()
    return intent

class SessionState:  
    def __init__(self): 
        # Redis configuration 
        self.redis_client = None 
        AZURE_REDIS_ENDPOINT = os.getenv("AZURE_REDIS_ENDPOINT")  
        AZURE_REDIS_KEY = os.getenv("AZURE_REDIS_KEY")  
        if AZURE_REDIS_KEY: #use redis
            self.redis_client = redis.StrictRedis(host=AZURE_REDIS_ENDPOINT, port=6380, password=AZURE_REDIS_KEY, ssl=True)  
            logger.info("Using Redis for session storage")
        else: #use in-memory
            self.session_store: Dict[str, Dict] = {}  

                
    def get(self, key):  
        if self.redis_client:
            self.data = self.redis_client.get(key)  
            return pickle.loads(base64.b64decode(self.data)) if self.data else None  
        else:
            return self.session_store.get(key)

          
    def set(self, key, value):  
        if self.redis_client:
            self.redis_client.set(key, base64.b64encode(pickle.dumps(value)))  
        else:
            self.session_store[key]=value
          
