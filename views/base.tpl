<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <title>Turfwars</title>

    <link href="/static/bootstrap/css/bootstrap.min.css" rel="stylesheet">
    <link href="/static/css/generic.css" rel="stylesheet">
    <link href="/static/css/site.css" rel="stylesheet">

</head>

<body>

    <div class="navbar navbar-fixed-top navbar-inverse" role="navigation">
        <div class="container">
            <div class="navbar-header">
                <button type="button" class="navbar-toggle" data-toggle="collapse" data-target=".navbar-collapse">
                    <span class="icon-bar"></span>
                    <span class="icon-bar"></span>
                    <span class="icon-bar"></span>
                </button>
                <a class="navbar-brand" href="/">Turfwars</a>
            </div>
            <div class="collapse navbar-collapse">
                <ul class="nav navbar-nav pull-right">
                    %if defined('vd') and 'logged_in_user' in vd:
                        <li>
                            <a>{{vd['logged_in_user'].email}}</a>
                        </li>
                    %end
                </ul>
            </div>
        </div>
    </div>

    <div class="container">

        %include

        %if defined('page'):
            %page()
        %else:
        <div class="row">
            <div class="col-sm-12">

            </div>
        </div>
        %end

    </div>

    <script src="/static/js/jquery.js"></script>
    <script src="/static/bootstrap/js/bootstrap.min.js"></script>
    <script src="/static/tinymce/js/tinymce/tinymce.min.js"></script>
    <script src="/static/js/site.js"></script>
    <script src="/static/js/util.js"></script>
    <script src="/static/js/pubsub.js"></script>

    %if defined('js'):
        %js()
    %end

</body>
</html>