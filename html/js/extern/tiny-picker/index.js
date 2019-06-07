/*
 *
 * TODO:
 * Dynamically add CSS
 *
 *
 */

// helper functions to minimize file size - can move out of TinyPicker

function createElementWithClass(type, className) {
    var el = document.createElement(type);
    el.className = className || '';
    return el;
}

function appendChild(parent, child) {
    parent.appendChild(child);
}

function getFirstElementByClass(className) {
    return document.getElementsByClassName(className)[0];
}

function newDateInstance(val) {
    return val ? new Date(val) : new Date();
}

function addClass(el, className) {
    el.classList.add(className);
}

function getTime(date) {
    return date.getTime();
}

function getNumberOfWeeks(date) {
    return Math.ceil((date.getDate() - 1 - date.getDay()) / 7);
}

function removeCalendar(className) {
    var element = getFirstElementByClass(className);
    element && document.body.removeChild(element);
}

function isDateTodayOrFuture(currentDate, checkThisDate) {
    return currentDate && checkThisDate && getTime(currentDate) >= getTime(checkThisDate);
}

function positionCalendar(calendarElement, shadowElement) {
    var positions = shadowElement.getBoundingClientRect();
    calendarElement.style.top  =  positions.top + positions.height + (window.pageYOffset || document.documentElement.scrollTop) + 15 + 'px';
    calendarElement.style.left = positions.left + 'px';
}

function writeCSSToHead() {
    var styleEl = document.createElement('style');
    styleEl.innerHTML = '.dHd,.day{float:left;text-align:center}.dHd,.day,.hed{text-align:center}.cal,.cal:after,.cal:before,.lChev,.rChev{position:absolute}.cal{background:#fff;border:1px solid #ccc;z-index:1;padding:0;font-size:10px;border-radius:4px;box-shadow:0 6px 12px rgba(0,0,0,.175);color:#000;font-family:Arial,Helvetica,sans-serif}.cal:before{top:-7px;left:9px;display:inline-block;border-right:7px solid transparent;border-bottom:7px solid #ccc;border-left:7px solid transparent;border-bottom-color:rgba(0,0,0,.2);content:\'\'}.cal:after,.lChev:before,.rChev:before{content:"";display:inline-block}.cal:after{top:-6px;left:10px;border-right:6px solid transparent;border-bottom:6px solid #fff;border-left:6px solid transparent}.hed{font-size:15px;font-weight:500;margin:15px 0 5px}.inBtw{background-color:#bbddf5}.nav{margin:0}.dHd{width:29.5px;color:#bbb;height:30px;line-height:30px;font-size:12px}.mnt{max-width:210px;width:auto;height:auto;display:inline-block;padding:0 10px 10px}.day{border:none;width:28px;height:28px;line-height:28px;color:#555;cursor:pointer;border-right:1.5px solid #fff;border-bottom:1.5px solid #fff;font-size:14px}.sel:not(.disb){background-color:#50a5e6}.disb{opacity:.7;color:#888;cursor:default}.lChev:before,.rChev:before{border-style:solid;border-width:3px 3px 0 0;height:7px;width:7px;cursor:pointer}.rChev:before{transform:rotate(45deg)}.lChev:before{transform:rotate(-135deg)}.lChev,.rChev{top:18px}.rChev{right:25px}.lChev{left:20px}';
    document.head.appendChild(styleEl);
}

function getDays(passedInDate, date, i, local) {
    var month = {
        name: date.toLocaleString(local, { month: 'long'}),
        year: date.getFullYear(),
        weeks: []
    };
    var newDate = new Date(passedInDate.getFullYear(), passedInDate.getMonth() + i, 1).getMonth();
    while (date.getMonth() === newDate) {
        var week = getNumberOfWeeks(newDateInstance(date));
        if (typeof month.weeks[week] === 'undefined') {
            month.weeks[week] = {};
        }

        var day = newDateInstance(date);
        month.weeks[week][day.getDay()] = {
            date: day
        };
        date.setDate(date.getDate() + 1);
    }
    return month;
}

function getMonthsInfoForCalendar(passedInDate, monthsToShow, local) {
    var monthsArr = [];
    var year = passedInDate.getFullYear();
    var monthNum = passedInDate.getMonth();
    for (var i = 0; i < monthsToShow; i++) {
        var date = new Date(year, monthNum + i, 1); // Get first day of the month
        var month = getDays(passedInDate, date, i, local); // Get the days that go in the month
        monthsArr.push(month);
    }

    return monthsArr;
}

