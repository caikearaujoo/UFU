tam([X], 1).
tam([_|Y], N):- tam(Y, N1),
    		N is N1+1.
