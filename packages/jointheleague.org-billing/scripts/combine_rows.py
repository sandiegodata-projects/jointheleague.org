#! /usr/bin/env python -u
#
# Merge all of the billing records into a single file. Iterates over all of
# the references in the source package and emits the rows after a little
# processing
#

#
# NOTE! this isn't used! It's just haning around as an example. See
# lib/

import sys
import csv

from os import environ
from metapack import MetapackDoc, parse_app_url, Downloader

fields = 'group type date num name memo class clr split amount balance '.split()

w = csv.DictWriter(sys.stdout, fields)
w.writeheader()

doc = MetapackDoc(parse_app_url(environ['METATAB_DOC'], downloader=Downloader()))

try:
    for r in doc.references():
        
        group = 'ns' if 'paid' in r.name else 's'
    
        for row in r.iterdict:
    
            if row['name'] and row['name'].strip():

                del row['account']
                row['group'] = group
                row['split'] = ''

                w.writerow(row)

except BrokenPipeError:
    # Parent exited before we wrote everything. This is almost guaranteed to 
    # happen while building schemas with `metapack -s`
    pass

        
