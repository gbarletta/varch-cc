# C compiler for varch

I'm trying to write a compiler that targets my abstract virtual machine, Venere. Would be nice to compile a subset of C: 
* no preprocessor
* no function prototypes
* no structs
* no array accesses (just use pointers, kid!)
* lots of keywords are ignored (export, inline, ...)

It will take time, but let's see how it goes :>