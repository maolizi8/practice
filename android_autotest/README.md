# python+appium+pytest 安卓app自动化测试

### 1.开启webview调试

获取Webview的context需要开发app的工程师在代码中添加开启webview调试的代码：

if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.KITKAT) {
    WebView.setWebContentsDebuggingEnabled(true);
}

### 2. Android版本4.4+
