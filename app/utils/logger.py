import json
import logging
from datetime import datetime
from time import time

from fastapi.logger import logger
from fastapi.requests import Request
# from pytz import timezone

logger.setLevel(logging.INFO)


async def api_logger(request: Request, response=None, error=None):
    time_format = "%Y/%m/%d %H:%M:%S"
    t = time() - request.state.start
    status_code = error.status_code if error else response.status_code
    error_log = None
    user = request.state.user
    # body = await request.body()

    if error:
        error_func = error_file = error_line = "UNKNOWN"
        if request.state.inspect:
            pass

        error_log = dict(
            errorFunc=error_func,
            location=f"{str(error_line)} in {error_file}",
            raised=str(error.__class__.__name__),
            msg=str(error),
        )

    user_log = dict(
        client=request.state.ip,
        user_email=user.email if user and user.email else None,
    )

    log_dict = dict(
        url=request.url.hostname + request.url.path,
        method=str(request.method),
        statusCode=status_code,
        errorDetail=error_log,
        client=user_log,
        processedTime=str(round(t * 1000, 5)) + "ms",
        datetimeUTC=datetime.utcnow().strftime(time_format),
        # datetimeKST=datetime.now(timezone("Asia/Seoul")).strftime(time_format),
        datetimeKST=datetime.now().strftime(time_format),
    )

    if error and error.status_code >= 500:
        logger.error(json.dumps(log_dict))
    else:
        logger.info(json.dumps(log_dict))
