class Layer(object):
    def act(self, proximities, lights, acceleration):
        """
        General action method for a layer.
        Sould return a two-tuple with (outputs, should_supress)
        """
        raise NotImplementedError
