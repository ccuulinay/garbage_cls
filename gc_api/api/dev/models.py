from flask_restplus import fields, reqparse

who_parser = reqparse.RequestParser()
who_parser.add_argument('who', type=str, location='args')