(and
      (on_table block2)
      (= (block_height block2) 0)
      (on_block block6 block2)
      (= (block_height block6) 1)
      (on_block block4 block6)
      (= (block_height block4) 2)
    )