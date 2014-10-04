To-do list
==========

Non-captive user interface
--------------------------

Maybe inspirate from nmh for the client?

Interesting read <http://stephenramsay.us/2011/04/09/life-on-the-command-line/>.

### How to?

I see two solutions:

1. Wrap the API in a shell file (calling the Python library) and export
   the session ID in an environment variable, thus passing it to the
   Python library for every request.

   The use would need to source this shell file, and would then have
   access to shell functions internally calling the library and managing
   environment.

2. Save the session ID in a "cookie" file upon the first login,
   something like `~/.cache/virtualis/cookie`, and read from it every
   further access. A command like `virtualis logout` would remove this
   file, and the user would be prompted for password whenever the cookie
   expires.

   This file should be readable only by the user itself, and the
   `virtualis logout` call should really be a reflex to be sure the
   cookie cannot be leaked afterwards. The nice thing with this is the
   password shouldn't stay long in memory, since we can discard it once
   we have the cookie. But this will prevent the auto refresh session
   feature of the actual client (which won't prompt twice for the
   password during a session since it's kept in memory).

   Anyway Python isn't the most suitable language for this kind of
   considerations, I can't be sure the password will be erased from
   memory directly after the program exits.
