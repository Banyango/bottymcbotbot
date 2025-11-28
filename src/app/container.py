import wireup
from wireup.integration import fastapi

import libs
import core
import app.config as config

container = wireup.create_async_container(
    # Add service modules
    service_modules=[
        # Top level module containing service registrations.
        config,
        core,
        libs,
        fastapi,
    ]
)
