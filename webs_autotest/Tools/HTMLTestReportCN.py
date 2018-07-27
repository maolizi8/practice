#coding=utf-8
"""
A TestRunner for use with the Python unit testing framework. It
generates a HTML report to show the result at a glance.

The simplest way to use this is to invoke its main method. E.g.

    import unittest
    import HTMLTestRunner

    ... define your tests ...

    if __name__ == '__main__':
        HTMLTestRunner.main()


For more customization options, instantiates a HTMLTestRunner object.
HTMLTestRunner is a counterpart to unittest's TextTestRunner. E.g.

    # output to a file
    fp = file('my_report.html', 'wb')
    runner = HTMLTestRunner.HTMLTestRunner(
                stream=fp,
                title='My unit test',
                description='This demonstrates the report output by HTMLTestRunner.'
                )

    # Use an external stylesheet.
    # See the Template_mixin class for more customizable options
    runner.STYLESHEET_TMPL = '<link rel="stylesheet" href="my_stylesheet.css" type="text/css">'

    # run the test
    runner.run(my_test_suite)


------------------------------------------------------------------------
Copyright (c) 2004-2007, Wai Yip Tung
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are
met:

* Redistributions of source code must retain the above copyright notice,
  this list of conditions and the following disclaimer.
* Redistributions in binary form must reproduce the above copyright
  notice, this list of conditions and the following disclaimer in the
  documentation and/or other materials provided with the distribution.
* Neither the name Wai Yip Tung nor the names of its contributors may be
  used to endorse or promote products derived from this software without
  specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED
TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER
OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

# URL: http://tungwaiyip.info/software/HTMLTestRunner.html

__author__ = "Wai Yip Tung,  Findyou"
__version__ = "0.8.2.2"

# geqiuli modify
'''图片存放的地址，请自行更改'''
IMG_DIR='E:/mypython/yaowang/imgs/'


"""
Change History
Version 0.8.2.1 -Findyou
* 改为支持python3

Version 0.8.2.1 -Findyou
* 支持中文，汉化
* 调整样式，美化（需要连入网络，使用的百度的Bootstrap.js）
* 增加 通过分类显示、测试人员、通过率的展示
* 优化“详细”与“收起”状态的变换
* 增加返回顶部的锚点

Version 0.8.2
* Show output inline instead of popup window (Viorel Lupu).

Version in 0.8.1
* Validated XHTML (Wolfgang Borgert).
* Added description of test classes and test cases.

Version in 0.8.0
* Define Template_mixin class for customization.
* Workaround a IE 6 bug that it does not treat <script> block as CDATA.

