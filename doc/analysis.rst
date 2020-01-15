Functional Specification
========================

:Project:   ttt
:Author:    Martin Uzak <martin.uzak@gmail.com>
:Date:      26.12.2016
:Abstract:  This document describes what the customer will be getting, i.e. how
            product `ttt` will look and work like. Also the purpose is to
            explain to developers what to develop and to the testers what to
            test. As a command line tool is requested there are no graphical
            wireframes but sample outputs, descriptions of computations and
            error handling. 

Limitations
-----------
* No editor is to be created. For editing files, user can use any text editor
  of his preference.  
* Multiuser capability is only to be specified, not to be designed nor
  implemented.
* Overlapping days are not supported in a single line. Every entry is
  considered to start and end on the same day.
* A day can have more than 24h. This is not checked.

Input
------

Formal specification of input file structure::

    DATE TIME_VALUE COST_CENTER DESCRIPTION

    DATE        = \d{1,}-\d{1,2}-\d{1,2}
    TIME        = \d{1,2}:\d{1,2}
    TIME_VALUE  = (TIME - TIME) | (\d+h(\s?\d+m)?)
    PRJ_ABBR    = \w+
    PHASE       = \d+
    COST_CENTER = PRJ_ABBR:PHASE
    DESCRIPTION = \S+

* Values can be separated by any number of whitespaces.
* Smallest granilarity of data is minute. 
* Minutes can be left out if they are zero. 
* Hours and minutes can have preceeding zeros.

Example for time value:: 

    2016-01-04 5h30m TT:0 Requirements - first customer meeting

Comments
~~~~~~~~

Everything encountered after `#` incl. this character is regarded as comment and will be ignored::

    # this line is a comment
    2016-11-21 12:00-13:15 PRJ:1 Analisis of requirements # With Marc via skype

Example::
    
    # Start of project TT
    2016-12-11 9:45-10:15 TT:0 Defining requirements
    2016-12-11 2h15m TT:1 Thinking over functional specification

Use Cases
---------
.. Usage

By default the program will read data from all the arguments. All arguments
have to be text files. Every line in those is considered to be an potential
input record. ttt will sum the input according to the cost centers and months
and output this and total information. Default usage::

    ttt (-h|-c) [--from_date DATE] [--from_date DATE] file1.txt ... fileN.txt

Human readable output
~~~~~~~~~~~~~~~~~~~~~

The example below produces a human readable summary for two files. Both belong to the project `TT`, one is for january the other for february 2016::

    ttt -h TT_january_2016.txt TT_febraury_2016.txt

    * January 2016
        OTRP:1         50h
        TT:0           56h
        TT:1           44h
        =>            150h

    * February 2016
        OTRP:3         41h 49min
        TT:0           49h
        TT:1           39h 11min
        =>            130h

    2016-01-01........2016-02-28
    ----------------------------
    TT:0              105h
    TT:1               83h 11min
    OTRP:1             50h
    OTRP:3             41h 49min
    ============================
    Total             280h

CSV output
~~~~~~~~~~~

* -h is for human readable and is default. Other is -c (csv), which outputs a summary for every cost center in the specified time, split by months::

    YEAR,MONTH,PRJ:COST_CENTER,MINUTES

Example::

    $ ttt -h TT_january_2016.txt TT_febraury_2016.txt

    2016,1,TT:0,3360
    2016,1,TT:1,2640
    2016,1,OTRP:1,3000
    2016,2,TT:0,2949
    2016,2,TT:1,4991
    2016,2,OTRP:3,2509

Limiting input
~~~~~~~~~~~~~~
* from_date and to_date options (default = None) specify limits in regard to the input dates used in compuation of the summary. Interval specification is: *[from_date, to_date)* meaning that data with `from_date` is to be included, data having date >= `to_date` is to be excluded ::

    $ ttt -h --from_date 2016-01-15 --to_date 2016-01-22 TT_january_2016.txt 

    January 2016
        TT:0            56h
        TT:1            44h
        OTRP:1          50h
        =>             150h

    2016-01-15  ==>  2016-02-28
    ---------------------------
    TT:0               56h
    TT:1               44h
    OTRP:1             50h
    ===========================
                      280h

External Interface
------------------
The tool itself shall be used in single user mode only. But there shall be provisions for using this tool for colaboration in bigger projects. NOTE: provisions, but no implementations. If requested, the implementation might be covered in later versions. 

For this, client server approach will be used. Every user will have to register
at at a server to get credentials. Then he will be able to submit his data. All
communication will be done using REST::

    POST /register
        <- username
        <- password
        <- email_address
        -> OK / Error

    GET /cost_centers
        # return all valid cost centers
        ->  { "PRJ_ID:PHASE": "Description", 
              ... , 
              "PRJ_ID_N:PHASE_N" : "Description_N" 
            }

    GET /user/data
        <- credentials
        -> ROW_1
           ...
           ROW_N

    POST /user/data
        <- credentials
        <- ROW_1 
           ... 
           ROW_N
        -> OK / Error

Errors
------

In case the input files contain errors, the program will perform no action(s), only describe the error and exit. For errors in the input file(s), it will say the name and line of the file causing trouble. E.g.::

    $ ttt -h --from_date 2016-01-34 --to_date 2016-01-22 TT_january_2016.txt 
    
    Invalid value for `--from_date`: 2016-01-34

    $ ttt -h TT_january_201.txt 
    
    File `TT_january_201.txt` doesn't exist

    $ ttt -h --from_date 2016-01-34 --to_date 2016-01-22 TT_March_2016.txt 
    
    Invalid input: TT_March_2016:63> Specification writing. 2016-11-11 3h PRJ:1

If there is multiple errors in the input file(s), the program will exit immediatelly after the first one. Only after its correction and running the same command again, the second error will be described.
