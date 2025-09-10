#!/usr/bin/env python3
# Copyright 2025 Canonical Ltd.
# See LICENSE file for licensing details.

"""Extension-aware Juju class for pytest-jubilant."""

import pathlib
from typing import Union, Optional
from collections.abc import Iterable, Mapping

try:
    import jubilant
    from jubilant import ConfigValue
    from .base import DefaultExtension

    class ExtensionAwareJuju(jubilant.Juju):
        """Extension-aware Juju class that integrates with pytest-jubilant extensions."""

        def __init__(
            self,
            *,
            model: str | None = None,
            wait_timeout: float = 3 * 60.0,
            cli_binary: str | pathlib.Path | None = None,
            extension=None,
        ):
            super().__init__(
                model=model,
                wait_timeout=wait_timeout,
                cli_binary=cli_binary,
            )
            self.extension = extension or DefaultExtension()

        def deploy(
            self,
            charm: str | pathlib.Path,
            app: str | None = None,
            *,
            attach_storage: str | Iterable[str] | None = None,
            base: str | None = None,
            bind: Mapping[str, str] | str | None = None,
            channel: str | None = None,
            config: Mapping[str, ConfigValue] | None = None,
            constraints: Mapping[str, str] | None = None,
            force: bool = False,
            num_units: int = 1,
            overlays: Iterable[str | pathlib.Path] = (),
            resources: Mapping[str, str] | None = None,
            revision: int | None = None,
            storage: Mapping[str, str] | None = None,
            to: str | Iterable[str] | None = None,
            trust: bool = False,
        ) -> None:
            # Get app name for hooks
            app_name = app or str(charm)

            # Pre-deployment hook
            self.extension.pre_deploy_hook(self, charm, app_name)

            # Apply extension modifications to deployment args
            kwargs = {
                "attach_storage": attach_storage,
                "base": base,
                "bind": bind,
                "channel": channel,
                "config": config,
                "constraints": constraints,
                "force": force,
                "num_units": num_units,
                "overlays": overlays,
                "resources": resources,
                "revision": revision,
                "storage": storage,
                "to": to,
                "trust": trust,
            }
            kwargs = self.extension.modify_deploy_args(kwargs)

            # Perform deployment
            super().deploy(charm, app, **kwargs)

            # Post-deployment hook
            self.extension.post_deploy_hook(self, app_name, charm)

except ImportError:
    # jubilant not available - create placeholder
    class ExtensionAwareJuju:
        def __init__(self, *args, **kwargs):
            raise ImportError(
                "ExtensionAwareJuju requires jubilant. "
                "Install with: pip install jubilant"
            )
