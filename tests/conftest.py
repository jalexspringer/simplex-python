"""
Configure pytest for async testing.
"""

# Configure pytest-asyncio mode
pytest_plugins = ["pytest_asyncio"]


# Set the default fixture loop scope and mode
def pytest_configure(config):
    # Set asyncio mode to auto to handle async fixtures correctly
    config.option.asyncio_mode = "auto"
    # Address deprecation warning
    config.option.asyncio_default_fixture_loop_scope = "function"
