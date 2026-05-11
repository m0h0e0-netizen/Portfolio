
function tick() {
   var date = new Date();
   var seconds = date.getSeconds();
   var minutes = date.getMinutes();
   var hours = date.getHours();
   
    Date.prototype.monthNames = ["January","February","March","April","May","June","July","August","September","October","November","December"];
   Date.prototype.getMonthName = function() {
    return this.monthNames[this.getMonth()];
};
  Date.prototype.getShortMonthName = function () {
    return this.getMonthName().substr(0, 3);
};
   var day = date.getDate()+"-"+date.getShortMonthName();

var date1 = new Date();

 Date.prototype.weekName = ["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"];
   Date.prototype.getWeekName = function() {
    return this.weekName[this.getDay()];
};
  Date.prototype.getShortWeekName = function () {
    return this.getWeekName().substr(0, 3);
}; 
   var day1 = date1.getShortWeekName();     

   
  


var date2 = new Date();

 Date.prototype.weekName = ["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"];
   Date.prototype.getWeekName = function() {
    return this.weekName[this.getDay()];
};
  Date.prototype.getShortWeekName = function () {
    return this.getWeekName().substr(0, 1);
}; 
   var day2 = date2.getShortWeekName();     

   var date3 = new Date();
   var hours = date3.getHours();
var minutes = date3.getMinutes();
  var ampm = hours >= 12 ? 'pm' : 'am';
  hours = hours % 12;
  hours = hours ? hours : 12; // the hour '0' should be '12'
  minutes = minutes < 10 ? '0'+minutes : minutes;
   var day3 = hours+":"+minutes+" " +ampm;
  
   $('.date').text(day);
   $('.date1').text(day1);
   $('.date2').text(day2);
    $('.date3').text(day3);
}

setInterval(tick, 100);


(function(){

            //generate clock animations
 Date.prototype.weekName = ["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"];
   Date.prototype.getWeekName = function() {
    return this.weekName[this.getDay()];
};
  Date.prototype.getShortWeekName = function () {
    return this.getWeekName().substr(0, 1);
};
 var now       = new Date(),
		weekarrow   = now.getShortWeekName()/ 7 * 155 + now.getHours() / 24 * 720, 
		days1   = now.getDay()/ 6 * 155 + now.getHours() / 2 * 12 * 360, 		
		hours   = now.getHours() / 12 * 360 + now.getMinutes() / 60 * 30,
                minutes = now.getMinutes() / 60 * 360 + now.getSeconds() / 60 * 6,
                seconds = now.getSeconds() / 60 * 360,
                stylesDeg = [
		    
		    "@-webkit-keyframes rotate-day{from{transform:rotate(" + weekarrow + "deg);}to{transform:rotate(" + (weekarrow + 150) + "deg);}}", 
		    "@-webkit-keyframes rotate-day{from{transform:rotate(" + (days1 - 95) + "deg);}to{transform:rotate(" + (days1 + 60) + "deg);}}",
		    "@-webkit-keyframes rotate-hour{from{transform:rotate(" + hours + "deg);}to{transform:rotate(" + (hours + 360) + "deg);}}",
                    "@-webkit-keyframes rotate-minute{from{transform:rotate(" + minutes + "deg);}to{transform:rotate(" + (minutes + 360) + "deg);}}",
                    "@-webkit-keyframes rotate-second{from{transform:rotate(" + seconds + "deg);}to{transform:rotate(" + (seconds + 360) + "deg);}}",
   		    "@-moz-keyframes rotate-day{from{transform:rotate(" + weekarrow + "deg);}to{transform:rotate(" + (weekarrow + 150) + "deg);}}",
		    "@-moz-keyframes rotate-day{from{transform:rotate(" + (days1 - 95) + "deg);}to{transform:rotate(" + (days1 + 60) + "deg);}}",
                    "@-moz-keyframes rotate-hour{from{transform:rotate(" + hours + "deg);}to{transform:rotate(" + (hours + 360) + "deg);}}",
                    "@-moz-keyframes rotate-minute{from{transform:rotate(" + minutes + "deg);}to{transform:rotate(" + (minutes + 360) + "deg);}}",
                    "@-moz-keyframes rotate-second{from{transform:rotate(" + seconds + "deg);}to{transform:rotate(" + (seconds + 360) + "deg);}}"
                ].join("");

            document.getElementById("clock-animations").innerHTML = stylesDeg;

        })();	