Version in 0.7.1
* Back port to Python 2.3 (Frank Horowitz).
* Fix missing scroll bars in detail log (Podi).
"""

# TODO: color stderr
# TODO: simplify javascript using ,ore than 1 class in the class attribute?

import datetime
import io
import sys
import time
import unittest
from xml.sax import saxutils
import sys

import os
import base64

# ------------------------------------------------------------------------
# The redirectors below are used to capture output during testing. Output
# sent to sys.stdout and sys.stderr are automatically captured. However
# in some cases sys.stdout is already cached before HTMLTestRunner is
# invoked (e.g. calling logging.basicConfig). In order to capture those
# output, use the redirectors for the cached stream.
#
# e.g.
#   >>> logging.basicConfig(stream=HTMLTestRunner.stdout_redirector)
#   >>>

class OutputRedirector(object):
    """ Wrapper to redirect stdout or stderr """
    def __init__(self, fp):
        self.fp = fp

    def write(self, s):
        self.fp.write(s)

    def writelines(self, lines):
        self.fp.writelines(lines)

    def flush(self):
        self.fp.flush()

stdout_redirector = OutputRedirector(sys.stdout)
stderr_redirector = OutputRedirector(sys.stderr)

# ----------------------------------------------------------------------
# Template

class Template_mixin(object):
    """
    Define a HTML template for report customerization and generation.

    Overall structure of an HTML report

    HTML
    +------------------------+
    |<html>                  |
    |  <head>                |
    |                        |
    |   STYLESHEET           |
    |   +----------------+   |
    |   |                |   |
    |   +----------------+   |
    |                        |
    |  </head>               |
    |                        |
    |  <body>                |
    |                        |
    |   HEADING              |
    |   +----------------+   |
    |   |                |   |
    |   +----------------+   |
    |                        |
    |   REPORT               |
    |   +----------------+   |
    |   |                |   |
    |   +----------------+   |
    |                        |
    |   ENDING               |
    |   +----------------+   |
    |   |                |   |
    |   +----------------+   |
    |                        |
    |  </body>               |
    |</html>                 |
    +------------------------+
    """

    STATUS = {
    0: '通过',
    1: '失败',
    2: '错误',
    }

    DEFAULT_TITLE = '单元测试报告'
    DEFAULT_DESCRIPTION = ''
    DEFAULT_TESTER='最棒QA'

    # ------------------------------------------------------------------------
    # HTML Template

    HTML_TMPL = r"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
    <title>%(title)s</title>
    <meta name="generator" content="%(generator)s"/>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>
    <link href="http://libs.baidu.com/bootstrap/3.0.3/css/bootstrap.min.css" rel="stylesheet">
    <script src="http://libs.baidu.com/jquery/2.0.0/jquery.min.js"></script>
    <script src="http://libs.baidu.com/bootstrap/3.0.3/js/bootstrap.min.js"></script>
    %(stylesheet)s
</head>
<body >
<script language="javascript" type="text/javascript">
output_list = Array();

/*level 调整增加只显示通过用例的分类 --Findyou
0:Summary //all hiddenRow
1:Failed  //pt hiddenRow, ft none
2:Pass    //pt none, ft hiddenRow
3:All     //pt none, ft none

*/
function showCase(level) {
    trs = document.getElementsByTagName("tr");
    for (var i = 0; i < trs.length; i++) {
        tr = trs[i];
        id = tr.id;
        if (id.substr(0,2) == 'ft') {
            if (level == 2 || level == 0 ) {
                tr.className = 'hiddenRow';
            }
            else {
                tr.className = '';
            }
        }
        if (id.substr(0,2) == 'pt') {
            
            if (level < 2) {
                tr.className = 'hiddenRow';
            }
            else {
                tr.className = '';
            }
        }
    }

    //加入【详细】切换文字变化 --Findyou
    detail_class=document.getElementsByClassName('detail');
	//console.log(detail_class.length)
	if (level == 3) {
		for (var i = 0; i < detail_class.length; i++){
			detail_class[i].innerHTML="收起"
		}
	}
	else{
			for (var i = 0; i < detail_class.length; i++){
			detail_class[i].innerHTML="详细"
		}
	}
}

function showClassDetail(cid, count) {
    var id_list = Array(count);
    var toHide = 1;
    for (var i = 0; i < count; i++) {
        //ID修改 点 为 下划线 -Findyou
        tid0 = 't' + cid.substr(1) + '_' + (i+1);
        tid = 'f' + tid0;
        tr = document.getElementById(tid);
        if (!tr) {
            tid = 'p' + tid0;
            tr = document.getElementById(tid);
        }
        id_list[i] = tid;
        if (tr.className) {
            toHide = 0;
        }
    }
    for (var i = 0; i < count; i++) {
        tid = id_list[i];
        //修改点击无法收起的BUG，加入【详细】切换文字变化 --Findyou
        if (toHide) {
            document.getElementById(tid).className = 'hiddenRow';
            document.getElementById(cid).innerText = "详细"
        }
        else {
            document.getElementById(tid).className = '';
            document.getElementById(cid).innerText = "收起"
        }
    }
}

function html_escape(s) {
    s = s.replace(/&/g,'&amp;');
    s = s.replace(/</g,'&lt;');
    s = s.replace(/>/g,'&gt;');
    return s;
}
</script>
%(heading)s
%(report)s
%(images_part)s
%(ending)s

</body>
</html>
"""
    # variables: (title, generator, stylesheet, heading, report, ending)


    # ------------------------------------------------------------------------
    # Stylesheet
    #
    # alternatively use a <link> for external style sheet, e.g.
    #   <link rel="stylesheet" href="$url" type="text/css">

    STYLESHEET_TMPL = """
<style type="text/css" media="screen">
body        { font-family: Microsoft YaHei,Tahoma,arial,helvetica,sans-serif;padding: 20px; font-size: 80%; }
table       { font-size: 100%; }

p {margin: 0 0 10px;}
.btn {
    display: inline-block;
    padding: 6px 12px;
    margin-bottom: 0;
    font-size: 14px;
    font-weight: normal;
    line-height: 1.428571429;
    text-align: center;
    white-space: nowrap;
    vertical-align: middle;
    cursor: pointer;
    background-image: none;
    border: 1px solid transparent;
    border-radius: 4px;
    -webkit-user-select: none;
    -moz-user-select: none;
    -ms-user-select: none;
    -o-user-select: none;
    user-select: none
}
.btn:focus {
    outline: thin dotted;
    outline: 5px auto -webkit-focus-ring-color;
    outline-offset: -2px
}
.btn:hover, .btn:focus {
    color: #333;
    text-decoration: none
}
.btn:active, .btn.active {
    background-image: none;
    outline: 0;
    -webkit-box-shadow: inset 0 3px 5px rgba(0, 0, 0, 0.125);
    box-shadow: inset 0 3px 5px rgba(0, 0, 0, 0.125)
}
.btn.disabled, .btn[disabled], fieldset[disabled] .btn {
    pointer-events: none;
    cursor: not-allowed;
    opacity: .65;
    filter: alpha(opacity = 65);
    -webkit-box-shadow: none;
    box-shadow: none
}
.btn-default {
    color: #333;
    background-color: #fff;
    border-color: #ccc
}
.btn-default:hover, .btn-default:focus, .btn-default:active,
    .btn-default.active, .open .dropdown-toggle.btn-default {
    color: #333;
    background-color: #ebebeb;
    border-color: #adadad
}
.btn-default:active, .btn-default.active, .open .dropdown-toggle.btn-default
    {
    background-image: none
}
.btn-default.disabled, .btn-default[disabled], fieldset[disabled] .btn-default,
    .btn-default.disabled:hover, .btn-default[disabled]:hover, fieldset[disabled] .btn-default:hover,
    .btn-default.disabled:focus, .btn-default[disabled]:focus, fieldset[disabled] .btn-default:focus,
    .btn-default.disabled:active, .btn-default[disabled]:active, fieldset[disabled] .btn-default:active,
    .btn-default.disabled.active, .btn-default[disabled].active, fieldset[disabled] .btn-default.active
    {
    background-color: #fff;
    border-color: #ccc
}
.btn-default .badge {
    color: #fff;
    background-color: #fff
}
.btn-primary {
    color: #fff;
    background-color: #428bca;
    border-color: #357ebd
}
.btn-primary:hover, .btn-primary:focus, .btn-primary:active,
    .btn-primary.active, .open .dropdown-toggle.btn-primary {
    color: #fff;
    background-color: #3276b1;
    border-color: #285e8e
}
.btn-primary:active, .btn-primary.active, .open .dropdown-toggle.btn-primary
    {
    background-image: none
}
.btn-primary.disabled, .btn-primary[disabled], fieldset[disabled] .btn-primary,
    .btn-primary.disabled:hover, .btn-primary[disabled]:hover, fieldset[disabled] .btn-primary:hover,
    .btn-primary.disabled:focus, .btn-primary[disabled]:focus, fieldset[disabled] .btn-primary:focus,
    .btn-primary.disabled:active, .btn-primary[disabled]:active, fieldset[disabled] .btn-primary:active,
    .btn-primary.disabled.active, .btn-primary[disabled].active, fieldset[disabled] .btn-primary.active
    {
    background-color: #428bca;
    border-color: #357ebd
}
.btn-primary .badge {
    color: #428bca;
    background-color: #fff
}
.btn-warning {
    color: #fff;
    background-color: #f0ad4e;
    border-color: #eea236
}
.btn-warning:hover, .btn-warning:focus, .btn-warning:active,
    .btn-warning.active, .open .dropdown-toggle.btn-warning {
    color: #fff;
    background-color: #ed9c28;
    border-color: #d58512
}
.btn-warning:active, .btn-warning.active, .open .dropdown-toggle.btn-warning
    {
    background-image: none
}
.btn-warning.disabled, .btn-warning[disabled], fieldset[disabled] .btn-warning,
    .btn-warning.disabled:hover, .btn-warning[disabled]:hover, fieldset[disabled] .btn-warning:hover,
    .btn-warning.disabled:focus, .btn-warning[disabled]:focus, fieldset[disabled] .btn-warning:focus,
    .btn-warning.disabled:active, .btn-warning[disabled]:active, fieldset[disabled] .btn-warning:active,
    .btn-warning.disabled.active, .btn-warning[disabled].active, fieldset[disabled] .btn-warning.active
    {
    background-color: #f0ad4e;
    border-color: #eea236
}
.btn-warning .badge {
    color: #f0ad4e;
    background-color: #fff
}
.btn-danger {
    color: #fff;
    background-color: #d9534f;
    border-color: #d43f3a
}
.btn-danger:hover, .btn-danger:focus, .btn-danger:active, .btn-danger.active,
    .open .dropdown-toggle.btn-danger {
    color: #fff;
    background-color: #d2322d;
    border-color: #ac2925
}
.btn-danger:active, .btn-danger.active, .open .dropdown-toggle.btn-danger
    {
    background-image: none
}
.btn-danger.disabled, .btn-danger[disabled], fieldset[disabled] .btn-danger,
    .btn-danger.disabled:hover, .btn-danger[disabled]:hover, fieldset[disabled] .btn-danger:hover,
    .btn-danger.disabled:focus, .btn-danger[disabled]:focus, fieldset[disabled] .btn-danger:focus,
    .btn-danger.disabled:active, .btn-danger[disabled]:active, fieldset[disabled] .btn-danger:active,
    .btn-danger.disabled.active, .btn-danger[disabled].active, fieldset[disabled] .btn-danger.active
    {
    background-color: #d9534f;
    border-color: #d43f3a
}
.btn-danger .badge {
    color: #d9534f;
    background-color: #fff
}
.btn-success {
    color: #fff;
    background-color: #5cb85c;
    border-color: #4cae4c
}
.btn-success:hover, .btn-success:focus, .btn-success:active,
    .btn-success.active, .open .dropdown-toggle.btn-success {
    color: #fff;
    background-color: #47a447;
    border-color: #398439
}
.btn-success:active, .btn-success.active, .open .dropdown-toggle.btn-success
    {
    background-image: none
}
.btn-success.disabled, .btn-success[disabled], fieldset[disabled] .btn-success,
    .btn-success.disabled:hover, .btn-success[disabled]:hover, fieldset[disabled] .btn-success:hover,
    .btn-success.disabled:focus, .btn-success[disabled]:focus, fieldset[disabled] .btn-success:focus,
    .btn-success.disabled:active, .btn-success[disabled]:active, fieldset[disabled] .btn-success:active,
    .btn-success.disabled.active, .btn-success[disabled].active, fieldset[disabled] .btn-success.active
    {
    background-color: #5cb85c;
    border-color: #4cae4c
}
.btn-success .badge {
    color: #5cb85c;
    background-color: #fff
}
.btn-info {
    color: #fff;
    background-color: #5bc0de;
    border-color: #46b8da
}
.btn-info:hover, .btn-info:focus, .btn-info:active, .btn-info.active,
    .open .dropdown-toggle.btn-info {
    color: #fff;
    background-color: #39b3d7;
    border-color: #269abc
}
.btn-info:active, .btn-info.active, .open .dropdown-toggle.btn-info {
    background-image: none
}
.btn-info.disabled, .btn-info[disabled], fieldset[disabled] .btn-info,
    .btn-info.disabled:hover, .btn-info[disabled]:hover, fieldset[disabled] .btn-info:hover,
    .btn-info.disabled:focus, .btn-info[disabled]:focus, fieldset[disabled] .btn-info:focus,
    .btn-info.disabled:active, .btn-info[disabled]:active, fieldset[disabled] .btn-info:active,
    .btn-info.disabled.active, .btn-info[disabled].active, fieldset[disabled] .btn-info.active
    {
    background-color: #5bc0de;
    border-color: #46b8da
}
.btn-info .badge {
    color: #5bc0de;
    background-color: #fff
}
.btn-link {
    font-weight: normal;
    color: #428bca;
    cursor: pointer;
    border-radius: 0
}
.btn-link, .btn-link:active, .btn-link[disabled], fieldset[disabled] .btn-link
    {
    background-color: transparent;
    -webkit-box-shadow: none;
    box-shadow: none
}
.btn-link, .btn-link:hover, .btn-link:focus, .btn-link:active {
    border-color: transparent
}
.btn-link:hover, .btn-link:focus {
    color: #2a6496;
    text-decoration: underline;
    background-color: transparent
}
.btn-link[disabled]:hover, fieldset[disabled] .btn-link:hover, .btn-link[disabled]:focus,
    fieldset[disabled] .btn-link:focus {
    color: #999;
    text-decoration: none
}
.btn-lg {
    padding: 10px 16px;
    font-size: 18px;
    line-height: 1.33;
    border-radius: 6px
}
.btn-sm {
    padding: 5px 10px;
    font-size: 12px;
    line-height: 1.5;
    border-radius: 3px
}
.btn-xs {
    padding: 1px 5px;
    font-size: 12px;
    line-height: 1.5;
    border-radius: 3px
}
.btn-block {
    display: block;
    width: 100%;
    padding-right: 0;
    padding-left: 0
}
.btn-block+.btn-block {
    margin-top: 5px
}
input[type="submit"].btn-block, input[type="reset"].btn-block, input[type="button"].btn-block
    {
    width: 100%
}
.fade {
    opacity: 0;
    -webkit-transition: opacity .15s linear;
    transition: opacity .15s linear
}
.fade.in {
    opacity: 1
}
.collapse {
    display: none
}
.collapse.in {
    display: block
}
.collapsing {
    position: relative;
    height: 0;
    overflow: hidden;
    -webkit-transition: height .35s ease;
    transition: height .35s ease
}
.text-center {
    text-align: center;
}
a {
    color: #428bca;
    text-decoration: none;
    background: transparent;
}

table {
    font-size: 100%;
    max-width: 100%;
    background-color: transparent;
    border-collapse: collapse;
    border-spacing: 0;
}
table {
    max-width: 100%;
    background-color: transparent
}

th {
    text-align: left
}

.table {
    width: 100%;
    margin-bottom: 20px
}

.table>thead>tr>th, .table>tbody>tr>th, .table>tfoot>tr>th, .table>thead>tr>td,
    .table>tbody>tr>td, .table>tfoot>tr>td {
    padding: 8px;
    line-height: 1.428571429;
    vertical-align: top;
    border-top: 1px solid #ddd
}

.table>thead>tr>th {
    vertical-align: bottom;
    border-bottom: 2px solid #ddd
}

.table>caption+thead>tr:first-child>th, .table>colgroup+thead>tr:first-child>th,
    .table>thead:first-child>tr:first-child>th, .table>caption+thead>tr:first-child>td,
    .table>colgroup+thead>tr:first-child>td, .table>thead:first-child>tr:first-child>td
    {
    border-top: 0
}

.table>tbody+tbody {
    border-top: 2px solid #ddd
}

.table .table {
    background-color: #fff
}

.table-condensed>thead>tr>th, .table-condensed>tbody>tr>th,
    .table-condensed>tfoot>tr>th, .table-condensed>thead>tr>td,
    .table-condensed>tbody>tr>td, .table-condensed>tfoot>tr>td {
    padding: 5px
}

.table-bordered {
    border: 1px solid #ddd
}

.table-bordered>thead>tr>th, .table-bordered>tbody>tr>th,
    .table-bordered>tfoot>tr>th, .table-bordered>thead>tr>td,
    .table-bordered>tbody>tr>td, .table-bordered>tfoot>tr>td {
    border: 1px solid #ddd
}

.table-bordered>thead>tr>th, .table-bordered>thead>tr>td {
    border-bottom-width: 2px
}

.table-striped>tbody>tr:nth-child(odd)>td, .table-striped>tbody>tr:nth-child(odd)>th
    {
    background-color: #f9f9f9
}

.table-hover>tbody>tr:hover>td, .table-hover>tbody>tr:hover>th {
    background-color: #f5f5f5
}

table col[class*="col-"] {
    position: static;
    display: table-column;
    float: none
}

table td[class*="col-"], table th[class*="col-"] {
    display: table-cell;
    float: none
}

.table>thead>tr>.active, .table>tbody>tr>.active, .table>tfoot>tr>.active,
    .table>thead>.active>td, .table>tbody>.active>td, .table>tfoot>.active>td,
    .table>thead>.active>th, .table>tbody>.active>th, .table>tfoot>.active>th
    {
    background-color: #f5f5f5
}

.table-hover>tbody>tr>.active:hover, .table-hover>tbody>.active:hover>td,
    .table-hover>tbody>.active:hover>th {
    background-color: #e8e8e8
}

.table>thead>tr>.success, .table>tbody>tr>.success, .table>tfoot>tr>.success,
    .table>thead>.success>td, .table>tbody>.success>td, .table>tfoot>.success>td,
    .table>thead>.success>th, .table>tbody>.success>th, .table>tfoot>.success>th
    {
    background-color: #dff0d8
}

.table-hover>tbody>tr>.success:hover, .table-hover>tbody>.success:hover>td,
    .table-hover>tbody>.success:hover>th {
    background-color: #d0e9c6
}

.table>thead>tr>.danger, .table>tbody>tr>.danger, .table>tfoot>tr>.danger,
    .table>thead>.danger>td, .table>tbody>.danger>td, .table>tfoot>.danger>td,
    .table>thead>.danger>th, .table>tbody>.danger>th, .table>tfoot>.danger>th
    {
    background-color: #f2dede
}

.table-hover>tbody>tr>.danger:hover, .table-hover>tbody>.danger:hover>td,
    .table-hover>tbody>.danger:hover>th {
    background-color: #ebcccc
}

.table>thead>tr>.warning, .table>tbody>tr>.warning, .table>tfoot>tr>.warning,
    .table>thead>.warning>td, .table>tbody>.warning>td, .table>tfoot>.warning>td,
    .table>thead>.warning>th, .table>tbody>.warning>th, .table>tfoot>.warning>th
    {
    background-color: #fcf8e3
}

.table-hover>tbody>tr>.warning:hover, .table-hover>tbody>.warning:hover>td,
    .table-hover>tbody>.warning:hover>th {
    background-color: #faf2cc
}

@media ( max-width :767px) {
    .table-responsive {
        width: 100%;
        margin-bottom: 15px;
        overflow-x: scroll;
        overflow-y: hidden;
        border: 1px solid #ddd;
        -ms-overflow-style: -ms-autohiding-scrollbar;
        -webkit-overflow-scrolling: touch
    }
    .table-responsive>.table {
        margin-bottom: 0
    }
    .table-responsive>.table>thead>tr>th, .table-responsive>.table>tbody>tr>th,
        .table-responsive>.table>tfoot>tr>th, .table-responsive>.table>thead>tr>td,
        .table-responsive>.table>tbody>tr>td, .table-responsive>.table>tfoot>tr>td
        {
        white-space: nowrap
    }
    .table-responsive>.table-bordered {
        border: 0
    }
    .table-responsive>.table-bordered>thead>tr>th:first-child,
        .table-responsive>.table-bordered>tbody>tr>th:first-child,
        .table-responsive>.table-bordered>tfoot>tr>th:first-child,
        .table-responsive>.table-bordered>thead>tr>td:first-child,
        .table-responsive>.table-bordered>tbody>tr>td:first-child,
        .table-responsive>.table-bordered>tfoot>tr>td:first-child {
        border-left: 0
    }
    .table-responsive>.table-bordered>thead>tr>th:last-child,
        .table-responsive>.table-bordered>tbody>tr>th:last-child,
        .table-responsive>.table-bordered>tfoot>tr>th:last-child,
        .table-responsive>.table-bordered>thead>tr>td:last-child,
        .table-responsive>.table-bordered>tbody>tr>td:last-child,
        .table-responsive>.table-bordered>tfoot>tr>td:last-child {
        border-right: 0
    }
    .table-responsive>.table-bordered>tbody>tr:last-child>th,
        .table-responsive>.table-bordered>tfoot>tr:last-child>th,
        .table-responsive>.table-bordered>tbody>tr:last-child>td,
        .table-responsive>.table-bordered>tfoot>tr:last-child>td {
        border-bottom: 0
    }
}

.collapse.in {
    display: block;
}

.collapse {
    display: none;
}

pre {
    display: block;
    padding: 9.5px;
    margin: 0 0 10px;
    font-size: 13px;
    line-height: 1.428571429;
    color: #333;
    word-break: break-all;
    word-wrap: break-word;
    background-color: #f5f5f5;
    border: 1px solid #ccc;
    border-radius: 4px;
}

code, kbd, pre, samp {
    font-family: Menlo,Monaco,Consolas,"Courier New",monospace;
}

pre {
    white-space: pre-wrap;
}

code, kbd, pre, samp {
    font-family: monospace,serif;
    font-size: 1em;
}

.glyphicon {
    position: relative;
    top: 1px;
    display: inline-block;
    font-family: 'Glyphicons Halflings';
    -webkit-font-smoothing: antialiased;
    font-style: normal;
    font-weight: normal;
    line-height: 1;
    -moz-osx-font-smoothing: grayscale;
}

.imgbox{
    float:left;
    padding:5px;
    margin:5px;
    border:1px solid #eee;
}
.imgs{
    width:237px;
    height:422px; 
    margin:5px;
}
.img_title{
    width:237px;
    font-size:14px;
    line-height:20px;
    text-aligin:center;
    overflow: hidden;
    text-overflow:ellipsis;
    white-space: nowrap;
}

/* -- heading ---------------------------------------------------------------------- */
.heading {
    margin-top: 0ex;
    margin-bottom: 1ex;
}

.heading .description {
    margin-top: 4ex;
    margin-bottom: 6ex;
}

/* -- report ------------------------------------------------------------------------ */
#total_row  { font-weight: bold; }
.passCase   { color: #5cb85c; }
.failCase   { color: #d9534f; font-weight: bold; }
.errorCase  { color: #f0ad4e; font-weight: bold; }
.hiddenRow  { display: none; }
.testcase   { margin-left: 2em; }
</style>

"""

    # ------------------------------------------------------------------------
    # Heading
    #

    HEADING_TMPL = """<div class='heading'>
<h1 style="font-family: Microsoft YaHei">%(title)s</h1>
%(parameters)s
<p class='description'>%(description)s</p>
</div>

""" # variables: (title, parameters, description)

    HEADING_ATTRIBUTE_TMPL = """<p class='attribute'><strong>%(name)s : </strong> %(value)s</p>
""" # variables: (name, value)



    # ------------------------------------------------------------------------
    # Report
    #
    # 汉化,加美化效果 --Findyou
    REPORT_TMPL = """
<p id='show_detail_line'>
<a class="btn btn-primary" href='javascript:showCase(0)'>通过率{ %(passrate)s }</a>
<a class="btn btn-danger" href='javascript:showCase(1)'>失败{ %(fail)s }</a>
<!-- <a class="btn btn-danger" href='javascript:showCase(4)'>错误{ %(error)s }</a> geqiuli add -->
<a class="btn btn-success" href='javascript:showCase(2)'>通过{ %(Pass)s }</a>
<a class="btn btn-info" href='javascript:showCase(3)'>所有{ %(count)s }</a>
</p>
<table id='result_table' class="table table-condensed table-bordered table-hover">
<colgroup>
<col align='left' />
<col align='right' />
<col align='right' />
<col align='right' />
<col align='right' />
<col align='right' />
</colgroup>
<tr id='header_row' class="text-center success" style="font-weight: bold;font-size: 14px;">
    <td>用例集/测试用例</td>
    <td>总计</td>
    <td>通过</td>
    <td>失败</td>
    <!-- <td>错误</td> -->
    <td>详细</td>
</tr>
%(test_list)s
<tr id='total_row' class="text-center active">
    <td>总计</td>
    <td>%(count)s</td>
    <td>%(Pass)s</td>
    <td>%(fail)s</td>
     <!-- <td>%(error)s</td> -->
    <td>通过率：%(passrate)s</td>
</tr>
</table>
""" # variables: (test_list, count, Pass, fail, error ,passrate)

    REPORT_CLASS_TMPL = r"""
<tr class='%(style)s warning'>
    <td>%(desc)s</td>
    <td class="text-center">%(count)s</td>
    <td class="text-center">%(Pass)s</td>
    <td class="text-center">%(fail)s</td>
     <!-- <td class="text-center">%(error)s</td> -->
    <td class="text-center"><a href="javascript:showClassDetail('%(cid)s',%(count)s)" class="detail" id='%(cid)s'>详细</a></td>
</tr>
""" # variables: (style, desc, count, Pass, fail, error, cid)

    #失败 的样式，去掉原来JS效果，美化展示效果  -Findyou
    REPORT_TEST_WITH_OUTPUT_TMPL = r"""
<tr id='%(tid)s' class='%(Class)s'>
    <td class='%(style)s'><div class='testcase'>%(desc)s</div></td>
    
    
    <td colspan='3' align='center'>
    
    <!--默认收起错误信息 -Findyou
    <button id='btn_%(tid)s' type="button"  class="btn btn-danger btn-xs collapsed" data-toggle="collapse" data-target='#div_%(tid)s'>%(status)s</button>
    <div id='div_%(tid)s' class="collapse">  -->

    <!-- 默认展开错误信息 -Findyou -->
    <!--<button id='btn_%(tid)s' type="button"  class="btn btn-danger btn-xs" data-toggle="collapse" data-target='#div_%(tid)s'>%(status)s</button>-->
    <div id='div_%(tid)s' class="collapse in">
    <pre>
    %(script)s
    </pre>
    </div>
    </td>
    
    <!-- geqiuli modify -->
    <td align='center' class='%(style)s'>
        <button id='btn_%(tid)s' type="button"  class="btn btn-default btn-xs %(style)s" data-toggle="collapse" data-target='#div_%(tid)s'>%(status)s</button> 
    </td>
</tr>
""" # variables: (tid, Class, style, desc, status)

    # 通过 的样式，加标签效果  -Findyou
    REPORT_TEST_NO_OUTPUT_TMPL = r"""
<tr id='%(tid)s' class='%(Class)s'>
    <td class='%(style)s'><div class='testcase'>%(desc)s</div></td>
    
    
    <td colspan='3' align='center'>
        <!-- <span class="label label-success success">%(status)s</span> -->
    </td>
    <!-- geqiuli modify -->
    <td align='center' class='%(style)s'>
       <button type="button"  class="btn btn-default btn-xs %(style)s">%(status)s</button> 
    </td>
    
</tr>
""" # variables: (tid, Class, style, desc, status)

    REPORT_TEST_OUTPUT_TMPL = r"""
%(id)s: %(output)s
""" # variables: (id, output)
    
    
    # base64的方式显示所有的图片
    IMAGES_TMPL="""
    
    """
    
    
    
    
    
    # ------------------------------------------------------------------------
    # ENDING
    #
    # 增加返回顶部按钮  --Findyou
    ENDING_TMPL = """<div id='ending'>&nbsp;</div>
    <div style=" position:fixed;right:50px; bottom:30px; width:20px; height:20px;cursor:pointer">
    <a href="#"><span class="glyphicon glyphicon-eject" style = "font-size:30px;" aria-hidden="true">
    </span></a></div>
    """
    
    

