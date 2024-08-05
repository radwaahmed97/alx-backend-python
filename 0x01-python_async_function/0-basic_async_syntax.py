#!/usr/bin/env python3
"""
returns random wait from 0 to max_delay default number
"""

import time
import asyncio
import random


async def wait_random(max_delay: int = 10) -> float:
    """ returns random_wait """
    random_wait = random.random() * max_delay
    await asyncio.sleep(random_wait)
    return random_wait
