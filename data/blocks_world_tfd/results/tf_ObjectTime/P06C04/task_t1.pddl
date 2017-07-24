(and
      (on_table block1)
      (= (block_height block1) 0)
      (on_block block11 block1)
      (= (block_height block11) 1)
      (on_block block6 block11)
      (= (block_height block6) 2)
    )