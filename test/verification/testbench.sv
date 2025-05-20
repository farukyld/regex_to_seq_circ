// see: https://chatgpt.com/share/68136a46-8298-800f-968c-beab5a84ea0f
module tb_seq_circt;

  logic clk, rst;
  logic [7:0] x;
  logic y;

  // File handles
  const integer stdin_fd = 32'h8000_0000;

  seq_circuit inst (
    .clk(clk),
    .rst(rst),
    .x_i(x),
    .y_o(y)
  );

  always #5 clk = ~clk;

  initial begin
    clk = 0;
    rst = 1;

    #13 rst = 0;

    while (!$feof(stdin_fd)) begin
    @(negedge clk);
    // verilator lint_off WIDTHTRUNC
      x = $fgetc(stdin_fd);
    // verilator lint_on WIDTHTRUNC

    // verilator lint_off IGNOREDRETURN
    #1 $writeb(y);
    // lint_on
    end

    $finish;
  end

endmodule
