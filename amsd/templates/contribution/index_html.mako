
<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "contributions" %>
<%block name="title">${_('Contributions')}</%block>

<%block name="head">
    <link href="${request.static_url('clld:web/static/css/select2.css')}" rel="stylesheet">
    <script src="${request.static_url('clld:web/static/js/select2.js')}"></script>
</%block>

<h2>${title()}</h2>

<div class="nav nav-pills pull-right" style="margin-top:-60px">
    <li class="">
        <a href="#map-container">
            <img src="${request.static_url('amsd:static/Map_Icon.png')}" width="35">
            Map
        </a>
    </li>
</div>

<div class="clearfix"> </div>

<div class="pull-left well" style="margin-top: -14px; padding: 5px 5px">
    <form id="prefilter-form">
        % if len(remotefields):
          <div class="pull-left">
            <i>Pre-filtering</i>
            <fieldset>
              % for rf in remotefields:
                <div class="pull-left select2-container select2-container-multi" style="margin:5px"><b>${rf.label}: </b>
                  % if rf.description:
                    <i title="${rf.description}" class="icon-info-sign"></i>
                  % endif
                  <br />
                  <ul class="select2-choices"><li class="select2-search-field">${rf.render()}</li></ul>
                </div>
              % endfor
              <div class="pull-left select2-container select2-container-multi" style="margin:5px;"><b>&nbsp;</b>
                <br />
                <button onclick="$('#prefilter-form').submit()" style="height: 34px"><i class="icon-search"></i></button>
              </div>
            </fieldset>
          </div>
        % endif
        <div class="pull-left">
          <i>Pre-filtering of multiple shared values</i>
          <fieldset onchange="submit()">
            <div class="pull-left" style="margin:5px"><b>Semantic domains:</b><br />${select_sem_domain.render()}</div>
            <div class="pull-left" style="margin:5px"><b>Keywords:</b><br />${select_keywords.render()}</div>
          </fieldset>
        </div>
    </form>
</div>

<div class="clearfix"> </div>

<div id="table-container">
    ${ctx.render()}
</div>

<div class="clearfix"> </div>

<div id="map-container" style="margin-top:20px">
    %if count_loc_note:
        <i><small>${count_loc_note}</small></i>
    % endif
    ${(map_ or request.map).render()}
</div>
