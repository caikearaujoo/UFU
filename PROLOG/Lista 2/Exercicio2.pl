main():-
    		write('Digite seu nome: '),
    		read(X),
    		nl,
    		write('Digite sua nota 1: '),
    		read(N1),
    		nl,
    		write('Digite sua nota 2: '),
    		read(N2),
    		nl,
    		write('Digite sua nota 3: '),
    		read(N3),
    		nl,
    		write('Digite sua nota 4: '),
    		read(N4),
    		nl,
    		write('Digite sua nota 5: '),
    		read(N5),
    		nl,
    		aprovado(X, N1, N2, N3, N4, N5),
			nl,
			S is (N1+N2+N3+N4+N5),
    		MA is (S/5),
    		write('Sua media aritmetica eh: '),
    		write(MA).

aprovado(_X, N1, N2, N3, N4, N5):-
    							(N1>60 -> write('X foi aprovado na materia1 com a nota: '),
    									write(N1); true), nl,
    							(N2>60, write('X foi aprovado na materia1 com a nota: '),
    									write(N2); true), nl,
    							(N3>60, write('X foi aprovado na materia1 com a nota: '),
    									write(N3); true), nl,
    							(N4>60, write('X foi aprovado na materia1 com a nota: '),
    									write(N4); true), nl,
    							(N5>60, write('X foi aprovado na materia1 com a nota: '),
    									write(N5); true).