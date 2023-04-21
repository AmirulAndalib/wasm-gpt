#
# gpt-2

set(CMAKE_C_FLAGS  "${CMAKE_C_FLAGS} -pthread")

set(TEST_TARGET gpt-2)
add_executable(${TEST_TARGET} main.cpp index.html)
target_link_libraries(${TEST_TARGET} PRIVATE ggml ggml_utils)

if (DEFINED EMSCRIPTEN)
    set(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} --shell-file ${CMAKE_CURRENT_SOURCE_DIR}/index.html")
    set_target_properties(gpt-2 PROPERTIES 
      SUFFIX ".html" 
      LINK_FLAGS "-pthread -g4 --bind --use-preload-cache \
        -s MINIFY_HTML=0 \
        -s ASYNCIFY=1 \
        -s USE_PTHREADS=1 \
        -s PTHREAD_POOL_SIZE=5 \
        -s PROXY_TO_PTHREAD=1 \
        -s ASSERTIONS \
        -s INITIAL_MEMORY=3GB \
        -s NO_EXIT_RUNTIME=1 \
        -s ALLOW_TABLE_GROWTH=1 \
        --preload-file ${CMAKE_CURRENT_SOURCE_DIR}/models@models/"
    )
endif (DEFINED EMSCRIPTEN)


#
# gpt-2-quantize

set(TEST_TARGET gpt-2-quantize)
add_executable(${TEST_TARGET} quantize.cpp)
target_link_libraries(${TEST_TARGET} PRIVATE ggml ggml_utils)