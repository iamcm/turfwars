

<div class="col-xs-12">
	%if vd['battle'].ended:
		<div class="alert alert-success">
			<div>The battle is over</div>
			<div>{{vd['battle'].loser.email}} was defeated!</div>
			<div>
				<a href="/">Return</a>
			</div>
		</div>
	%else:
		<div class="alert alert-info">
			%if vd['battle'].latest_action:
				<div>{{vd['battle'].latest_action}}</div>
			%end

			<div>
			%if vd['current_session_user_id'] != vd['battle'].turn_of_user._id:
				Waiting for {{vd['battle'].turn_of_user.email}} to take their turn...
			%else:
				Its your turn!
			%end
			</div>
		</div>

		%for u in vd['battle'].users:
			<div class="row">
				%if vd['current_session_user_id'] != u._id and vd['current_session_user_id'] == vd['battle'].turn_of_user._id:
					<a href="/attack/{{vd['battle']._id}}/{{u._id}}" class="btn btn-default pull-right">Attack!</a>
				%end
				{{u.email}} - Health: {{u.userdata.health}}
			</div>
		%end
	%end
</div>



%rebase base vd=vd