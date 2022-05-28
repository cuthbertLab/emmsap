#!/usr/bin/python

import cgi_helper
import cgitb
import sys

try:
    f = cgi_helper.form()
    a = cgi_helper.abe(f)
    a.searchTN()
except Exception as e:
    cgitb.handler(sys.exc_info())
