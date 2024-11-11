<%inherit file="../home_comp.mako"/>

<div class=" pull-left" style="padding: 10px; width: 38%">
    <div  style="text-align: center;">
        <img width="80%"
             src="${request.static_url('amsd:static/amsd_logo.png')}"
             class="image"/>
        % if example:
            <h5>Example</h5>
            <a href="${example['link_url']}">
                <img style="width: 80%; margin: 20px"
                     src="${example['image_url']}" class="image"/>
            </a>
        % endif
        <table class="table">
            <tbody>
            <tr>
                <th>Artefacts</th>
                <td class="right">${count_sticks}</td>
                <td>&nbsp;</td>
            </tr>
            <tr>
                <th>Linguistic areas</th>
                <td class="right">${count_ling_areas}</td>
                <td>&nbsp;</td>
            </tr>
            <tr>
                <th>Terms for message stick</th>
                <td class="right">${count_terms}</td>
                <td>&nbsp;</td>
            </tr>
        </tbody>
        </table>
    </div>
    <div class="well well-small pull-left" style="width: 95%">
        <h4>How to cite:</h4>
        <p>
            Kelly, Piers, Junran Lei, Hans-Jörg Bibiko, and Lorina Barker. 2024.<br />"AMSD: The Australian Message Stick Database."<br />
            PLOS One 19 (4): e0299712. doi: <a href="https://doi.org/10.1371/journal.pone.0299712">https://doi.org/10.1371/journal.pone.0299712</a>
        </p>
    </div>
</div>

<div class="fluid pull-right" style="width: 58%;margin-right: 6px">
    <h3>Welcome to the Australian Message Stick Database</h3>

    <p class="lead">
        Message sticks are carved graphic devices from Indigenous Australia, used to
        facilitate long-distance communication. This database is a digital
        repository of ${count_sticks} message sticks and associated metadata located in museums
        across the world. It also stores photographs and sketches of messages that
        are no longer extant.
    </p>

    <h4>Sensitivity notice</h4>

    <h5>Artefacts and entries</h5>
    <p>Message sticks are public communication devices that go by many different names in Australian languages.
    Note that the English term 'message stick' is sometimes mistakenly used to refer to non-public sacred objects,
    of similar appearance, used in parts of Central and Western Australia. No sacred materials are included here.
    Each entry in the dataset is created from a composite of public sources, including manuscripts,
    published papers, and museum catalogues. The AMSD makes no representations, warranties or assurances
    (either expressed or implied) as to the accuracy, currency or completeness of the cited sources that
    inform each entry. Users of this dataset are also advised that locations of language groups or places
    shown on the map are approximate and are not to be used for land or native title claims.</p>

    <h5>Access conditions, copyright and ICIP</h5>
    <p>The AMSD does not claim or own any copyright or ICIP over any of the information, including records
    produced through our own field research. The dataset is intended for personal study only. For any other uses
    please review information in each record to find the traditional owners of the material (if available),
    the institution responsible for copyright management, and the original sources. Note that all non-public
    sources are excluded from the dataset. If you believe that we have included a source in error, please
    contact us.</p>

    <h5>Deceased persons</h5>
    <p>Users of the dataset should be aware that in some Aboriginal and Torres Strait Islander communities,
    seeing images of deceased kin may cause distress and violate cultural prohibitions. A small number of entries
    includes images of people who are now deceased.</p>

    <h5>Digital repatriation policy</h5>
    <p>The images and metadata within this dataset are sourced from many locations across the world, but have a
    special value within their communities of origin. We respect the rights of Indigenous communities to retain
    full access to their cultural heritage and control over ICIP. We will make every effort to help re-archive
    materials of interest in local repositories with the participation of collecting institutions.</p>
</div>