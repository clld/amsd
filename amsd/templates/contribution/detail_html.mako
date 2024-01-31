<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "contributions" %>

<%block name="title">${_('Contribution')} ${ctx.id}</%block>

% if ctx.latitude:
<div class="well well-small pull-right" style="width:30%;padding:10px;margin-top:10px;margin-left:20px">
    ${(map_ or request.map).render()}
    ${h.format_coordinates(ctx)}
</div>
% endif

<div style='float: right;padding: 20px'>${h.contactmail(request, ctx, title="Give feedback")}</div>

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
% if ctx.item_subtype:
    <p><b>Subtype: </b>${ctx.item_subtype}</p>
% endif
% if ctx.ling_area_1:
    <p><b>Linguistic area 1: </b>
        % if ctx.ling_area_1.chirila_name:
            ${h.external_link('https://www.pamanyungan.net/', label='Chirila')}: ${ctx.ling_area_1.chirila_name}
        % endif
        % if ctx.ling_area_1.austlang_code or ctx.ling_area_1.austlang_name:
            %if ctx.ling_area_1.austlang_code:
                ${h.external_link('https://collection.aiatsis.gov.au/austlang/language/'+ctx.ling_area_1.austlang_code, label='Austlang: %s - %s' % (ctx.ling_area_1.austlang_code, ctx.ling_area_1.austlang_name))}
            % endif
        % endif
        % if ctx.ling_area_1.glottolog_code:
            ${h.external_link('https://glottolog.org/resource/languoid/id/'+ctx.ling_area_1.glottolog_code, label='Glottolog: '+ctx.ling_area_1.glottolog_code)}
        % endif
    </p>
% endif
% if ctx.ling_area_2:
    <p><b>Linguistic area 2: </b>
        % if ctx.ling_area_2.chirila_name:
            ${h.external_link('https://www.pamanyungan.net/', label='Chirila')}: ${ctx.ling_area_2.chirila_name}
        % endif
        % if ctx.ling_area_2.austlang_code or ctx.ling_area_2.austlang_name:
            %if ctx.ling_area_2.austlang_code:
                ${h.external_link('https://collection.aiatsis.gov.au/austlang/language/'+ctx.ling_area_2.austlang_code, label='Austlang: %s - %s' % (ctx.ling_area_2.austlang_code, ctx.ling_area_2.austlang_name))}
            % endif
        % endif
        % if ctx.ling_area_2.glottolog_code:
            ${h.external_link('https://glottolog.org/resource/languoid/id/'+ctx.ling_area_2.glottolog_code, label='Glottolog: '+ctx.ling_area_2.glottolog_code)}
        % endif
    </p>
% endif
% if ctx.ling_area_3:
    <p><b>Linguistic area 3: </b>
    % if ctx.ling_area_3.chirila_name:
        ${h.external_link('https://www.pamanyungan.net/', label='Chirila')}: ${ctx.ling_area_3.chirila_name}
    % endif
    % if ctx.ling_area_3.austlang_code or ctx.ling_area_3.austlang_name:
        %if ctx.ling_area_3.austlang_code:
            ${h.external_link('https://collection.aiatsis.gov.au/austlang/language/'+ctx.ling_area_3.austlang_code, label='Austlang: %s - %s' % (ctx.ling_area_3.austlang_code, ctx.ling_area_3.austlang_name))}
        % endif
    % endif
    % if ctx.ling_area_3.glottolog_code:
        ${h.external_link('https://glottolog.org/resource/languoid/id/'+ctx.ling_area_3.glottolog_code, label='Glottolog: '+ctx.ling_area_3.glottolog_code)}
    % endif
    </p>
% endif
% if ctx.notes_ling_area:
    <p><b>Notes on linguistic areas: </b>${ctx.notes_ling_area}</p>
% endif
% if ctx.cultural_region:
    <p><b>Cultural region: </b>${ctx.cultural_region}</p>
% endif
% if ctx.stick_term:
    <p><b>Term for 'message stick' (or related) in language: </b>${ctx.stick_term}</p>
% endif
% if ctx.motifs:
    <p><b>Motifs: </b>${ctx.motifs}</p>
% endif
% if ctx.motif_transcription:
    <p><b>Motif transcription: </b>${ctx.motif_transcription}</p>
% endif
% if semantic_domains:
    <p><b>Semantic domains: </b>${semantic_domains|n}</p>
% endif
% if ctx.dim_1 or ctx.dim_2 or ctx.dim_3:
    <p>
        % if ctx.dim_1:
            <b>Dimension 1: </b>${ctx.dim_1}mm
        % endif
        % if ctx.dim_2:
            <b>Dimension 2: </b>${ctx.dim_2}mm
        % endif
        % if ctx.dim_3:
            <b>Dimension 3: </b>${ctx.dim_3}mm
        % endif
    </p>
% endif
% if materials:
    <p><b>Materials: </b>${materials|n}</p>
% endif
% if techniques:
    <p><b>Techniques: </b>${techniques|n}</p>
% endif
% if ctx.references:
    <p><b>Sources: </b>${u.amsd_linked_references(request, ctx)}</p>
% endif
% if source_types:
    <p><b>Source types: </b>${source_types|n}</p>
% endif
% if ctx.date_collected:
    <p><b>Date collected: </b>${ctx.date_collected}</p>
% endif
% if ctx.holder_file:
    <p><b>Institution/Holder file: </b>${ctx.holder_file}
% endif
% if ctx.holder_obj_id:
    <b>object identifier: </b>${ctx.holder_obj_id}</p>
% endif
% if ctx.collector:
    <p><b>Collector: </b>${ctx.collector}</p>
% endif
% if ctx.place_collected:
    <p><b>Place collected: </b>${ctx.place_collected}</p>
% endif
% if ctx.latitude:
    <p><b>Coordinates: </b>${u.degminsec(ctx.latitude, 'NS')},${u.degminsec(ctx.longitude, 'EW')}&nbsp;&nbsp;(${ctx.latitude}, ${ctx.longitude})
% endif
% if ctx.creator_copyright:
    <p><b>Creator copyright: </b>${ctx.creator_copyright}</p>
% endif
% if ctx.file_copyright:
    <p><b>Media copyright: </b>${ctx.file_copyright}</p>
% endif
% if ctx.notes_coords:
    <p><b>Notes on coordinates: </b>${ctx.notes_coords}</p>
% endif
% if ctx.url_institution:
    <p><b>URL institution: </b>
    % for url in ctx.url_institution.split('  '):
        ${h.external_link(url, label=url)}
    % endfor
    </p>
% endif
% if ctx.url_source_1:
    <p><b>URL source 1: </b>
    % for url in ctx.url_source_1.split(' '):
        ${h.external_link(url, label=url)}
    % endfor
    </p>
% endif
% if ctx.url_source_2:
    <p><b>URL source 2: </b>
    % for url in ctx.url_source_2.split(' '):
        ${h.external_link(url, label=url)}
    % endfor
    </p>
% endif
% if ctx.irn:
    <p><b>IRN: </b>${ctx.irn}</p>
% endif
% if ctx.notes:
    <p><b>Notes: </b>${ctx.notes}</p>
% endif
% if linked_filename_urls:
    <p><b>Media Files:</b></p>
    <p>${linked_filename_urls|n}</p>
% endif
% if data_entry:
    <p><b>Data Entry: </b>${data_entry|n}</p>
% endif
% if ctx.related_entries:
    <p><b>Related Entries: </b>
        ${u.format_related_entries(ctx.related_entries, request)|n}
    </p>
% endif


