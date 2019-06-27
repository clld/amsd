% if ctx.description:
    <p><b>Description: </b>${ctx.description}</p>
% endif
% if ctx.message:
    <p><b>Message: </b>${ctx.message}</p>
% endif
% if ctx.references:
    <p><b>Sources: </b>${u.amsd_linked_references(request, ctx)}</p>
% endif
