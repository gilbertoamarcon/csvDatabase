(and
      (on_table block9)
      (= (block_height block9) 0)
      (on_block block10 block9)
      (= (block_height block10) 1)
      (on_block block1 block10)
      (= (block_height block1) 2)
    )