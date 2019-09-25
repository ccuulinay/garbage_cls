from flask_restplus import Namespace, Resource
from api.dev.models import who_parser

dev_ns = Namespace('dev', description="dev operations")


@dev_ns.route("")
class Dev(Resource):
    """
    Dev operations for ping
    """

    # @jwt_required
    @dev_ns.expect(who_parser)
    def get(self):
        args = who_parser.parse_args()
        msg = {"Message": "Welcome " + args['who']}
        return msg


@dev_ns.route("/<string:name>")
class Dev(Resource):
    def get(self, name):
        """

        :param name:
        :return:
        """
        msg = {"Message": "你好 " + name}
        return msg

