from clld.web.assets import environment
from clldutils.path import Path

import amsd


environment.append_path(
    Path(amsd.__file__).parent.joinpath('static').as_posix(),
    url='/amsd:static/')
environment.load_path = list(reversed(environment.load_path))
