Redis Adapter for PyCasbin 
====

Redis Adapter is the [redis](https://redis.io/) adapter for [PyCasbin](https://github.com/casbin/pycasbin). With this library, Casbin can load policy from redis or save policy to it.

## Installation

```
pip install casbin_redis_adapter
```

## Simple Example

```python
import casbin_redis_adapter
import casbin

adapter = casbin_redis_adapter.Adapter('localhost', 6379)

e = casbin.Enforcer('path/to/model.conf', adapter, True)

sub = "alice"  # the user that wants to access a resource.
obj = "data1"  # the resource that is going to be accessed.
act = "read"  # the operation that the user performs on the resource.

if e.enforce(sub, obj, act):
    # permit alice to read data1casbin_sqlalchemy_adapter
    pass
else:
    # deny the request, show an error
    pass
```
### Getting Help

- [PyCasbin](https://github.com/casbin/pycasbin)

### License

This project is licensed under the [Apache 2.0 license](LICENSE).