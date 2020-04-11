"""
http://code.activestate.com/recipes/86900/

A generic factory implementation.

Examples:
>>> f=Factory()
>>> class A:pass
>>> f.register("createA",A)
>>> f.createA()
<__main__.A instance at 01491E7C>

>>> class B:
... 	def __init__(self, a,b=1):
... 		self.a=a
... 		self.b=b
...
>>> f.register("createB",B,1,b=2)
>>> f.createB()
>>> b=f.createB()
>>>
>>> b.a
1
>>> b.b
2

>>> class C:
... 	def __init__(self,a,b,c=1,d=2):
... 		self.values = (a,b,c,d)
...
>>> f.register("createC",C,1,c=3)
>>> c=f.createC(2,d=4)
>>> c.values
(1, 2, 3, 4)

>>> f.register("importSerialization",__import__,"cPickle")
>>> pickle=f.importSerialization()
>>> pickle
<module 'cPickle' (built-in)>
>>> f.register("importSerialization",__import__,"marshal")
>>> pickle=f.importSerialization()
>>> pickle
<module 'marshal' (built-in)>

>>> f.unregister("importSerialization")
>>> f.importSerialization()
Traceback (most recent call last):
  File "<interactive input>", line 1, in ?
AttributeError: Factory instance has no attribute 'importSerialization'
"""


class Factory:

    def register(self, methodName, constructor: callable, *args, **kwargs):
        """register a constructor"""
        setattr(self, methodName, Constructor(constructor, args, kwargs))

    def unregister(self, methodName):
        """unregister a constructor"""
        delattr(self, methodName)


class Constructor:
    """
    Constructor will hold a construct function and all arguments for construct
    a specific instance, it will be used to construct an instance in a factory.
    """
    def __init__(self, function: callable, args: list, kwargs: dict):

        assert callable(function), "function should be a callable obj"
        self._function = function
        self._args = args
        self._kwargs = kwargs

    def __call__(self, *args, **kwargs):
        """call function"""
        _args = list(self._args)
        _args.extend(args)
        _kwargs = self._kwargs.copy()
        _kwargs.update(kwargs)
        return self._function(*_args, **_kwargs)


class C:

    def __init__(self, a, b, c=1, d=2):
        self.values = (a, b, c, d)


f = Factory()
f.register("createC", C, 1, c=3)
c = f.createC(2, d=4)  # pylint: disable=no-member
print(c.values)
# Outputs: (1, 2, 3, 4)
