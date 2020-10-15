import pytest


@pytest.mark.parametrize(
    "method,path",
    [
        ('get_html', '/'),
        ('get_html', '/legal'),
        ('get_html', '/download'),
        ('get_html', '/sources'),
        ('get_html', '/sources/33'),
        ('get_html', '/contributions'),
        ('get_html', '/contributions?keywords=&sem_domain=sd_acculturation'),
        ('get_html', '/contributions?keywords=&material=bark'),
        ('get_html', '/contributions?keywords=&technique=carved'),
        ('get_html', '/contributions?keywords=&keywords=500_29218'),
        ('get_html', '/contributions/AB1881P192'),
        ('get_html', '/contributions/AB1881P192.snippet.html'),
        ('get_html', '/contributions/PRM1989_46_3.snippet.html?keywords=500_29218&sem_domain=&material=&technique=&map_pop_up=1&map_pop_up=1'),
    ])
def test_pages(app, method, path):
    getattr(app, method)(path)
