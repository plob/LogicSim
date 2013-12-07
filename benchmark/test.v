module c17 (N1,N2,N3,N20);

input N1,N2;

output N20;

and AND (N20, N1, N2);
nand NAND (N20, N1, N2);
or OR (N20, N1, N2);
nor NOR (N20, N1, N2);
xor XOR (N20, N1, N2);

endmodule
