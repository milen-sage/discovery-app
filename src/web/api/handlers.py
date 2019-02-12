import json

import tornado
from biothings.web.api.es.handlers.base_handler import BaseESRequestHandler

from .es import Schema, Metadata


class BaseHandler(BaseESRequestHandler):

    def get_current_user(self):
        user_json = self.get_secure_cookie("user").decode('utf-8')
        if not user_json:
            return None
        return json.loads(user_json)


class APIHandler(BaseHandler):
    def post(self):
        req = tornado.escape.json_decode(self.request.body)
        url = req.get('url', '').lower()
        slug = req.get('slug', '').lower()

        user = self.get_current_user()

        if not user:
            res = {'success': False,
                   'error': 'Authenticate first with your github account.'}
            self.set_status(401)
            self.return_json(res)
        else:
            if url and slug:
                meta = Metadata(username=user, url=url, slug=slug)
                schema = Schema(_meta=meta)
                res = schema.save()
                self.return_json({'success': res})
            else:
                self.return_json(
                    {'success': False, 'error': 'Parameters "url" and/or "slug" not found.'})

    def get(self, api_id):
        s = Schema.get(id=api_id)
        self.return_json(s.to_dict())