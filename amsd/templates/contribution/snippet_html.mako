% if ctx.id:
    <p><h4>${h.link(request, ctx)}</h4></p>
% endif
% if request.params.get('map_pop_up'):
    % if ctx.title:
        <p><b>Title: </b>${ctx.title}</p>
    % endif
    ${u.get_popup_images(request, ctx)|n}
% else:
    %if ctx.longitude:
    <div class="well well-small pull-right" style="width:30%;padding:10px;margin-top:10px;margin-left:20px">
        ${h.format_coordinates(ctx)}
    </div>
    % endif
    % if ctx.title:
        <p><b>Title: </b>${ctx.title}</p>
    % endif
    % if ctx.description:
        <p><b>Description: </b>${ctx.description}</p>
    % endif
    % if ctx.message:
        <p><b>Message: </b>${ctx.message}</p>
    % endif
    % if ctx.references:
        <p><b>Sources: </b>${u.amsd_linked_references(request, ctx)}</p>
    % endif
% endif
% if ctx.related_entries:
    <p><b>Related Entries: </b>
        ${u.format_related_entries(ctx.related_entries, request)|n}
    </p>
% endif
