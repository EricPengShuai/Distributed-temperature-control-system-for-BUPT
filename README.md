# Distributed-temperature-control-system-for-BUPT
[大三软工作业--前端Vue--后端python_flask](https://github.com/pengshuai98/Distributed-temperature-control-system-for-BUPT)

# 工程说明文件

## 运行方式

安装完依赖后，运行工程文件夹下的`run.sh`即可运行。![截屏2020-06-1422.51.26](README.assets/截屏2020-06-1422.51.26.png)

随后点击其中一个URL即可访问本分布式空调管理系统的界面

## 数据库建库脚本文件

`mysqlTable.py`已集成到代码中。

![截屏2020-06-1422.52.23](README.assets/截屏2020-06-1422.52.23.png)

## 依赖

### 后端依赖

需要使用`pip3`安装以下包。

```
PyMySQL==0.9.3
Flask_Cors==3.0.8
Flask==1.1.2
Flask_SocketIO==4.3.0
```

### 前端依赖

在`front_end`目录下运行命令`npm install`即可运行。
```
{
  "name": "project", 
  "version": "0.1.0", 
  "private": true, 
  "scripts": { 
    "serve": "vue-cli-service serve", 
    "build": "vue-cli-service build", 
    "lint": "vue-cli-service lint" 
  }, 
  "dependencies": {
    "axios": "^0.19.2", 
    "bootstrap": "^4.5.0", 
    "bootstrap-vue": "^2.14.0", 
    "core-js": "^3.6.4", 
    "json2csv": "^5.0.1", 
    "popper.js": "^1.16.1", 
    "socket.io": "^2.3.0", 
    "socket.io-client": "^2.3.0", 
    "vue": "^2.6.11", 
    "vue-router": "^3.1.6", 
    "vue-socket.io": "^3.0.9", 
    "vue-socket.io-extended": "^4.0.3", 
    "vuex": "^3.4.0", 
    "vuex-persist": "^2.2.0" 
  }, 
  "devDependencies": { 
    "@vue/cli-plugin-babel": "~4.3.0", 
    "@vue/cli-plugin-eslint": "~4.3.0", 
    "@vue/cli-service": "~4.3.0", 
    "babel-eslint": "^10.1.0", 
    "eslint": "^6.7.2", 
    "eslint-plugin-vue": "^6.2.2", 
    "vue-template-compiler": "^2.6.11" 
  }, 
  "eslintConfig": {
    "root": true, 
    "env": { 
      "node": true 
    }, 
    "extends": [ 
      "plugin:vue/essential", 
      "eslint:recommended" 
    ], 
    "parserOptions": { 
      "parser": "babel-eslint" 
    }, 
    "rules": {} 
  }, 
  "browserslist": [ 
    "> 1%", 
    "last 2 versions", 
    "not dead" 
  ]
}
```
