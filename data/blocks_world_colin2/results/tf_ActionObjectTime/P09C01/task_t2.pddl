(and
      (on_table block11)
      (= (block_height block11) 0)
      (on_block block3 block11)
      (= (block_height block3) 1)
      (on_block block2 block3)
      (= (block_height block2) 2)
    )