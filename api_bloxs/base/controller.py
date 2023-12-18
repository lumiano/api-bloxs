from api_bloxs.infra.trace import Trace, trace


class Controller:
    log = Trace(__name__)

    @classmethod
    def loguru(cls, func):
        return trace(cls.log)(func)
