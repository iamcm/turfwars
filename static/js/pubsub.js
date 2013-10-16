

var getMessageFailedAttempts = 0;

var readMessageIds = []

function getMessages(){
	if(getMessageFailedAttempts < 10) {
		var data = {
			'readIds':readMessageIds
		}
		$.ajax("/message/subscribe", {'timeout':'25000', 'data':data})
		.done(function(data){
			//readMessageIds = [];

			if(data['messages']){

				$.each(data['messages'], function(i, el){
					readMessageIds.push(el._id);
				})

				var obj = data['messages'][0];

				if(obj){
					readMessageIds.push(obj._id);

					if(obj.type == 'challenge'){
						Util.FlashMessage.show('info', 'You have been challenged to a battle - <a href="/battle/'+ obj.data.battle_id +'">accept</a>', 150000);
					}
					else if(obj.type == 'reload'){
						$.ajax('/message/read/'+ obj._id).done(function(){
							window.setTimeout(function(){
								window.location.reload();
							},10)
						});
					}	
				}				
			}

		}).error(function(){
			getMessageFailedAttempts += 1;
		}).always(function(){
			setTimeout(getMessages, 250)
		});
	}
}

getMessages();