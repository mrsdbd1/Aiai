import random
import logging
import subprocess
import sys
import os
import re
import time
import concurrent.futures
import discord
from discord.ext import commands, tasks
import docker
import asyncio
from discord import app_commands
from discord.ui import Button, View, Select
import string
from datetime import datetime, timedelta
from typing import Optional, Literal

TOKEN = ''
RAM_LIMIT = '6g'
SERVER_LIMIT = 10
database_file = 'database.txt'
PUBLIC_IP = '0.0.0.0'

# Admin user IDs - add your admin user IDs here
ADMIN_IDS = [1368602087520473140]  # Replace with actual admin IDs