# -------------------- The end of the Template class -------------------


TestResult = unittest.TestResult

class _TestResult(TestResult):
    # note: _TestResult is a pure representation of results.
    # It lacks the output and reporting ability compares to unittest._TextTestResult.

    def __init__(self, verbosity=1):
        TestResult.__init__(self)
        self.stdout0 = None
        self.stderr0 = None
        self.success_count = 0
        self.failure_count = 0
        self.error_count = 0
        self.verbosity = verbosity

        # result is a list of result in 4 tuple
        # (
        #   result code (0: success; 1: fail; 2: error),
        #   TestCase object,
        #   Test output (byte string),
        #   stack trace,
        # )
        self.result = []
        #增加一个测试通过率 --Findyou
        self.passrate=float(0)


    def startTest(self, test):
        TestResult.startTest(self, test)
        # just one buffer for both stdout and stderr
        self.outputBuffer = io.StringIO()
        stdout_redirector.fp = self.outputBuffer
        stderr_redirector.fp = self.outputBuffer
        self.stdout0 = sys.stdout
        self.stderr0 = sys.stderr
        sys.stdout = stdout_redirector
        sys.stderr = stderr_redirector


    def complete_output(self):
        """
        Disconnect output redirection and return buffer.
        Safe to call multiple times.
        """
        if self.stdout0:
            sys.stdout = self.stdout0
            sys.stderr = self.stderr0
            self.stdout0 = None
            self.stderr0 = None
        return self.outputBuffer.getvalue()


    def stopTest(self, test):
        # Usually one of addSuccess, addError or addFailure would have been called.
        # But there are some path in unittest that would bypass this.
        # We must disconnect stdout in stopTest(), which is guaranteed to be called.
        self.complete_output()


    def addSuccess(self, test):
        self.success_count += 1
        TestResult.addSuccess(self, test)
        output = self.complete_output()
        self.result.append((0, test, output, ''))
        if self.verbosity > 1:
            sys.stderr.write('ok ')
            sys.stderr.write(str(test))
            sys.stderr.write('\n')
        else:
            sys.stderr.write('.')

    def addError(self, test, err):
        self.error_count += 1
        # geqiuli modify start
        self.failure_count += 1
        # geqiuli modify end
        TestResult.addError(self, test, err)
        _, _exc_str = self.errors[-1]
        output = self.complete_output()
        self.result.append((2, test, output, _exc_str))
        if self.verbosity > 1:
            sys.stderr.write('E  ')
            sys.stderr.write(str(test))
            sys.stderr.write('\n')
        else:
            sys.stderr.write('E')

    def addFailure(self, test, err):
        self.failure_count += 1
        TestResult.addFailure(self, test, err)
        _, _exc_str = self.failures[-1]
        output = self.complete_output()
        self.result.append((1, test, output, _exc_str))
        if self.verbosity > 1:
            sys.stderr.write('F  ')
            sys.stderr.write(str(test))
            sys.stderr.write('\n')
        else:
            sys.stderr.write('F')


