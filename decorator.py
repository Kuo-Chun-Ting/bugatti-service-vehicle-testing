from functools import wraps
import asyncio

def clear(func):
    @wraps(func)
    async def wrapped(*args):
        try:
            print('Removing test data...')
            result = await func(*args)
            print('Finished')
            return result
        except Exception as e:
            print(f'An error occurred while removing test data. {e}')
    return wrapped

def exception_handler(func):
    @wraps(func)
    async def wrapped(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            print(f'An error occurred in VehicleClient.{func.__name__}().', e)
    return wrapped