function TinyPicker(overrides) { // eslint-disable-line no-unused-vars
    var firstBox = overrides.firstBox;
    var lastBox = overrides.lastBox || {};
    var settings = {
        local: overrides.local || 'en-US',
        selectPast: overrides.allowPast || false,
        months: window.innerWidth > 500 ? overrides.months || 2 : 1,
        days: overrides.days || ['S', 'M', 'T', 'W', 'T', 'F', 'S'],
        success: overrides.success || function () {},
        err: overrides.err || function () {}
    };
    var initialDateSet = true;
    setDateInEl(overrides.startDate, firstBox, initialDateSet);
    setDateInEl(overrides.endDate, lastBox, initialDateSet);
    // Settings and constants
    var today = newDateInstance(newDateInstance().setHours(0, 0, 0, 0));
    var wroteCss = false;
    var calendarClassName = 'cal';
    var div = 'div';
    var selectedString = 'sel';
    var selectedRangeString = 'inBtw';
    var startDate = overrides.startDate;
    startDate = firstBox.value === '' ? today : newDateInstance(startDate && startDate.setHours(0, 0, 0, 0) || '');
    var endDate = overrides.endDate;
    endDate = newDateInstance(endDate && endDate.setHours(0, 0, 0, 0) || '');

    function showCalendar(element, newStartDate) {
        if (!newStartDate) {
            newStartDate = element === firstBox ? startDate : new Date(endDate.getFullYear(), endDate.getMonth());
        }

        newStartDate = isDateTodayOrFuture(newStartDate, today) || settings.selectPast ? newStartDate : today;
        renderCalendar(element, newStartDate);
        positionCalendar(getFirstElementByClass(calendarClassName), element);

        // Close the calendar listener
        ['click', 'touchend'].forEach(function (event) {
            document.addEventListener(event, function (e) {
                var el = e.target;
                var calendarEl = getFirstElementByClass(calendarClassName);
                if (calendarEl && !calendarEl.contains(getFirstElementByClass(el.className)) && el !== document.activeElement) {
                    removeCalendar(calendarClassName);
                }
            });
        });
    }

    function renderCalendar(element, newDate) {
        removeCalendar(calendarClassName);

        var calendarObj = getMonthsInfoForCalendar(newDate, settings.months, settings.local);
        var sinceDate = element !== firstBox && isDateTodayOrFuture(startDate, today) ? startDate : today;

        var calendarWidget = createElementWithClass(div, calendarClassName);
        appendChild(calendarWidget, getChevrons(element, calendarObj));
        appendChild(document.body, calendarWidget);

        calendarObj.forEach(function (month) {
            var monthDiv = createElementWithClass(div, 'mnt');

            var monthHeader = createElementWithClass('p', 'hed');
            monthHeader.innerHTML = month.name + ' ' + month.year;
            appendChild(monthDiv, monthHeader);

            var calendarContainer = createElementWithClass(div);

            settings.days.forEach(function (day) {
                var dayEl = createElementWithClass(div, 'dHd');
                dayEl.innerHTML = day;
                appendChild(calendarContainer, dayEl);
            });

            appendChild(calendarContainer, createCalInnerWorkings(month.weeks, sinceDate, element));
            appendChild(monthDiv, calendarContainer);
            appendChild(calendarWidget, monthDiv);
        });
    }

    function handleCalendarState(shadowElement, date) {
        if (shadowElement === firstBox) {
            startDate = date;
            endDate = startDate;
            if (lastBox.nodeType) {
                lastBox.value = ''; // If user reenters startDate, force reselect of enddate
                lastBox.focus();
            } else {
                removeCalendar(calendarClassName);
                settings.success(startDate);
            }
        } else {
            endDate = date;
            removeCalendar(calendarClassName);
            shadowElement.classList.remove('err');
            settings.success(startDate, endDate);
        }
    }

    function getChevrons(element, calendarObj) {
        var navWrapper = createElementWithClass(div, 'nav');

        appendChild(navWrapper, createElementWithClass('span', 'rChev'));
        appendChild(navWrapper, createElementWithClass('span', 'lChev'));

        navWrapper.addEventListener('click', function (e) {
            var monthChange = e.target.className === 'rChev' ? 1 : -1;
            var firstWeek = calendarObj[0].weeks[0];
            var date = firstWeek[Object.keys(firstWeek)[0]].date;
            var newStartDate = newDateInstance(date.setMonth(date.getMonth() + monthChange));

            showCalendar(element, newStartDate);
        });
        return navWrapper;
    }

    function createCalInnerWorkings(weeks, sinceDate, element) {
        var calendarBody = createElementWithClass(div);

        weeks.forEach(function (week) {
            for (var i = 0; i < 7; i++) {
                var currentDate = week[i] && week[i].date;
                var dayOfWeekEl = createElementWithClass(div, 'day');

                if (typeof currentDate === 'undefined') {
                    appendChild(calendarBody, dayOfWeekEl);
                } else {
                    dayOfWeekEl.className = 'disb';
                    var currentTime = getTime(currentDate);
                    if ((currentDate >= today && element === firstBox) || currentDate >= startDate || settings.selectPast) {
                        dayOfWeekEl.className =  'active';
                        dayOfWeekEl.addEventListener('click', setDateInEl.bind(this, currentDate, element, false));

                        // Add Highlights to days
                        if (endDate > currentDate && startDate < currentDate) {
                            addClass(dayOfWeekEl, selectedRangeString);
                        } else if (getTime(endDate) === currentTime || currentTime ===  getTime(startDate)) {
                            addClass(dayOfWeekEl, selectedString);
                        }
                    }

                    dayOfWeekEl.innerHTML = currentDate.getDate();
                    dayOfWeekEl.classList.add('day');
                    dayOfWeekEl.setAttribute('time', currentTime);
                    appendChild(calendarBody, dayOfWeekEl);
                    hoverRange(dayOfWeekEl, element);
                }
            }
        });

        return calendarBody;
    }

    function hoverRange(el, inputClicked) {
        el.addEventListener('mouseover', function (e) {
            var days = document.getElementsByClassName('day');
            var hoverTime = parseInt(e.target.getAttribute('time'), 10);
            var startTime = getTime(startDate);

            for (var i = 0; i < days.length; i++) {
                var day = days[i];
                var elTime = parseInt(day.getAttribute('time'), 10);

                day.classList.remove(selectedString);
                day.classList.remove(selectedRangeString);
                if (inputClicked === lastBox && elTime < hoverTime && elTime > startTime) {
                    addClass(day, selectedRangeString);
                } else if (hoverTime === elTime || (elTime === startTime && inputClicked !== firstBox)) {
                    addClass(day, selectedString);
                }
            }
        });
    }

    // Specific helpers for TinyPicker

    function setDateInEl(date, shadowElement, initial) {
        initial = initial || false;
        if (date instanceof Date && shadowElement instanceof HTMLElement) {
            shadowElement.value = date.toLocaleDateString(settings.local);
            shadowElement.setAttribute('date', getTime(date));
        }
        if (!initial) {
            handleCalendarState(shadowElement, date);
        }
    }

    function userInputedDateHandler(element) {
        var val = element.value;
        var userInputedDate = val && newDateInstance(val);
        var instanceOfDate = userInputedDate instanceof Date;

        if (instanceOfDate || (instanceOfDate && !isDateTodayOrFuture(userInputedDate, startDate))) {
            element.value = '';
            settings.err();
        }
        isDateTodayOrFuture(userInputedDate, today) && setDateInEl(userInputedDate, element, false);
    }

    // Init listeners to properly display calendar
    this.init = function () {
        [firstBox, lastBox].forEach(function (element) {
            if (!element.nodeType) return;
            element.addEventListener('focus', function (e) {
                !wroteCss && writeCSSToHead();
                wroteCss = true;
                showCalendar(e.target);
            });
            // TODO: Should this be here??? I can do this somewhere else
            var timer;
            element.addEventListener('keydown', function (e) {
                clearTimeout(timer);
                timer = setTimeout(function () {
                    userInputedDateHandler(e.target);
                }, 1000);
            });

            // Stop if you click on input
            element.addEventListener('click', function (e) {
                e.stopPropagation();
            });
        });
    };
}

//module.exports = TinyPicker;