class HTMLTestRunner(Template_mixin):
    """
    """
    def __init__(self, stream=sys.stdout, verbosity=1,title=None,description=None,tester=None):
        self.stream = stream
        self.verbosity = verbosity
        if title is None:
            self.title = self.DEFAULT_TITLE
        else:
            self.title = title
        if description is None:
            self.description = self.DEFAULT_DESCRIPTION
        else:
            self.description = description
        if tester is None:
            self.tester = self.DEFAULT_TESTER
        else:
            self.tester = tester

        self.startTime = datetime.datetime.now()


    def run(self, test):
        "Run the given test case or test suite."
        result = _TestResult(self.verbosity)
        test(result)
        self.stopTime = datetime.datetime.now()
        self.generateReport(test, result)
        
        #geqiuli modify
        
        
        print('\nTime Elapsed: %s' % (self.stopTime-self.startTime), file=sys.stderr)
        return result


    def sortResult(self, result_list):
        # unittest does not seems to run in any particular order.
        # Here at least we want to group them together by class.
        rmap = {}
        classes = []
        for n,t,o,e in result_list:
            cls = t.__class__
            if cls not in rmap:
                rmap[cls] = []
                classes.append(cls)
            rmap[cls].append((n,t,o,e))
        r = [(cls, rmap[cls]) for cls in classes]
        return r

    #替换测试结果status为通过率 --Findyou
    def getReportAttributes(self, result):
        """
        Return report attributes as a list of (name, value).
        Override this to add custom attributes.
        """
        startTime = str(self.startTime)[:19]
        duration = str(self.stopTime - self.startTime)
        status = []
        
        # geqiuli modify
        #status.append('共 %s' % (result.success_count + result.failure_count + result.error_count))
        status.append('共 %s' % (result.success_count + result.failure_count))
        
        if result.success_count: status.append('通过 %s'    % result.success_count)
        if result.failure_count: status.append('失败 %s' % result.failure_count)
        if result.error_count:   status.append('错误 %s'   % result.error_count  )
        if status:
            status = '，'.join(status)
            # geqiuli modify
            #self.passrate = str("%.2f%%" % (float(result.success_count) / float(result.success_count + result.failure_count + result.error_count) * 100))
            self.passrate = str("%.2f%%" % (float(result.success_count) / float(result.success_count + result.failure_count) * 100))
            
        else:
            status = 'none'
        return [
            ('测试人员', self.tester),
            ('开始时间',startTime),
            ('合计耗时',duration),
            ('测试结果',status + "，通过率= "+self.passrate),
        ]


    def generateReport(self, test, result):
        report_attrs = self.getReportAttributes(result)
        generator = 'HTMLTestRunner %s' % __version__
        stylesheet = self._generate_stylesheet()
        heading = self._generate_heading(report_attrs)
        report = self._generate_report(result)
        ending = self._generate_ending()
        
        #geqiuli modify
        images_part=self.generate_imags_display()
        
        output = self.HTML_TMPL % dict(
            title = saxutils.escape(self.title),
            generator = generator,
            stylesheet = stylesheet,
            heading = heading,
            report = report,
            #geqiuli modify
            images_part=images_part,
            ending = ending,
        )
        self.stream.write(output.encode('utf8'))


    def _generate_stylesheet(self):
        return self.STYLESHEET_TMPL

    #增加Tester显示 -Findyou
    def _generate_heading(self, report_attrs):
        a_lines = []
        for name, value in report_attrs:
            line = self.HEADING_ATTRIBUTE_TMPL % dict(
                    name = saxutils.escape(name),
                    value = saxutils.escape(value),
                )
            a_lines.append(line)
        heading = self.HEADING_TMPL % dict(
            title = saxutils.escape(self.title),
            parameters = ''.join(a_lines),
            description = saxutils.escape(self.description),
            tester= saxutils.escape(self.tester),
        )
        return heading

    #生成报告  --Findyou添加注释
    def _generate_report(self, result):
        rows = []
        sortedResult = self.sortResult(result.result)
        for cid, (cls, cls_results) in enumerate(sortedResult):
            # subtotal for a class
            np = nf = ne = 0
            
            # geqiuli comments: n-status? np-pass_subtotal? nf-fail_subtotal? ne-error_subtotal
            for n,t,o,e in cls_results:
                #geqiuli modify
                #if n == 0: np += 1
                #elif n == 1: nf += 1
                #else: ne += 1
                if n == 0: np += 1
                else: nf += 1

            # format class description
            if cls.__module__ == "__main__":
                name = cls.__name__
            else:
                name = "%s.%s" % (cls.__module__, cls.__name__)
            doc = cls.__doc__ and cls.__doc__.split("\n")[0] or ""
            desc = doc and '%s: %s' % (name, doc) or name

            row = self.REPORT_CLASS_TMPL % dict(
                style = ne > 0 and 'errorClass' or nf > 0 and 'failClass' or 'passClass',
                desc = desc,
                #geqiuli modify
                #count = np+nf+ne,
                count = np+nf,
                
                Pass = np,
                fail = nf,
                error = ne,
                cid = 'c%s' % (cid+1),
            )
            rows.append(row)

            for tid, (n,t,o,e) in enumerate(cls_results):
                self._generate_report_test(rows, cid, tid, n, t, o, e)

        report = self.REPORT_TMPL % dict(
            test_list = ''.join(rows),
            # geqiuli modify
            #count = str(result.success_count+result.failure_count+result.error_count),
            count = str(result.success_count+result.failure_count),
            Pass = str(result.success_count),
            fail = str(result.failure_count),
            error = str(result.error_count),
            passrate =self.passrate,
        )
        return report


    def _generate_report_test(self, rows, cid, tid, n, t, o, e):
        # e.g. 'pt1.1', 'ft1.1', etc
        
        #print('o--',o)
        #print('e--',e)
        
        has_output = bool(o or e)
        # ID修改点为下划线,支持Bootstrap折叠展开特效 - Findyou
        tid = (n == 0 and 'p' or 'f') + 't%s_%s' % (cid+1,tid+1)
        name = t.id().split('.')[-1]
        doc = t.shortDescription() or ""
        desc = doc and ('%s: %s' % (name, doc)) or name
        
        #geqiuli modify (tid, Class, style, desc, status)
        #tmpl = has_output and self.REPORT_TEST_WITH_OUTPUT_TMPL or self.REPORT_TEST_NO_OUTPUT_TMPL
        #print('has_output:',has_output)
        if has_output:
            tmpl=self.REPORT_TEST_WITH_OUTPUT_TMPL
        else:
            tmpl=self.REPORT_TEST_NO_OUTPUT_TMPL

        # utf-8 支持中文 - Findyou
         # o and e should be byte string because they are collected from stdout and stderr?
        if isinstance(o, str):
            # TODO: some problem with 'string_escape': it escape \n and mess up formating
            # uo = unicode(o.encode('string_escape'))
            # uo = o.decode('latin-1')
            uo = o
        else:
            uo = o
        if isinstance(e, str):
            # TODO: some problem with 'string_escape': it escape \n and mess up formating
            # ue = unicode(e.encode('string_escape'))
            # ue = e.decode('latin-1')
            ue = e
        else:
            ue = e

        script = self.REPORT_TEST_OUTPUT_TMPL % dict(
            id = tid,
            output = saxutils.escape(uo+ue),
        )

        row = tmpl % dict(
            tid = tid,
            Class = (n == 0 and 'hiddenRow' or 'none'),
            style = n == 2 and 'errorCase' or (n == 1 and 'failCase' or 'passCase'),
            desc = desc,
            script = script,
            status = self.STATUS[n],
        )
        rows.append(row)
        if not has_output:
            return

    def _generate_ending(self):
        return self.ENDING_TMPL

    def generate_imags_display(self):
        ''''''
        lists_all = os.listdir(IMG_DIR)
        list_file=[]
        for f in lists_all:
            if os.path.isfile(IMG_DIR+f):
                list_file.append(f)
        list_file.sort(key=lambda fn:os.path.getmtime(IMG_DIR+fn))
        
        images_html=''
        for ff in list_file:
            if ff.endswith('.png'):
                with open(IMG_DIR+ff,'rb') as fr:
                    img_byte=base64.b64encode(fr.read())
                    img='''
                    <div>
                    <div class="imgbox">
                    <div class="img_title">{}</div>
                    <img src="data:image/png;base64,{}" class="imgs" />
                    </div>
                    </div>
                    '''.format(ff[:-4],str(img_byte).replace("b'",'')[:-1])
                    images_html+=img
                
        return images_html
        
##############################################################################
# Facilities for running tests from the command line
##############################################################################

# Note: Reuse unittest.TestProgram to launch test. In the future we may
# build our own launcher to support more specific command line
# parameters like test title, CSS, etc.
class TestProgram(unittest.TestProgram):
    """
    A variation of the unittest.TestProgram. Please refer to the base
    class for command line parameters.
    """
    def runTests(self):
        # Pick HTMLTestRunner as the default test runner.
        # base class's testRunner parameter is not useful because it means
        # we have to instantiate HTMLTestRunner before we know self.verbosity.
        if self.testRunner is None:
            self.testRunner = HTMLTestRunner(verbosity=self.verbosity)
        unittest.TestProgram.runTests(self)

main = TestProgram

##############################################################################
# Executing this module from the command line
##############################################################################

if __name__ == "__main__":
    main(module=None)
