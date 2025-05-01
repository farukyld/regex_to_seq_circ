// see: https://chatgpt.com/share/68136a46-8298-800f-968c-beab5a84ea0f
module tb_seq_circt;

  logic clk, rst;
  logic [7:0] x;
  logic [7:0] y;

  // File handles
  integer input_file, output_file;
  string input_line;
  int r;

  // Instantiate the DUT
  seq_circt inst (
    .clk(clk),
    .rst(rst),
    .x(x),
    .y(y)
  );

  // Clock generation
  always #5 clk = ~clk;

  // File-based stimulus and capture
  initial begin
    // Initialize
    clk = 0;
    rst = 1;
    y = 8'd0;

    // Open files
    input_file = $fopen("input.txt", "r");
    output_file = $fopen("output.txt", "w");

    if (input_file == 0 || output_file == 0) begin
      $display("ERROR: Failed to open file(s).");
      $finish;
    end

    // Reset pulse
    #10 rst = 0;

    // Read and feed each char per cycle
    while (!$feof(input_file)) begin
      byte c;
      r = $fread(c, input_file);  // read a single byte
      y = c;

      @(negedge clk); // take snapshot before next posedge
      $fwrite(output_file, "%0t: x = %02x\n", $time, x);
    end

    // Finish
    $fclose(input_file);
    $fclose(output_file);
    $finish;
  end

endmodule
