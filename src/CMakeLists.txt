# set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -pthread")

if (GGML_ALL_WARNINGS)
    if (CMAKE_COMPILER_IS_GNUCC OR CMAKE_C_COMPILER_ID MATCHES "Clang")
        #set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -Wall -Wextra")
        set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} \
            -Wall                           \
            -Wextra                         \
            -Wpedantic                      \
            -Wshadow                        \
            -Wcast-qual                     \
            -Wstrict-prototypes             \
            -Wpointer-arith                 \
            -Wno-unused-function            \
        ")
    else()
        # todo : windows
    endif()
endif()

# compiler flags

if (NOT MSVC)
    set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -Werror=vla")
    #set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -fno-math-errno -ffinite-math-only -funsafe-math-optimizations")
endif()

message(STATUS "CMAKE_SYSTEM_PROCESSOR: ${CMAKE_SYSTEM_PROCESSOR}")

if (NOT UNAME_S)
    execute_process(COMMAND uname -s OUTPUT_VARIABLE UNAME_S)
endif()
if (NOT UNAME_P)
    execute_process(COMMAND uname -p OUTPUT_VARIABLE UNAME_P)
endif()
if (NOT UNAME_M)
    execute_process(COMMAND uname -m OUTPUT_VARIABLE UNAME_M)
endif()
#message(STATUS "UNAME_S: ${UNAME_S}  UNAME_P: ${UNAME_P}  UNAME_M: ${UNAME_M}")

# Mac OS + Arm can report x86_64
# ref: https://github.com/ggerganov/whisper.cpp/issues/66#issuecomment-1282546789
if (UNAME_S MATCHES "Darwin")
    if (NOT UNAME_P MATCHES "arm")
        execute_process(COMMAND sysctl -n hw.optional.arm64 OUTPUT_VARIABLE SYSCTL_M)
	if (SYSCTL_M MATCHES "1")
            #set(UNAME_P "arm")
            #set(UNAME_M "arm64")
	    message(WARNING "Your arch is announced as x86_64, but it seems to actually be ARM64. Not fixing that can lead to bad performance. For more info see: https://github.com/ggerganov/whisper.cpp/issues/66\#issuecomment-#1282546789")
	endif()
    endif()
endif()

if (${CMAKE_SYSTEM_PROCESSOR} MATCHES "arm" OR ${CMAKE_SYSTEM_PROCESSOR} MATCHES "aarch64")
    message(STATUS "ARM detected")
    #set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -mcpu=apple-m1")
else()
    set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -mf16c -msse3 -mrelaxed-simd -pthread")
    # message(STATUS "x86 detected")
    # #set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -mavx -mavx2 -mfma -mf16c")
    # if (UNAME_S MATCHES "Darwin")
    #     execute_process(COMMAND sysctl machdep.cpu.features OUTPUT_VARIABLE AVX1_M)
    #     if (AVX1_M MATCHES "AVX1.0")
    #         set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -mavx")
    #     endif()
    #     execute_process(COMMAND sysctl machdep.cpu.leaf7_features OUTPUT_VARIABLE AVX2_M)
    #     if (AVX2_M MATCHES "AVX2")
    #         set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -mavx2")
    #     endif()
    #     if (AVX1_M MATCHES "FMA")
    #         set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -mfma")
    #     endif()
    #     set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -mf16c")
    # elseif (UNAME_S MATCHES "Linux")
    #     message(STATUS "Linux detected")
    #     execute_process(COMMAND grep "avx " /proc/cpuinfo OUTPUT_VARIABLE AVX1_M)
    #     if (AVX1_M MATCHES "avx")
    #         set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -mavx")
    #     endif()
    #     execute_process(COMMAND grep "avx2 " /proc/cpuinfo OUTPUT_VARIABLE AVX2_M)
    #     if (AVX2_M MATCHES "avx2")
    #         set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -mavx2")
    #     endif()
    #     execute_process(COMMAND grep "fma " /proc/cpuinfo OUTPUT_VARIABLE FMA_M)
    #     if (FMA_M MATCHES "fma")
    #         set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -mfma")
    #     endif()
    #     execute_process(COMMAND grep "f16c " /proc/cpuinfo OUTPUT_VARIABLE F16C_M)
    #     if (F16C_M MATCHES "f16c")
    #         set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -mf16c")
    #     endif()
    #     execute_process(COMMAND grep "sse3 " /proc/cpuinfo OUTPUT_VARIABLE SSE3_M)
    #     if (SSE3_M MATCHES "sse3")
    #         set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -msse3")
    #     endif()
    # elseif (UNAME_S MATCHES "Haiku")
    #     message(STATUS "Haiku detected")
    #     execute_process(COMMAND sysinfo -cpu COMMAND grep "AVX " OUTPUT_VARIABLE AVX1_M)
    #     if (AVX1_M MATCHES "avx")
    #         set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -mavx")
    #     endif()
    #     execute_process(COMMAND sysinfo -cpu COMMAND grep "AVX2 " OUTPUT_VARIABLE AVX2_M)
    #     if (AVX2_M MATCHES "avx2")
    #         set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -mavx2")
    #     endif()
    #     execute_process(COMMAND sysinfo -cpu COMMAND grep "FMA " OUTPUT_VARIABLE FMA_M)
    #     if (FMA_M MATCHES "fma")
    #         set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -mfma")
    #     endif()
    #     execute_process(COMMAND sysinfo -cpu COMMAND grep "F16C " OUTPUT_VARIABLE F16C_M)
    #     if (F16C_M MATCHES "f16c")
    #         set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -mf16c")
    #     endif()
    # else()
    #     set(CMAKE_C_FLAGS  "${CMAKE_C_FLAGS} -mfma -mf16c -mavx -mavx2")
    # endif()
