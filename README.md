# (T)ext file based (T)ime (T)racking

To generate and browse documentation run:

    $ pip install -r requirements.txt
    $ make
    $ open build/html/index.html

Usage:

    $ python ttt.py example/TT_* -hr
    * January 2016
        OTRP:1      50h        
        TT:0        56h        
        TT:1        44h        
        =>         150h        

    * February 2016
        OTRP:3      41h 49min
        TT:0        49h        
        TT:1        39h 11min
        =>         130h        

    2016-01-03..........2016-02-24
    ------------------------------
        OTRP:1      50h        
        OTRP:3      41h 49min
        TT:0       105h        
        TT:1        83h 11min
    ==============================
    Total      280h
