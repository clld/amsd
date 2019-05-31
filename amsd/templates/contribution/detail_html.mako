<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "contributions" %>

<%block name="title">${_('Contribution')} ${ctx.id}</%block>
<h2>${ctx.id}</h2>
% if ctx.title:
    <p><b>Title: </b>${ctx.title}</p>
% endif
% if ctx.description:
    <p><b>Description: </b>${ctx.description}</p>
% endif
% if ctx.message:
    <p><b>Message: </b>${ctx.message}</p>
% endif
% if ctx.obj_creator:
    <p><b>Creator of Object: </b>${ctx.obj_creator}</p>
% endif
% if ctx.date_created:
    <p><b>Date Created: </b>${ctx.date_created}</p>
% endif
% if ctx.note_place_created:
    <p><b>Notes on date created: </b>${ctx.note_place_created}</p>
% endif
% if ctx.place_created:
    <p><b>Place Created: </b>${ctx.place_created}</p>
% endif
% if ctx.item_type:
    <p><b>Item type: </b>${ctx.item_type}</p>
% endif
% if ctx.ling_area_1:
    <p><b>Linguistic area 1: </b>
    % if ctx.ling_area_1.chirila_name:
        <i>Chirila:</i> ${ctx.ling_area_1.chirila_name}
    % endif
    % if ctx.ling_area_1.austlang_code or ctx.austlang_name:
        <i>Austlang:</i> 
        %if ctx.ling_area_1.austlang_code:
            ${ctx.ling_area_1.austlang_code}:
        % endif
        %if ctx.ling_area_1.austlang_name:
            ${ctx.ling_area_1.austlang_name}
        % endif
    % endif
    % if ctx.ling_area_1.glottolog_code:
        <i>Glottolog:</i> ${ctx.ling_area_1.glottolog_code}
    % endif
    </p>
% endif
% if ctx.ling_area_2:
    <p><b>Linguistic area 2: </b>
    % if ctx.ling_area_1.chirila_name:
        <i>Chirila:</i> ${ctx.ling_area_2.chirila_name}
    % endif
    % if ctx.ling_area_2.austlang_code or ctx.ling_area_2.austlang_name:
        <i>Austlang:</i> 
        %if ctx.ling_area_2.austlang_code:
            ${ctx.ling_area_2.austlang_code}:
        % endif
        %if ctx.ling_area_2.austlang_name:
            ${ctx.ling_area_2.austlang_name}
        % endif
    % endif
    % if ctx.ling_area_2.glottolog_code:
        <i>Glottolog:</i> ${ctx.ling_area_2.glottolog_code}
    % endif
    </p>
% endif
% if ctx.ling_area_3:
    <p><b>Linguistic area 3: </b>
    % if ctx.ling_area_3.chirila_name:
        <i>Chirila:</i> ${ctx.ling_area_3.chirila_name}
    % endif
    % if ctx.ling_area_3.austlang_code or ctx.ling_area_3.austlang_name:
        <i>Austlang:</i> 
        %if ctx.ling_area_3.austlang_code:
            ${ctx.ling_area_3.austlang_code}:
        % endif
        %if ctx.ling_area_3.austlang_name:
            ${ctx.ling_area_3.austlang_name}
        % endif
    % endif
    % if ctx.ling_area_3.glottolog_code:
        <i>Glottolog:</i> ${ctx.ling_area_3.glottolog_code}
    % endif
    </p>
% endif
% if ctx.notes_ling_area:
    <p><b>Notes on linguistic areas: </b>${ctx.notes_ling_area}</p>
% endif
% if data_entry:
    <p><b>Data Entry: </b>${data_entry|n}</p>
% endif
% if linked_filename_urls:
    <p><b>Media Files:</b></p>
    <p>${linked_filename_urls|n}</p>
% endif


