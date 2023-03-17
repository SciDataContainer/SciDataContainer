Configuration
=============

Author and E-Mail address
-------------------------

These default values are either been taken from the environment variables `DC_AUTHOR` and `DC_EMAIL` or from a configuration file.
This configuration file is `%USERPROFILE%\scidata.cfg` on Microsoft Windows and `~/.scidata` on other operating systems.
The file is expected to be a text file.
Leading and trailing white space is ignored, as well as lines starting with `#`.
The parameters are taken from lines in the form `<key>=<value>`, with the keywords `author` and `email`. Optional white space before and after the equal sign is ignored. The keywords are case-insensitive.

(Optional) Server settings
--------------------------

In order to be able to use the server, you need an account.
This enables you to get an API key.
For interaction with a server, the credentials file mentioned above (keywords `server` and `key`) or in the environment variables `DC_SERVER` and `DC_KEY`.

Example config file
-------------------

The content of an examplary config file might look like this:

.. code-block:: cfg

    author=InsertYourNameHere
    email=youraddress@example.com
    server=https://data.example.com
    key=487cadbdcca5302b5d24f94609dbadda4f5b034d2f863ec22f9caa739b12690b

(Windows only) Registration of the container format
---------------------------------------------------
On Microsoft Windows you may inspect ZDC files with a double-click in the Windows Explorer. This requires that you register the extension `.zdc` as a copy of `.zip`.
Run the following on the command prompt to achieve this behaviour:

.. code-block:: powershell

    reg copy HKCR\.zip HKCR\.zdc /s /f

