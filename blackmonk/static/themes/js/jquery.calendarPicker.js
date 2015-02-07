jQuery.fn.calendarPicker = function(options) {
  // --------------------------  start default option values --------------------------
  if (!options.date) {
    options.date = new Date();
  }
  if (typeof(options.years) == "undefined")
    options.years=1;

  if (typeof(options.months) == "undefined")
    options.months=3;

  if (typeof(options.days) == "undefined")
    options.days=4;

  if (typeof(options.showDayArrows) == "undefined")
    options.showDayArrows=true;

  if (typeof(options.useWheel) == "undefined")
    options.useWheel=true;

  if (typeof(options.callbackDelay) == "undefined")
    options.callbackDelay=500;
	
  if (typeof(options.onSelect) == "undefined")
	options.onSelect = function() {}
  
  if (typeof(options.monthNames) == "undefined")
    options.monthNames = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];

  if (typeof(options.dayNames) == "undefined")
    options.dayNames = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];
	
  if (typeof(options.disablePrvDate) == "undefined")
    options.disablePrvDate = false;
	
  if (typeof(options.reYe) == "undefined")
    options.reYe = false;
  


  // --------------------------  end default option values --------------------------

  var calendar = {currentDate: options.date};
  calendar.options = options;

  //build the calendar on the first element in the set of matched elements.
  var theDiv = this.eq(0);//$(this);
  theDiv.addClass("cAl-hOrZtL");

  //empty the div
  theDiv.empty();


  var divYears = $("<div>").addClass("cAlYeR");
  var divMonths = $("<div>").addClass("cAlMnT");
  var divDays = $("<div>").addClass("cAlDaY");


  theDiv.append(divYears).append(divMonths).append(divDays);

  calendar.changeDate = function(date) {
    calendar.currentDate = date;

    var fillYears = function(date) {
      var year = date.getFullYear();
      var t = new Date();
      divYears.empty();
      var nc = options.years*2+1;
      //var w = parseInt((theDiv.width()-4-(nc)*4)/nc)+"px";
	  var w = options.colWidth; 
      for (var i = year - options.years; i <= year + options.years; i++) {
        var d = new Date(date);
        d.setFullYear(i);
        var span = $("<span>").addClass("cAlElM").attr("millis", d.getTime()).html(i).css("width",w);
        if (d.getYear() == t.getYear()){
          span.addClass("tOdAy");
			if (options.disablePrvDate == true){
			  dayIndex = $('.cAlYeR .cAlElM.tOdAy').index();
			  $('.cAlYeR .cAlElM').eq(dayIndex).addClass('dSbLd');
			  $('.cAlYeR .cAlElM').eq(dayIndex).prevAll().addClass('dSbLd');
			} 
		}
        if (d.getYear() == calendar.currentDate.getYear())
          span.addClass("aCtV");
        divYears.append(span);
      }
    }

    var fillMonths = function(date) {
      var month = date.getMonth();
      var t = new Date();
      divMonths.empty();
      var oldday = date.getDay();
      var nc = options.months*2+1;
      //var w = parseInt((theDiv.width()-4-(nc)*4)/nc)+"px";
	  var w = options.colWidth; 
      for (var i = -options.months; i <= options.months; i++) {
        var d = new Date(date);
        var oldday = d.getDate();
        d.setMonth(month + i);

        if (d.getDate() != oldday) {
          d.setMonth(d.getMonth() - 1);
          d.setDate(28);
        }
        var span = $("<span>").addClass("cAlElM").attr("millis", d.getTime()).html(options.monthNames[d.getMonth()]).css("width",w);
        if (d.getYear() == t.getYear() && d.getMonth() == t.getMonth()){
          span.addClass("tOdAy");
		 	if (options.disablePrvDate == true){
			  dayIndex = $('.cAlMnT .cAlElM.tOdAy').index();
			  $('.cAlMnT .cAlElM').eq(dayIndex).addClass('dSbLd');
			  $('.cAlMnT .cAlElM').eq(dayIndex).prevAll().addClass('dSbLd');
			} 
		}
        if (d.getYear() == calendar.currentDate.getYear() && d.getMonth() == calendar.currentDate.getMonth()){
          span.addClass("aCtV");
		  span.append('<b class="caret"></b>');
		  }
        divMonths.append(span);

      }
    }

    var fillDays = function(date) {
      var day = date.getDate();
      var t = new Date();
      divDays.empty();
      var nc = options.days*2+1;
      //var w = parseInt((theDiv.width()-4-(options.showDayArrows?12:0)-(nc)*4)/(nc-(options.showDayArrows?2:0)))+"px";
	  var w = options.colWidth; 
	  var dayIndex;
      for (var i = -options.days; i <= options.days; i++) {
        var d = new Date(date);
        d.setDate(day + i)
        var span = $("<span>").addClass("cAlElM").attr("millis", d.getTime())
        if (i == -options.days && options.showDayArrows) {
          span.addClass("prev");
        } else if (i == options.days && options.showDayArrows) {
          span.addClass("next");
        } else {
          span.html("<span class=dAyNuM>" + d.getDate() + "</span><span class='dAy'>" + options.dayNames[d.getDay()]+"</span>").css("width",w);
          if (d.getYear() == t.getYear() && d.getMonth() == t.getMonth() && d.getDate() == t.getDate()){
                span.addClass("tOdAy");
				if (options.disablePrvDate == true){
				  dayIndex = $('.cAlDaY .cAlElM.tOdAy').index();
				  $('.cAlDaY .cAlElM').eq(dayIndex).addClass('dSbLd');
				  $('.cAlDaY .cAlElM').eq(dayIndex).prevAll().addClass('dSbLd');
				}
		  }
          if (d.getYear() == calendar.currentDate.getYear() && d.getMonth() == calendar.currentDate.getMonth() && d.getDate() == calendar.currentDate.getDate())
            span.addClass("aCtV");
        }
        divDays.append(span);

      }
	  
    }

    var deferredCallBack = function() {
      if (typeof(options.callback) == "function") {
        if (calendar.timer)
          clearTimeout(calendar.timer);

        calendar.timer = setTimeout(function() {
          options.callback(calendar);
        }, options.callbackDelay);
      }
    }


    fillYears(date);
    fillMonths(date);
    fillDays(date);

    deferredCallBack();

  }

  theDiv.click(function(ev) {
    var el = $(ev.target).closest(".cAlElM");
    if (el.hasClass("cAlElM")) {
      calendar.changeDate(new Date(parseInt(el.attr("millis"))));
    }
	var d = calendar.currentDate;
	options.onSelect.call(this,d);
  });


  //if mousewheel
  if ($.event.special.mousewheel && options.useWheel) {
    divYears.mousewheel(function(event, delta) {
      var d = new Date(calendar.currentDate.getTime());
      d.setFullYear(d.getFullYear() + delta);
      calendar.changeDate(d);
      return false;
    });
    divMonths.mousewheel(function(event, delta) {
      var d = new Date(calendar.currentDate.getTime());
      d.setMonth(d.getMonth() + delta);
      calendar.changeDate(d);
      return false;
    });
    divDays.mousewheel(function(event, delta) {
      var d = new Date(calendar.currentDate.getTime());
      d.setDate(d.getDate() + delta);
      calendar.changeDate(d);
      return false;
    });
  }
  if (options.reYe == true){
      $('.cAlYeR').remove();
  }

  calendar.changeDate(options.date);

  return calendar;
};