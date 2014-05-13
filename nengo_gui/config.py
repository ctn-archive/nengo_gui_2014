import nengo
import nengo.config


class Config(nengo.config.Config):
    def __init__(self, parent=None):
        super(Config, self).__init__(parent=parent)
        for klass in [nengo.Ensemble, nengo.Node, nengo.Network]:
            self.configures(klass)
            self[klass].set_param('pos', nengo.config.Parameter(None))
