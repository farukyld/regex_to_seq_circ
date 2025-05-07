// see: https://chatgpt.com/share/68136a46-8298-800f-968c-beab5a84ea0f
module tb_seq_circt;

  import "DPI-C" function int getchar;
  import "DPI-C" function int putchar(int c);
  import "DPI-C" function int eof_stdin();

  logic clk, rst;
  logic [7:0] x;
  logic y;

  // File handles
  integer input_file, output_file;
  string input_line;
  int r;

  seq_circuit inst (
    .clk(clk),
    .rst(rst),
    .x_i(x),
    .y_o(y)
  );

  always #5 clk = ~clk;
  integer i;
  initial begin
    clk = 0;
    rst = 1;

    #10 rst = 0;

    i = 0;
    // while (i < 10) begin
    while (!(|eof_stdin())) begin
    i = i +1;
    // verilator lint_off WIDTHTRUNC
      x = getchar();
    // verilator lint_on WIDTHTRUNC

      @(negedge clk);
      // verilator lint_off IGNOREDRETURN
      putchar({31'b0,y}+48);
      // lint_on
    end

    $finish;
  end

endmodule
