<%inherit file="app.mako"/>
<%block name="title">${_('Home')}</%block>
<%block name="brand">
    <a href="${request.resource_url(request.dataset)}" class="brand">${request.dataset.name}</a>
</%block>

${next.body()}
