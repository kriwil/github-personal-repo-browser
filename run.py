# -*- coding: utf-8 -*-

import os

from repo_browser import app


port = int(os.environ.get('PORT', 5000))
app.run(debug=False)

