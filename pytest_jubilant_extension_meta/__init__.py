#!/usr/bin/env python3
# Copyright 2025 Canonical Ltd.
# See LICENSE file for licensing details.

"""Extension framework for pytest-jubilant."""

from .base import BaseExtension, DefaultExtension
from .manager import ExtensionManager, extension_manager
from .juju import ExtensionAwareJuju

__all__ = [
    "BaseExtension",
    "DefaultExtension", 
    "ExtensionManager",
    "extension_manager",
    "ExtensionAwareJuju",
]

__version__ = "99999.99999.99999"
