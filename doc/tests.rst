Testing
=======


:Author:    Martin Užák <martin.uzak@gmail.com>
:Creation:  2017-01-05 14:15
:File:      tests.rst
:Abstract:  This document describes the testplan for `ttt`.

input variations
----------------

doctests 
--------
used for testing the logic. As a side effect, doctest provide handy
documentation too.

unittests
---------
Test the integration of various components, i.e. `ttt` (the driver module) and
`data` the data model.

use cases
---------
as defined in the requirements

external interfaces
-------------------
No tests necessary 

exceptions
----------
Make sure the exceptions are propagated as documented
