
<div class="container-fluid p10">
    
    %if vd.get('error'):
    <div class="alert alert-error">
        <button class="close" data-dismiss="alert">×</button>
        {{vd['error']}}
    </div>
    %end

    <form class="form-horizontal" id="loginForm" method='POST' action="/login" >
        
        <div class="form-group">

            <input type="text" class="form-control" name="email" id="email" value="{{vd.get('email') if vd.get('email') else ''}}" placeholder="Email" />
            
        </div>
        
        <div class="form-group">

            <input type="password" class="form-control" name="password" id="password" value="{{vd.get('password') if vd.get('password') else ''}}" placeholder="Password" />
        </div>
        
        <div class="form-group">

            <button type="submit" class="btn">Login</button>
            - <a href="/forgotten-password">Forgotten password?</a>
            
        </div>
        
    </form>
</div>

%rebase base_public
