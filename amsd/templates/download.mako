<%inherit file="${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="util.mako"/>

<h3>Download</h3>

<div class="alert alert-success">
    <p>
        The AMSD data is curated in a repository on Github - ${h.external_link('https://github.com/clld/amsd-data')},
        with this web application providing the latest version.<br />
        To access the full data, please clone or download this repository.
    </p>
</div>