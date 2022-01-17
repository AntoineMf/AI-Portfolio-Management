class Singleton(type):
    __instances = {}

    def __call__(class__, *args, **kwargs):
        if class__ not in class__.__instances:
            class__.__instances[class__] = super(Singleton, class__).__call__(*args, **kwargs)
        return class__.__instances[class__]
