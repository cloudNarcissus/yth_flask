#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask import request, json

from werkzeug.exceptions import HTTPException


class ApiException(HTTPException):
    code = 500
    description = u'服务端出现异常'

    def get_headers(self, environ=None):
        """Get a list of headers."""
        return [('Content-Type', 'application/json')]

    def get_body(self, environ=None):
        """Get the HTML body."""
        msg = {
            'code': self.code,
            'message': self.description,
            'request': request.method + ' ' + self.get_url_no_param()
        }
        return json.dumps(msg)

    @staticmethod
    def get_url_no_param():
        full_path = str(request.full_path)
        url_no_param = full_path.split('?')[0]
        return url_no_param


class Success(ApiException):
    code = 201
    description = u'成功'


class DeleteSuccess(Success):
    code = 202
    description = u'删除成功'


class BadRequest(ApiException):
    code = 400
    description = u'接口调用方式不合法'


class Forbidden(ApiException):
    code = 403
    description = u'接口不允许调用'


class NotFound(ApiException):
    code = 404
    description = u'接口不存在'


class ServerError(ApiException):
    pass
