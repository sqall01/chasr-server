var TinyPicker = require('../../index');
var JSDOM = require('jsdom').JSDOM;
var dom = new JSDOM('<!DOCTYPE html><input id="jokes" type="text" class="jokes" name="jokes" placeholder="Enter your joke term">', { pretendToBeVisual: true });
global.window = dom.window;
global.document = dom.window.document;
global.HTMLElement = dom.window.HTMLElement;
global.XMLHttpRequest = require('xmlhttprequest').XMLHttpRequest;

describe('TinyPicker', function () {
    function setUpTinyPicker() {
        new TinyPicker({
            firstBox: global.document.getElementById('jokes'),
            startDate: new Date('03/20/2020'),
            months: 2,
            days: ['Su', 'Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa'],
            local: 'en-US',
            allowPast: true,
            success: function (s, e){ alert(s + ' ' + e); }
        }).init();
    }
    it('Need to write tests', function () {
        setUpTinyPicker();

        expect(true).toBe(true);
    });
});
