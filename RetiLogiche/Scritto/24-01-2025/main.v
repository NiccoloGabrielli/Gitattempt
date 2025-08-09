module ABC(reset_, clock, x2, eoc2, soc2, x1, eoc1, soc1, out);

    input reset_, clock;
    input[7:0] x1, x2;
    input eoc1, eoc2;

    output soc1, soc2, out;


    reg [7:0] v1, v2;
    reg SOC1, SOC2; assign soc1 = SOC1; assign soc2 = SOC2;
    reg OUT; assign out = OUT;

    wire [7:0] out_rc;
    MEDIA m(
        .v1(v1), .v2(v2), .m(out_rc)
    );
    reg[7:0] duration;


    reg[3:0] STAR;
    localparam
        S0 = 0,
        S1 = 1,
        S2 = 2,
        S3 = 3, 
        S4 = 4,
        S5 = 5;


    // media is going to stay on 8 bits as it's an addition of 2 natural numbers and then a division by 2 (right-shift)

    // Going to do the states casually and then sharpen them later

    always @(reset_ == 0) begin
        SOC1 <= 0; SOC2 <= 0;
        STAR <= 0;
    end    



    always @(posedge clock) if(reset_ == 1) #3 begin

        casex(STAR)

            S0: begin SOC1 <= 1; SOC2 <= 1; v1 <= x1; v2 <= v2; 
                STAR <= ({eoc1, eoc2} == 2'b00) ? S1: S0;
            end

            S1: begin duration <= out_rc; SOC1<= 0; SOC2 <= 0;
                STAR <= (duration != 0) ? S2: S3;
            end

            S2: begin OUT <= 1; duration <= duration - 1;
                STAR <= (duration == 1)? S3: S2;    // checking for duration == 1 because the change of duration will happen at the next clock change 
            end

            S3: begin OUT <= 0;
                STAR <= ({eoc1,eoc2} == 2'b11) ? S0: S3;
                
            end

        endcase


    end 

endmodule


module MEDIA(
    v1, v2, 
    m
);

    input[7:0] v1, v2;
    output[7:0] m;

    assign #1 m = (v1+v2)/2;    // I don't know if we can do divison, it would've been smarter to just take the 8 top bits


endmodule



// Sintesi 