from typing import Callable, Optional

JSONPrimitive = str | int | float | bool

TransformFunc = Callable[[Optional[JSONPrimitive]], Optional[JSONPrimitive]]
