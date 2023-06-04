Redis Adapter for PyCasbin 
====

[![GitHub Actions](https://github.com/pycasbin/redis-adapter/workflows/build/badge.svg?branch=master)](https://github.com/pycasbin/redis-adapter/actions)
[![Coverage Status](https://coveralls.io/repos/github/pycasbin/redis-adapter/badge.svg?branch=master)](https://coveralls.io/github/pycasbin/redis-adapter?branch=master)
[![Version](https://img.shields.io/pypi/v/casbin_redis_adapter.svg)](https://pypi.org/project/casbin_redis_adapter/)
[![PyPI - Wheel](https://img.shields.io/pypi/wheel/casbin_redis_adapter.svg)](https://pypi.org/project/casbin_redis_adapter/)
[![Pyversions](https://img.shields.io/pypi/pyversions/casbin_redis_adapter.svg)](https://pypi.org/project/casbin_redis_adapter/)
[![Download](https://img.shields.io/pypi/dm/casbin_redis_adapter.svg)](https://pypi.org/project/casbin_redis_adapter/)
[![License](https://img.shields.io/pypi/l/casbin_redis_adapter.svg)](https://pypi.org/project/casbin_redis_adapter/)

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