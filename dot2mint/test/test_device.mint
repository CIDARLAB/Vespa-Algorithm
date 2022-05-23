DEVICE test_device

LAYER FLOW 

PORT f1 ;
PORT f2 ;
PORT f3 ;
PORT f4 ;
PORT f5 ;
PORT fo1 ;
PORT fo2 ;



CHANNEL connection_0 from f1  to f4   ;
CHANNEL connection_1 from f1  to f5   ;
CHANNEL connection_2 from f1  to fo1   ;
CHANNEL connection_3 from f2  to fo1   ;
CHANNEL connection_4 from f2  to fo2   ;
CHANNEL connection_5 from f3  to f2   ;
CHANNEL connection_6 from f3  to fo1   ;
CHANNEL connection_7 from f4  to f2   ;
CHANNEL connection_8 from f4  to f3   ;
CHANNEL connection_9 from f4  to fo2   ;
CHANNEL connection_10 from f5  to f2   ;
CHANNEL connection_11 from fo1  to f5   ;
CHANNEL connection_12 from fo1  to fo2   ;
CHANNEL connection_13 from fo2  to f3   ; 

END LAYER

LAYER CONTROL 

PORT c1 ;

VALVE3D v1 on connection_2 ;
VALVE3D v2 on connection_6 ;

CHANNEL control_connection_0 from v1  to c1   ;
CHANNEL control_connection_1 from v2  to c1   ; 

END LAYER

