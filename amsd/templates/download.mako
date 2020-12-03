<%inherit file="${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="util.mako"/>

<h3>Download</h3>
<p>
  So far no downloadable data available. Please contact the author <a href="mailto:${request.contact_email_address}">${request.dataset.editors[0].contributor.name}</a>.
</p>
