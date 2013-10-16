Util = {}

Util.FlashMessage = {
    
    /**
    * show a message at the top of the screen on a coloured background 
    * based on the message type.
    * Standard bootstrap messagetypes are used:
    *   alert, error, success, info 
    * e.g.
    *   Util.flashMessage('error', 'An error has occured');
    *   Util.flashMessage('success', 'Something great has happened', 15000);
    */
    show: function (messagetype, message, timeout) {

        var html = '<div class="alert alert-' + messagetype + '">';
        html += '<button type="button" class="close" data-dismiss="alert">&times;</button>';
        html += message + '</div>'

        if ($('#flashmessagecontent').length < 1) {
            var content = Util.Html.div({ id: 'flashmessagecontent' });
            var container = Util.Html.div({ id: 'flashmessagecontainer', content: content });

            $('body').append(container);
        }

        $('#flashmessagecontent').html(html);

        setTimeout(function () {
            if ($('#flashmessagecontent')) $('#flashmessagecontent').fadeOut(function () {
                $(this).html('').show();
            });
        }, timeout || 7000)
    },

    hide: function () {
        $('#flashmessagecontent').html('');
    }
}


Util.Html = {
    /**
     * obj.content
     * obj.id
     * obj.classname
     * obj.style
     */
    div:function(obj){
        
        var id = (obj.id) ? ' id="'+ obj.id +'"' : '' ;
        var classname = (obj.classname) ? ' class="'+ obj.classname +'"' : '' ;
        var style = (obj.style) ? ' style="'+ obj.style +'"' : '' ;
        
        return '<div'+ id + classname + style +'>'+ obj.content +'</div>';
        
    },
    
    /**
     * obj.content
     * obj.id
     * obj.classname
     * obj.style
     * obj.title
     */
    span:function(obj){
        
        var id = (obj.id) ? ' id="'+ obj.id +'"' : '' ;
        var classname = (obj.classname) ? ' class="'+ obj.classname +'"' : '' ;
        var style = (obj.style) ? ' style="'+ obj.style +'"' : '' ;
        var title = (obj.title) ? ' title="'+ obj.title +'"' : '' ;
        
        return '<span'+ id + classname + style + title +'>'+ obj.content +'</span>';
    }    
}

Util.String = {
    trim:function(string, maxlength, addTitle){       
        if(string.length > length){
            var output = string.slice(0, maxlength) + '...';
            
            if(addTitle){
                output = Util.Html.span({
                    'content':output,
                    'title':string
                })
            }
        } else {
            var output = string;
        }   
        
        return output;
    }
}

Util.Templating = {
    renderTemplate:function(templateid, context, targetid, fadeInEl){
        var source = $('#'+ templateid).html();
        source = source.replace(/\[\[/g, '{{');
        source = source.replace(/\]\]/g, '}}');
        var template = Handlebars.compile(source);
        $('#'+ targetid).html(template(context));
        $(fadeInEl).fadeIn(50);
    }
}