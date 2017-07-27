(and
      (on_table block10)
      (= (block_height block10) 0)
      (on_block block7 block10)
      (= (block_height block7) 1)
      (on_block block2 block7)
      (= (block_height block2) 2)
    )