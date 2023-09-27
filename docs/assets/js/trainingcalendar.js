
function fetchActiveDays(callback) {
	var httpRequest = new XMLHttpRequest();
	httpRequest.onreadystatechange = function() {
		if (httpRequest.readyState === 4) {
			if (httpRequest.status === 200) {
				var data = JSON.parse(httpRequest.responseText);
				if (callback) callback(data);
			}
		}
	};
	httpRequest.open('GET', '/assets/activedays.json');
	httpRequest.send();
}

function weeklypage(data) {
	var index = 0;
	while (index < data.activedays.length) {
		var id = 'c' + data.activedays[index];
		document.getElementById(id).style.background = '#ddf3ff';
		index++;
	}
	return;
}

function fullcalendar(data) {
	var pct = Number((data.activedays.length / data.totaldays)).toLocaleString(undefined,{style: 'percent', minimumFractionDigits:1});
	document.getElementById('tdc').innerHTML = data.totaldays;
	document.getElementById('adc').innerHTML = data.activedays.length;
	document.getElementById('adp').innerHTML = pct;
	weeklypage(data);
	if(screen.availHeight < screen.availWidth) {
    	flkty.select(2);
	}	
}


function cellClick(w,d) {
	var url = 'triathlon2024-' + w + 'weeksout?' + d;
	alert(url);
}
