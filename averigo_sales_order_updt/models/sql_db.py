import threading
import time

import psycopg2

from odoo import tools
from odoo.sql_db import Cursor
import re
re_from = re.compile('.* from "?([a-zA-Z_0-9]+)"? .*$')
re_into = re.compile('.* into "?([a-zA-Z_0-9]+)"? .*$')

import logging

_logger = logging.getLogger(__name__)

@Cursor.check
def execute(self, query, params=None, log_exceptions=None):
    if params and not isinstance(params, (tuple, list, dict)):
        # psycopg2's TypeError is not clear if you mess up the params
        raise ValueError("SQL query parameters should be a tuple, list or dict; got %r" % (params,))

    if self.sql_log:
        encoding = psycopg2.extensions.encodings[self.connection.encoding]
        _logger.debug("query: %s", self._obj.mogrify(query, params).decode(encoding, 'replace'))
    now = time.time()
    try:
        params = params or None
        aggs = (
        'sum', 'avg', 'min', 'max', 'string_agg', 'array_agg', 'group by', 'insert', 'update')
        conditions = [query.lower().find(x) != -1 for x in aggs]
        res = self._obj.execute(query if (any(conditions) or (
                    query.split('FROM')[-1].find('stock_move') == -1)) else (
                    query + ' FOR UPDATE NOWAIT'), params)
    except Exception as e:
        if self._default_log_exceptions if log_exceptions is None else log_exceptions:
            _logger.error("bad query: %s\nERROR: %s", tools.ustr(self._obj.query or query), e)
        raise

    # simple query count is always computed
    self.sql_log_count += 1
    delay = (time.time() - now)
    if hasattr(threading.current_thread(), 'query_count'):
        threading.current_thread().query_count += 1
        threading.current_thread().query_time += delay

    # advanced stats only if sql_log is enabled
    if self.sql_log:
        delay *= 1E6

        query_lower = self._obj.query.decode().lower()
        res_from = re_from.match(query_lower)
        if res_from:
            self.sql_from_log.setdefault(res_from.group(1), [0, 0])
            self.sql_from_log[res_from.group(1)][0] += 1
            self.sql_from_log[res_from.group(1)][1] += delay
        res_into = re_into.match(query_lower)
        if res_into:
            self.sql_into_log.setdefault(res_into.group(1), [0, 0])
            self.sql_into_log[res_into.group(1)][0] += 1
            self.sql_into_log[res_into.group(1)][1] += delay
    # print("for update nowait",res)
    return res
Cursor.execute = execute
