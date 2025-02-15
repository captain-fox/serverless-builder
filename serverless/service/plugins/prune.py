from serverless.service.plugins.generic import Generic


class Prune(Generic):
    yaml_tag = u"!PrunePlugin"

    def __init__(self, automatic=True, number=3):
        super().__init__("serverless-prune-plugin")
        self.automatic = automatic
        self.number = number

    def enable(self, service):
        export = dict(self)
        export.pop("name", None)

        service.custom.prune = export
