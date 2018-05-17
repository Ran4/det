#!/usr/bin/env python3
from typing import TypeVar, Callable, Dict, Any
    
A = TypeVar('A')
B = TypeVar('B')
C = TypeVar('C')
D = TypeVar('D')

def map_dict(f: Callable[[A], B],
             d: Dict[Any, A]) \
             -> Dict[Any, B]:
    return {key: f(value) for key, value in d.items()}
