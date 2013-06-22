MznResolver
===========

Resolves SABR program using MiniZinc.

This tests a translation from CNF derived from SABR to MiniZinc. The tests
are for solving a Rubics which has been scrambled to varying degrees. The
longest a scramble could take to solve is 20.

To test, place SABR folder with sabr executable next to MznResolver and run

python resolver.py &ltrubiks test size&gt

The result will be placed in out/result/cube-&ltrubiks test size&gt-result.txt
