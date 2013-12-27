"""
Stub LTI server for manual testing.

Used for manual testing and testing on sandbox.
"""
from stubs.lti import StubLtiService

try:
    stub_server = StubLtiService(8765)
except KeyboardInterrupt:
    print('^C received, shutting down server')
    stub_server.shutdown()
