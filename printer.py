import time

async def printer(text, delay=0.05):
    for ch in text:
        print(ch, end='', flush=True)
        time.sleep(delay)