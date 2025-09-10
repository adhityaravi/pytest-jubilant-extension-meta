#!/usr/bin/env python3
# Copyright 2025 Canonical Ltd.
# See LICENSE file for licensing details.

"""Base classes for pytest-jubilant extensions."""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

class BaseExtension(ABC):
    """Base class for pytest-jubilant extensions."""
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Extension name for CLI options and identification."""
        pass
    
    @property
    @abstractmethod
    def cli_option(self) -> str:
        """CLI option name (e.g., 'meshify' for --meshify)."""
        pass
    
    @property
    @abstractmethod
    def help_text(self) -> str:
        """Help text for the CLI option."""
        pass
    
    @abstractmethod
    def setup_infrastructure(self, temp_model_factory) -> None:
        """Setup any required infrastructure before tests."""
        pass
    
    @abstractmethod
    def modify_deploy_args(self, kwargs: Dict[str, Any]) -> Dict[str, Any]:
        """Modify deployment arguments."""
        pass
    
    @abstractmethod
    def post_deploy_hook(self, juju, app_name: str, charm) -> None:
        """Execute after deployment."""
        pass
    
    def pre_deploy_hook(self, juju, charm, app_name: str) -> None:
        """Execute before deployment (optional)."""
        pass
    
    def teardown_hook(self, temp_model_factory) -> None:
        """Execute during teardown (optional)."""
        pass


class DefaultExtension(BaseExtension):
    """Default no-op extension."""
    
    @property
    def name(self) -> str:
        return "default"
    
    @property
    def cli_option(self) -> str:
        return "default"
    
    @property
    def help_text(self) -> str:
        return "Default extension (no-op)"
    
    def setup_infrastructure(self, temp_model_factory):
        """No-op infrastructure setup."""
        pass
    
    def modify_deploy_args(self, kwargs):
        """No-op deployment argument modification."""
        return kwargs
    
    def post_deploy_hook(self, juju, app_name, charm):
        """No-op post-deployment hook."""
        pass