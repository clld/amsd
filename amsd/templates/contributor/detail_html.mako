<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "contributors" %>

<%block name="title">${_('Contributor')} ${ctx.id}</%block>
<h2>${_('Contributor')}</h2>
<p>${ctx.name}</p>


<%def name="sidebar()">
    <% referents, one_open = context.get('referents', {}), False %>
    <div class="accordion" id="sidebar-accordion">
    % if referents.get('contribution'):
        <%util:accordion_group eid="acc-c" parent="sidebar-accordion" title="${_('Contributions')}" open="${not one_open}">
            ${util.stacked_links(referents['contribution'])}
        </%util:accordion_group>
        <% one_open = True %>
    % endif
    </div>
</%def>
