import logging


async def get_dict(keys=None, **kwargs) -> dict:
    """
    :param keys: default: None - columns names
    :param kwargs: info about user
    :return: dict with necessary info about user
    """
    if keys is None:
        keys = ['chat_id', 'language_code', 'computers', 'server']
    return {key: kwargs.get(key) if key != 'chat_id' else kwargs.get('id') for key in keys}
