% if obj:
    <input type="text" autocomplete="off" autocorrect="off" autocapitilize="off" spellcheck="false" placeholder="${obj.options.get('placeholder', 'Search')}" class="${obj.options.get('class', '')}" id="${obj.eid}" value="${obj.value or ''}" name="${obj.query_name}" title="Search for a maximum of 8 terms, separated by spaces, in all text fields. A terms can be wrapped by double quotes for a phrase search.">
% endif