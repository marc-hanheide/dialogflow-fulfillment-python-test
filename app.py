#!/usr/bin/env python
import web

import logging
from json import loads, dumps
from pprint import pformat

logging.basicConfig(level=logging.DEBUG)



urls = (
    '/webhook', 'index'
)


class index:

    def POST(self):
        return self.process()

    def GET(self):
        return self.process()

    def on_add_item(self, d):
        logging.debug('called add_item')
        return "it worked"

    def _dispatch(self, r):
        if 'action' in r:
            method = r['action']
            try:
                method_to_call = getattr(self, 'on_%s' % method)
                logging.info('dispatch to method on_%s' % method)
            except AttributeError:
                logging.warn('cannot dispatch method %s' % method)
                return
            return method_to_call(r)

    def process(self):
        req = web.input()
        data = web.data()
        logging.info(req)
        d = loads(data)
        logging.info(pformat(d))
        try:
            r = self._dispatch(d['result'])
        except Exception as e:
            logging.warn("couldn't dispatch")
            return web.BadRequest(e)
        web.header('Content-Type', 'application/json')

        response = {
          "speech": r,
          "displayText": r,
          "data": {},
          "contextOut": [],
          "source": "server"
        }

        return dumps(response)
    # action = req.get('result').get('action')

    # # Check if the request is for the translate action
    # if action == 'translate.text':
    #     # Get the parameters for the translation
    #     text = req['result']['parameters'].get('text')
    #     source_lang = req['result']['parameters'].get('lang-from')
    #     target_lang = req['result']['parameters'].get('lang-to')

    #     # Fulfill the translation and get a response
    #     output = translate(text, source_lang, target_lang)

    #     # Compose the response to API.AI
    #     res = {'speech': output,
    #            'displayText': output,
    #            'contextOut': req['result']['contexts']}
    # else:
    #     # If the request is not to the translate.text action throw an error
    #     LOG.error('Unexpected action requested: %s', json.dumps(req))
    #     res = {'speech': 'error', 'displayText': 'error'}

    # return make_response(jsonify(res))


if __name__ == "__main__":
    app = web.application(urls, globals())
    app.internalerror = web.debugerror
    app.run()
