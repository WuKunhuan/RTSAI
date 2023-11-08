file(REMOVE_RECURSE
  "RTSAI"
  "RTSAI.pdb"
)

# Per-language clean rules from dependency scanning.
foreach(lang )
  include(CMakeFiles/RTSAI.dir/cmake_clean_${lang}.cmake OPTIONAL)
endforeach()
