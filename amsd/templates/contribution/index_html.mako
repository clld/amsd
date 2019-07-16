
<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "contributions" %>
<%block name="title">${_('Contributions')}</%block>

<%block name="head">
    <link href="${request.static_url('clld:web/static/css/select2.css')}" rel="stylesheet">
    <script src="${request.static_url('clld:web/static/js/select2.js')}"></script>
</%block>

<h2>${title()}</h2>

<div class="" style="padding: 0px 0px">
    <form>
        <i>Pre-filtering of multiple shared values</i>
        <fieldset onchange="submit()">
            <div class="pull-left" style="margin-right:5px"><b>Keywords:</b><br />${select_keywords.render()}</div>
            <div class="pull-left" style="margin-right:5px"><b>Semantic domains:</b><br />${select_sem_domain.render()}</div>
            <div class="pull-left" style="margin-right:5px"><b>Materials:</b><br />${select_material.render()}</div>
            <div class="pull-left" style="margin-right:5px"><b>Techniques:</b><br />${select_technique.render()}</div>
        </fieldset>
    </form>
</div>

<div class="clearfix"> </div>
<div>
    ${ctx.render()}
</div>
