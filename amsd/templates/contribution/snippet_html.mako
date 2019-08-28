% if ctx.id:
    <p><h4>${h.link(request, ctx)}</h4></p>
% endif
% if request.params.get('map_pop_up'):
    % if ctx.title:
        <p><b>Title: </b>${ctx.title}</p>
    % endif
    ${u.get_popup_images(request, ctx)|n}
% else:
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
%if ctx.longitude:
<div>
    ${h.format_coordinates(ctx)}
</div>
% endif

