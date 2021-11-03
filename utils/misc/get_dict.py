import logging


async def get_dict(keys=None, **kwargs) -> dict:
    if keys is None:
        keys = ['chat_id', 'language_code', 'computers', 'server']
    return {key: kwargs.get(key) if key != 'chat_id' else kwargs.get('id') for key in keys}
