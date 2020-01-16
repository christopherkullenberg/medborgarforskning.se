#
# File Name: test.py
# Description: test if the uwsgi configuration to serve applications is functioning
#
def application(env, start_response):
    start_response('200 OK', [('Content-Type','text/html')])
    return [b"Hello World"] # python3
