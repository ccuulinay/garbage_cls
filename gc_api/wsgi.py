from api import application, api
from pages import static_pages
from api.dev.views import dev_ns
from api.supervisor_ayi.views import supervisor_ayi_ns
from api.garbage_classifier.service import load_model


api.add_namespace(dev_ns, "/api/v1/dev")
api.add_namespace(supervisor_ayi_ns, "/api/v1/ayi")


application.register_blueprint(static_pages)

api.init_app(application)


load_model()

if __name__ == "__main__":
    application.run(host="0.0.0.0", port=40086, debug=True)