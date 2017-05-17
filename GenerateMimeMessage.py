#!/usr/bin/python

import sys

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

if len(sys.argv) == 1:
    print("%s input-file:type ..." % (sys.argv[0]))
    #sys.exit(1)

combined_message = MIMEMultipart()
# for i in sys.argv[1:]:
#
#     with open(filename) as fh:
#         contents = fh.read()
#     sub_message = MIMEText(contents, format_type, sys.getdefaultencoding())
#     sub_message.add_header('Content-Disposition', 'attachment; filename="%s"' % (filename))
#     combined_message.attach(sub_message)

i = 'myscript.sh:text/x-shellscript'
j = 'cloud_config.data:text/cloud-config'
(filename, format_type) = j.split(":", 1)
format_type='text/cloud-config'
with open(filename) as fh:
    contents = fh.read()
sub_message = MIMEText(contents, format_type, sys.getdefaultencoding())
sub_message.add_header('Content-Disposition', 'attachment; filename="%s"' % (filename))
combined_message.attach(sub_message)

print(combined_message)