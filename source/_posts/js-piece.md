---
title: Javascript detail record
date: 2017-07-09 10:22:44
categories: javascript
tags: [javascript-piece，html]
description: 记录javascript的注意点。

---

#Web的集成开发环境:
1. [jsfiddle](https://jsfiddle.net/)
2. [Thimble](https://thimble.webmaker.org/)
3. [jsbin](http://jsbin.com/)
---
# BugFix

1. `<script>`元素要放所有的标签的后面，也就是最后。
今天的一个bug问题就出现在这里
```javascirpt
var myButton = document.querySelector('button');
var myHeading = document.querySelector('h1');

function setUserName() {
    var myName = prompt('Please enter your name.');
    localStorage.setItem('name', myName);
    myHeading.innerHTML = 'Mozilla is cool, ' + myName;
}

if(!localStorage.getItem('name')) {
    setUserName();
} else {
    var storedName = localStorage.getItem('name');
    myHeading.innerHTML = 'Mozilla is cool, ' + storedName;
}

myButton.onclick = function() {
    setUserName();
}
```
html里面是
```
	...
    <script src="scripts/main.js"></script>
    <button>Change user</button>
	...
```
在页面中点击change user的按钮一直没有反应，打开console看到报错原因是
```
Uncaught TypeError: Cannot set property 'onclick' of null
    at main.js:45
```
`null`说明`myButton`是空的，没有读取到，然后在html中将`<button>``<scirpt>`标签调换一下就可以了。

> `<script>`元素放在 HTML 文件底部的原因是，浏览器解析 HTML 似乎按照代码出现的顺序来的。如果 JavaScript被首先读取，它也应该影响下面的 HTML，但有时会出现问题，因为 JavaScript 会在 HTML 之前被加载，如果 JavaScript 代码出现问题则 HTML 不会被加载。所以将 JavaScript 代码放在底部是最好的选择。