endif()


# ggml

set(TARGET ggml)

# on APPLE - include Accelerate framework
if (APPLE AND NOT GGML_NO_ACCELERATE)
    find_library(ACCELERATE_FRAMEWORK Accelerate)
    if (ACCELERATE_FRAMEWORK)
        message(STATUS "Accelerate framework found")

        set(GGML_EXTRA_LIBS  ${GGML_EXTRA_LIBS}  ${ACCELERATE_FRAMEWORK})
        set(GGML_EXTRA_FLAGS ${GGML_EXTRA_FLAGS} -DGGML_USE_ACCELERATE)
    else()
        message(WARNING "Accelerate framework not found")
    endif()
endif()

if (GGML_OPENBLAS)
    set(OPENBLAS_INCLUDE_SEARCH_PATHS
        /usr/include
        /usr/include/openblas
        /usr/include/openblas-base
        /usr/local/include
        /usr/local/include/openblas
        /usr/local/include/openblas-base
        /opt/OpenBLAS/include
        $ENV{OpenBLAS_HOME}
        $ENV{OpenBLAS_HOME}/include
        )
    find_path(OPENBLAS_INC NAMES cblas.h PATHS ${OPENBLAS_INCLUDE_SEARCH_PATHS})
    find_library(OPENBLAS_LIB NAMES openblas libopenblas)
    if (OPENBLAS_LIB)
        message(STATUS "OpenBLAS found")

        set(GGML_EXTRA_LIBS  ${GGML_EXTRA_LIBS}  ${OPENBLAS_LIB})
        set(GGML_EXTRA_INCS  ${GGML_EXTRA_INCS}  ${OPENBLAS_INC})
	set(GGML_EXTRA_FLAGS ${GGML_EXTRA_FLAGS} -DGGML_USE_OPENBLAS)
    else()
        message(WARNING "OpenBLAS not found")
    endif()
endif()

if (GGML_PERF)
    set(GGML_EXTRA_FLAGS ${GGML_EXTRA_FLAGS} -DGGML_PERF)
endif()

add_library(${TARGET}
    ggml.c
    )

target_include_directories(${TARGET} PUBLIC
    .
    ../include
    ../include/ggml
    ${GGML_EXTRA_INCS}
    )

if (MSVC)
    target_link_libraries(${TARGET} PUBLIC ${GGML_EXTRA_LIBS} ${CMAKE_THREAD_LIBS_INIT})
else()
    target_link_libraries(${TARGET} PUBLIC m ${GGML_EXTRA_LIBS} ${CMAKE_THREAD_LIBS_INIT})
endif()

if (BUILD_SHARED_LIBS)
    target_link_libraries(${TARGET} PUBLIC
        ${CMAKE_DL_LIBS}
        )

    target_compile_definitions(${TARGET} PUBLIC
        GGML_SHARED
        )
endif()

target_compile_definitions(${TARGET} PUBLIC
    ${GGML_EXTRA_FLAGS}
    )

if (MINGW)
    target_link_libraries(${TARGET} PUBLIC
        stdc++
        )
endif()

# if (DEFINED EMSCRIPTEN)
#     set_target_properties(${TARGET} PROPERTIES LINK_FLAGS " --bind -pthread -sPROXY_TO_PTHREAD -sPTHREAD_POOL_SIZE=8 -s NO_EXIT_RUNTIME=1 -s ALLOW_MEMORY_GROWTH=1 -s MAXIMUM_MEMORY=4GB -fno-vectorize")
# endif (DEFINED EMSCRIPTEN)

install(TARGETS ${TARGET}
    LIBRARY DESTINATION lib
    ARCHIVE DESTINATION lib/static
    )
