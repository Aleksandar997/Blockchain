from .logger import LoggerService

def exec(func):
    res = None
    try:
        res = func()
    except AttributeError as ve:
        res = ve.args
    except Exception as e:
        LoggerService.logger.log_exception(e)
        res = e.args
    finally:
        return res