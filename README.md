# global-manager

![Tests](https://github.com/shmakovpn/global-manager/actions/workflows/python-package.yml/badge.svg)
[![codecov](https://codecov.io/github/shmakovpn/global-manager/graph/badge.svg?token=744XXMAKOZ)](https://codecov.io/github/shmakovpn/global-manager)
![Mypy](https://github.com/shmakovpn/global-manager/actions/workflows/mypy.yml/badge.svg)
[![pypi](https://img.shields.io/pypi/v/global-manager.svg)](https://pypi.python.org/pypi/global-manager)
[![downloads](https://static.pepy.tech/badge/global-manager/month)](https://pepy.tech/project/global-manager)
[![versions](https://img.shields.io/pypi/pyversions/global-manager.svg)](https://github.com/shmakovpn/global-manager)


Global thread context manager.

## Installation 

```bash
pip install global-manager
```

## Examples

```py
from typing import Optional
import dataclasses
import logging
from global_manager import GlobalManager

logger = logging.getLogger('my_view')

@dataclasses.dataclass
class UserContext:
    """Some context"""
    ip: str
    profile_id: int

class UserContextManager(GlobalManager[UserContext]):
    @classmethod
    def get_current_user_context(cls) -> Optional[UserContext]:
        """a business meaning method name is a good practice"""
        return cls.get_current_context()


def my_func():
    user_context: Optional[UserContext] = UserContextManager.get_current_user_context()
    # retrieve context
    logger.debug('my_view profile_id=%s, ip=%s', user_context.profile_id, user_context.ip)
    # other logic ...


# some where in code, m.b. in web framework
def my_view(request):
    # Imagine that the data is obtained from the request
    user_context = UserContext(ip='127.0.0.1', profile_id=1)
    
    with UserContext(user_context):
        return my_func()
```

Context in context.

```py
with UserContext(uc1):
    UserContext.get_current_user_context()  # uc1 context
    
    with UserContext(uc2):
        UserContext.get_current_user_context() # uc2 context

    UserContext.get_current_user_context()  # uc1 context

UserContext.get_current_user_context()  # None
```

Async notations is supported too.

```py
async with UserContext(uc1):
    UserContext.get_current_user_context()  # uc1 context
    
    async with UserContext(uc2):
        UserContext.get_current_user_context() # uc2 context

    UserContext.get_current_user_context()  # uc1 context

UserContext.get_current_user_context()  # None
```
