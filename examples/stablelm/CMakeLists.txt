#
# stablelm

set(TEST_TARGET stablelm)
add_executable(${TEST_TARGET} main.cpp)
target_link_libraries(${TEST_TARGET} PRIVATE ggml ggml_utils)

#
# stablelm-quantize

set(TEST_TARGET stablelm-quantize)
add_executable(${TEST_TARGET} quantize.cpp)
target_link_libraries(${TEST_TARGET} PRIVATE ggml ggml_utils)
