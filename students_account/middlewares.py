import re
from django.db import connection
from operator import add
from time import time

class StatsMiddleware(object):

    def process_view(self, request, view_func, view_args, view_kwargs):
        """
        In your base template, put this:
        <div id="stats"><!-- STATS: Total: %(total_time).5fs <br/>
        Queries: %(queries)d --></div>
        otherwise statistics would be placed before </body> tag 
        """

        import settings
        if not settings.DEBUG:
            return None
        n = len(connection.queries)
        start = time()
        response = view_func(request, *view_args, **view_kwargs)
        total_time = time() - start
        queries_amount = len(connection.queries) - n
        stats = {'total_time': total_time,
                 'queries': queries_amount}
        out = "<hr />total time: %(total_time).5fs, queries: %(queries)d" % stats
        if response and response.content \
            and response['Content-Type'].find('text/html') != -1:
            s = response.content
            regexp = re.compile(r'(?P<cmt><!--\s*STATS:(?P<fmt>.*?)-->)')
            match = regexp.search(s)
            if match:
                s = s[:match.start('cmt')] + \
                    match.group('fmt') % stats + \
                    s[match.end('cmt'):]
            else:
                regexp = re.compile(r'(?P<cmt></body>)')
                match = regexp.search(s)
                s = s[:match.start('cmt')] + out + \
                    s[match.end('cmt'):]
            response.content = s
        return response
