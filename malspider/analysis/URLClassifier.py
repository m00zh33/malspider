#  
#  Copyright (c) 2016-present, Cisco Systems, Inc. All rights reserved.
#
#  This source code is licensed under the BSD-style license found in the
#  LICENSE file in the root directory of this source tree. 
#

import sys
import yara
import os
from scrapy import log

class URLClassifier:
    yara_rules = yara.compile(filepaths=
        {'urls':os.path.join(os.getcwd(),'yara/url_rules.yar')}
    )

    @staticmethod
    def scan(uri):
        alerts = list()
        matches = URLClassifier.yara_rules.match(data=uri.encode('ascii', 'ignore'))
        if not len(matches) > 0:
            return alerts

        for match in matches['urls']:
           alert_reason = ", ".join([" ".join(t.split('_')) for t in match['tags']])
           alert_data = "\n".join([s['data'] for s in match['strings']])
           alerts.append((alert_reason, alert_data))
           log.msg("Yara URL Classification Match: " + alert_reason, level=log.INFO)
        return alerts
