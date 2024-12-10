
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

function trainingweek(data) {
	var index = 0;
	while (index < data.activedays.length) {
		var id = 'c' + data.activedays[index];
		try {
			var elmt = document.getElementById(id);
			if (elmt) elmt.style.background = '#c9e6ff';
		} catch(err) {
			return;
		}
		index++;
	}
	index = 0;
	while (index < data.offdays.length) {
		var id = 'c' + data.offdays[index];
		try {
			var elmt = document.getElementById(id);
			if (elmt) {
				if (elmt.style.background != '#c9e6ff') {
					elmt.style.textDecoration = 'line-through';
				}
				elmt.style.background = '#ffeef7';
			}
		} catch(err) {
			return;
		}
		index++;
	}
	scroll();
	return;
}

function fullcalendar(data) {
	var pct = Number((data.activedays.length / data.totaldays)).toLocaleString(undefined,{style: 'percent', minimumFractionDigits:1});
	document.getElementById('tdc').innerHTML = data.totaldays;
	document.getElementById('adc').innerHTML = data.activedays.length;
	document.getElementById('adp').innerHTML = pct;
	trainingweek(data);
	if(screen.availHeight < screen.availWidth) {
    	flkty.select(2);
	}	
	return;
}

function cellClick(w,d) {
	var url = '/training/'+yyyy+'-'+w+'-weeks-out?'+d;
	window.location.assign(url);
	return;
}
