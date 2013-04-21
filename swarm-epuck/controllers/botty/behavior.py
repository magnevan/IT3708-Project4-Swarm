class Behavior(object):
    def act(self, inputs):
        """
        General action method for a behavior.
        Should return a two-tuple with (outputs, should_supress)
        """
        raise NotImplementedError
