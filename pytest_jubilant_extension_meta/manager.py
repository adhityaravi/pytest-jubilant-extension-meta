#!/usr/bin/env python3
# Copyright 2025 Canonical Ltd.
# See LICENSE file for licensing details.

"""Extension manager for pytest-jubilant extensions."""

import importlib
import logging
from typing import Dict, Type, Optional, List
from .base import BaseExtension, DefaultExtension

logger = logging.getLogger(__name__)


class ExtensionManager:
    """Manages discovery and loading of pytest-jubilant extensions."""
    
    def __init__(self):
        self._extensions: Dict[str, Type[BaseExtension]] = {}
        self._discover_extensions()
    
    def _discover_extensions(self):
        """Auto-discover extensions via entry points."""
        try:
            import pkg_resources  # much more succinct but additional dep.
            for entry_point in pkg_resources.iter_entry_points('pytest_jubilant.extensions'):
                try:
                    extension_class = entry_point.load()
                    if issubclass(extension_class, BaseExtension):
                        self._extensions[entry_point.name] = extension_class
                        logger.info(f"Discovered extension: {entry_point.name}")
                    else:
                        logger.warning(f"Extension {entry_point.name} does not inherit from BaseExtension")
                except ImportError as e:
                    logger.debug(f"Extension {entry_point.name} not available: {e}")
        except ImportError:
            # pkg_resources not available, try importlib.metadata
            self._discover_with_importlib()
    
    def _discover_with_importlib(self):
        """Fallback discovery using importlib.metadata."""
        try:
            from importlib.metadata import entry_points
            eps = entry_points()
            if hasattr(eps, 'select'):
                # Python 3.10+
                jubilant_eps = eps.select(group='pytest_jubilant.extensions')
            else:
                # Python 3.8-3.9. do we even need to support this?
                jubilant_eps = eps.get('pytest_jubilant.extensions', [])
            
            for entry_point in jubilant_eps:
                try:
                    extension_class = entry_point.load()
                    if issubclass(extension_class, BaseExtension):
                        self._extensions[entry_point.name] = extension_class
                        logger.info(f"Discovered extension: {entry_point.name}")
                except ImportError as e:
                    logger.debug(f"Extension {entry_point.name} not available: {e}")
        except ImportError:
            logger.debug("No extension discovery mechanism available")
    
    def get_extension(self, name: str) -> Type[BaseExtension]:
        """Get extension by name, fallback to default."""
        return self._extensions.get(name, DefaultExtension)
    
    def available_extensions(self) -> List[str]:
        """List available extensions."""
        return list(self._extensions.keys())
    
    def get_extension_instance(self, name: str) -> BaseExtension:
        """Get extension instance by name."""
        extension_class = self.get_extension(name)
        return extension_class()
    
    def register_cli_options(self, parser):
        """Register CLI options for all available extensions."""
        try:
            group = parser.getgroup("jubilant")
        except ValueError:
            # Group doesn't exist yet, create it. this is probably invasive. pytest-jubilant should handle this rather.
            group = parser.getgroup("jubilant", "pytest-jubilant options")
        
        for extension_class in self._extensions.values():
            # Create temporary instance to get metadata
            try:
                temp_instance = extension_class()
                group.addoption(
                    f"--{temp_instance.cli_option}",
                    action="store_true",
                    default=False,
                    help=temp_instance.help_text,
                )
            except Exception as e:
                logger.warning(f"Failed to register CLI option for extension {extension_class}: {e}")


# Global extension manager instance
extension_manager = ExtensionManager()
