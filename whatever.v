
// Library - ysc_layout, Cell - auto_route, View - schematic
// LAST TIME SAVED: Feb 19 17:29:33 2020
// NETLIST TIME: Feb 19 17:31:01 2020
`timescale 1ns / 1ns 

module auto_route ( ABO, AI1, AI2, BI, TI1, TI2 );

output  ABO;

input  AI1, AI2, BI, TI1, TI2;


specify 
    specparam CDS_LIBNAME  = "ysc_layout";
    specparam CDS_CELLNAME = "auto_route";
    specparam CDS_VIEWNAME = "schematic";
endspecify

and_e I0 ( .BI(BI), .ABO(net14), .TI(TI2),
     .AI(AI2));
cb_a I2 ( .ABO(ABO), .BI(net14), .AI(net13));
d22_a I1 ( .TO(net13), .TI(TI1), .AI(AI1));

endmodule