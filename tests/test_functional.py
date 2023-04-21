import pytest


@pytest.mark.parametrize(
    "method,path",
    [
        ('get_html', '/'),
        ('get_html', '/legal'),
        ('get_html', '/download'),
        ('get_html', '/images'),
        ('get_html', '/images/1-1-0'),
        ('get_html', '/images?&sSearch_0=Artefact11'),
        ('get_html', '/sources'),
        ('get_html', '/sources/33'),
        ('get_html', '/contributors'),
        ('get_html', '/contributors/1'),
        ('get_html', '/contributions'),
        ('get_html', '/contributions?keywords=&sem_domain=sd_acculturation'),
        ('get_dt', '/contributions?keywords=&sem_domain=sd_acculturation'),
        ('get_html', '/contributions?keywords=&keywords=500_29218'),
        ('get_html', '/contributions?sSearch_5=camp%20daw'),
        ('get_dt', '/contributions?sSearch_5=camp%20daw'),
        ('get_dt', '/contributions?sSearch_5=a:'),
        ('get_html', '/contributions/AB1881P192'),
        ('get_html', '/contributions/GALITJU2007'),
        ('get_html', '/contributions/AB1881P192.snippet.html'),
        ('get_html', '/contributions/PRM1989_46_3.snippet.html?keywords=500_29218&sem_domain=&material=&technique=&map_pop_up=1&map_pop_up=1'),
    ])
def test_pages(app, method, path):
    getattr(app, method)(path)
