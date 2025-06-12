from datetime import timedelta
from typing import Literal

EncodingErrorHandler = Literal["strict", "ignore", "replace"]

DEFAULT_ENCODING = "utf-8"
DEFAULT_ENCODING_ERROR_HANDLER: EncodingErrorHandler = "strict"

DEFAULT_HTTP_TIMEOUT = 30.0
DEFAULT_SSE_READ_TIMEOUT = 60.0

DEFAULT_STREAMABLE_HTTP_TIMEOUT = 30.0
DEFAULT_STREAMABLE_HTTP_SSE_READ_TIMEOUT = 60.0 