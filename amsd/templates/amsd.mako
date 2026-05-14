<%inherit file="app.mako"/>
<%block name="title">${_('Home')}</%block>
<%block name="brand">
    <a href="${request.resource_url(request.dataset)}" class="brand">${request.dataset.name}</a>
</%block>

${next.body()}

<%block name="footer">
    <div class="row-fluid" style="padding-top: 15px; border-top: 1px solid black;">
        <div class="span3">
            <a href="${request.dataset.publisher_url}"
               title="${request.dataset.publisher_name}, ${request.dataset.publisher_place}">
            % if request.registry.settings.get('clld.publisher_logo'):
                <img width="80" src="${request.static_url(request.registry.settings['clld.publisher_logo'])}" />
            % else:
                ${request.dataset.publisher_name}, ${request.dataset.publisher_place}
            % endif
            </a>
        </div>
        <div class="span6" style="text-align: center;">
            ${request.dataset.formatted_name()}
            edited by
            <span xmlns:cc="https://creativecommons.org/ns#"
                  property="cc:attributionName"
                  rel="cc:attributionURL">
                ${request.dataset.formatted_editors()}
           </span>
        </div>
        <div class="span3" style="text-align: right;">
            % if request.registry.settings.get('clld.privacy_policy_url'):
                <a class="clld-privacy-policy" href="${request.registry.settings['clld.privacy_policy_url']}">${_('Privacy Policy')}</a><br/>
            % endif
            <a class="clld-disclaimer" href="${request.route_url('legal')}">${_('Disclaimer')}</a>
            <br/>
            % if request.registry.settings.get('clld.github_repos'):
            <a href="https://github.com/${request.registry.settings['clld.github_repos']}">
                <i class="icon-share">&nbsp;</i>
                Application source
                % if request.registry.settings['clld.git_tag']:
                    (${request.registry.settings['clld.git_tag']})
                % endif
                on<br/>
                <img height="25" src="${request.static_url('clld:web/static/images/GitHub_Logo.png')}" />
            </a>
            % endif
        </div>
    </div>
</%block>
