Design
======

:Project:   ttt
:Author:    Martin Užák <martin.uzak@gmail.com>
:Creation:  2017-01-02 11:40
:File:      design.rst
:Abstract:  This document describes the internal technical design for the `ttt`
            project.


Object Oriented Analysis and Design
-----------------------------------
Based on the input file the following structures have been identified:

* Date
* Date_Interval
* Time_Value
* Cost_Center
* Description

Taking into account the operations used on the structures, here is the their
proposed types::

    * Date: datetime.date
    * Date_Interval
      - date
      - start
      - end
      - __int__ -> minutes
    * Time_Value
      - hours
      - mins
      - __int__ -> minutes
    * Cost_Center: str
    * Description: str


Workflow
~~~~~~~~

One actor has been identified:

* TTT - driver class, trigerred by `main()`

.. mermaid::

    graph LR
        subgraph main
        M[main] --> A
        A[argparse] --> M
        M --> C
        subgraph TTT
        C[TTT.__init__] --> R
        R --> |using data.py| R
        R[ttt.read] --> CSV[ttt.csv_output]
        R --> H[ttt.human_readable_output]
        end
        end

Limitations
-----------
* There cannot be -h and -r options, because -h is used internally by argparse. Therefore, use for signalizing output type::

    -csv    CSV output
    -hr     Human Readable output

Notes
-----

* Modules
    * argparse
    * datetime

::

    >>> datetime.datetime.strptime("2012-11-18", "%Y-%m-%d")
    datetime.datetime(2012, 11, 18, 0, 0)
