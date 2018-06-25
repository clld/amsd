<%inherit file="../home_comp.mako"/>

<h2>Welcome to the Australian Message Stick Database</h2>

<p class="lead">
    Message sticks are carved graphic devices from Indigenous Australia, used to
    facilitate long-distance communication. This database is a digital
    repository of 1024 message sticks and associated metadata located in museums
    across the world. It also stores photographs and sketches of messages that
    are no longer extant. The database is searchable via 30 fields, including
    linguistic area, semantic domain, motifs and source. The full dataset will
    be migrated to this location soon. In the meantime click <a
        href="https://cdhrsys.anu.edu.au/occams_v1c/index.php" target="_blank">here</a>
    to visit the beta version and the Help link for access instructions.
</p>

<h2>Example</h2>
<img width="180" height="180"
     src="${request.static_url('amsd:static/1520350500.png')}" class="image"/>

<p>
    The Australian Message Stick Database contains data licensed under various
    conditions depending on agreements with museums (see individual records for
    details). No restricted or sacred items are included. It has been developed
    by The Mint Research Group at The Max Planck Institute for the Science of
    Human History.
</p>

<h3>How to access the Australian Message Sticks Database</h3>
<p>The beta version can be accessed from <a
        href="https://cdhrsys.anu.edu.au/occams_v1c/index.php">https://cdhrsys.anu.edu.au/occams_v1c/index.php</a>.<br/>
    Please contact Piers Kelly (kelly [AT] shh.mpg.de) for log-in credentials or
    for a zipped copy of the database.
</p>

<div class="row-fluid">
    <div class="span4 well well-small">
        <h3>How to cite:</h3>
        <p>
            Kelly, Piers (ed.). 2018. The Australian Message Stick Database
            (beta version)
        </p>
    </div>
    <div class="span4" style="padding: 20px; text-align: center;">
        <img width="200" height="200"
             src="${request.static_url('amsd:static/amsd_logo.png')}"
             class="image"/>
    </div>
    <div class="span4">
        <table class="table table-nonfluid">
            <tbody>
            <tr>
                <th>Artefacts</th>
                <td class="right">1024</td>
            </tr>
            <tr>
                <th>Linguistic areas</th>
                <td class="right">54</td>
            </tr>
            <tr>
                <th>Motifs</th>
                <td class="right">37</td>
            </tr>
            </tbody>
        </table>
    </div>
</div>

