# tiny-picker
[![NPM](https://nodei.co/npm/tiny-picker.png)](https://nodei.co/npm/tiny-picker/)

[![NPM version](https://img.shields.io/npm/v/tiny-picker.svg?style=flat-square)](https://www.npmjs.com/package/tiny-picker)
[![dependencies](https://david-dm.org/raymondborkowski/tiny-picker.svg)](https://david-dm.org/raymondborkowski/tiny-picker)
[![Build](https://travis-ci.org/raymondborkowski/tiny-picker.svg?branch=master)](https://travis-ci.org/raymondborkowski/tiny-picker)
[![codecov.io](https://codecov.io/github/raymondborkowski/tiny-picker/coverage.svg?branch=master)](https://codecov.io/github/raymondborkowski/tiny-picker?branch=master)
[![gitter](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/tiny-picker?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)
[![devDependencies](https://david-dm.org/raymondborkowski/tiny-picker/dev-status.svg)](https://david-dm.org/raymondborkowski/tiny-picker#info=devDependencies)
[![FOSSA Status](https://app.fossa.io/api/projects/git%2Bgithub.com%2Fraymondborkowski%2Ftiny-picker.svg?type=shield)](https://app.fossa.io/projects/git%2Bgithub.com%2Fraymondborkowski%2Ftiny-picker?ref=badge_shield)
[![downloads](https://img.shields.io/npm/dt/tiny-picker.svg)](https://img.shields.io/npm/dt/tiny-picker.svg)

*Ultra light weight date picker. There are no external dependencies involved. We mimic jQuery UI Datepicker without the bloat*<br><br>
[View Demo](https://raymondborkowski.github.io/tiny-picker/index.html)<br><br>
![](https://raw.githubusercontent.com/raymondborkowski/tiny-picker/master/docs/example.png)
## Install

` npm install tiny-picker --save`

## Use

Bind to input:

```html
<input type="text" id="startDate" />
<input type="text" id="endDate" />
```

In Javascript:<br>
```js
new TinyPicker({
        firstBox:document.getElementById('startDate'),
        lastBox: document.getElementById('endDate'),
}).init();
```

#### Options:
*TinyPicker also takes in options as seen below*
```js
new TinyPicker({
        firstBox:document.getElementById('startDate'), // Required -- Overrides us finding the first input box
        lastBox: document.getElementById('endDate'), // Required -- Overrides us finding the last input box
        startDate: new Date(), // Needs to be a valid instance of Date
        endDate: new Date(), // Needs to be a valid instance of Date
        allowPast: true, // If you want the user to be able to select past dates
        monthsToShow: 2, // How many months to display
        days: ['Su','Mo','Tu','We','Th','Fr','Sa'], // Override for day abbreviations in the calendar
        local: 'es-US', // Specifiy the language and date format. < IE 10 defaults to en-US,
        success: function(startDate, endDate){} // callback function when user inputs dates,
        err: function(){} // callback fired when err state
});
```

#### Color/Style Customizations

Currently using standard jQuery colorizations. Just create overriding styles in your own CSS files to change. Classes are currently not specific so overriding should be a breeze!

## Benchmarking Size (`npm package-size`):
|Date Range Packages  | minified  |  Gzipped |
| ------------- | ------------- | ------------- |
| tiny-picker  | 3.31kB |1.43kB
| tiny-picker + css  | 4.9kB |2.27kB
| Pikaday  |247kB|70.6kB|
| jquery-date-range-picker |367kB|110kB|
| moment  |232kB|65.1kB|
| air-datepicker  |35.3kB|9.45kB|
| tiny-date-picker  |9.8kB|3.42kB|
|tiny-date-picker + css |13.3kB|4.6kB|

## Developing and contributing to tiny-picker
### Folder structure
The main body of code is in `index.js`

The tests are in the `spec/unit` directory. Please follow naming convention with `xxxx.spec.js`

### Running tests

We use [Jasmine](https://jasmine.github.io/api/3.0/global) The existing tests are in the spec folder.

Please write tests for new additions. We use codecov to test for complete unit test coverage.

#### Run all the tests:

`npm test`

### Before submitting a pull request

Please make sure all code supports all versions of node. We write code in ES5 syntax for smaller size and browser compatibility.

We use ESLint for syntax consistency, and the linting rules are included in this repository. Running `npm test` will check the linting rules as well. Please make sure your code has no linting errors before submitting a pull request.

`npm run lint_fix` will also automatically fix any linting errors.

## License

[MIT](https://github.com/raymondborkowski/tiny-picker/blob/master/LICENSE.md)


[![FOSSA Status](https://app.fossa.io/api/projects/git%2Bgithub.com%2Fraymondborkowski%2Ftiny-picker.svg?type=large)](https://app.fossa.io/projects/git%2Bgithub.com%2Fraymondborkowski%2Ftiny-picker?ref=badge_large)