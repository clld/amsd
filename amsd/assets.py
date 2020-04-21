import pathlib

from clld.web.assets import environment

import amsd


environment.append_path(
    str(pathlib.Path(amsd.__file__).parent.joinpath('static')), url='/amsd:static/')
environment.load_path = list(reversed(environment.load_path))
