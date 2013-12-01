module c17 (N1,N2,N3,N4,N5,N6,N7,N8,N9,N10,N20,N22,N23,N24,N25);

input N1,N2,N3,N4,N5,N6,N7,N8,N9,N10;

output N20,N22,N23,N24,N25;

and AND (N20, N1, N2);
nand NAND (N21, N3, N4);
or OR (N22, N5, N6);
nor NOR (N23, N7, N8);
xor XOR (N24, N9, N10);

endmodule
