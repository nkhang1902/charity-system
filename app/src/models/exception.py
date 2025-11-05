from flask import Response
from collections import OrderedDict
import json


class ApiException(Exception):
    def __init__(self, error: str, status_code: int = 500):
        super().__init__(error)
        self.error = error
        self.status_code = status_code

    def to_response(self):
        print(self.error)
        response_body = OrderedDict([
            ("error", self.error)
        ])
        return Response(
            response=json.dumps(response_body),
            status=self.status_code,
            mimetype='application/json'
        )