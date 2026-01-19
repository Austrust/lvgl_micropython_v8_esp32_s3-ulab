# MicroPython CMake configuration for user C modules
# This file integrates LVGL v8 and ulab into the MicroPython build

# Include ulab module
set(ULAB_DIR ${CMAKE_CURRENT_LIST_DIR}/../lib/ulab/code)
if(EXISTS ${ULAB_DIR}/micropython.cmake)
    include(${ULAB_DIR}/micropython.cmake)
endif()

# Include LVGL bindings
set(LV_BINDINGS_DIR ${CMAKE_CURRENT_LIST_DIR}/../lib/lv_bindings)
if(EXISTS ${LV_BINDINGS_DIR}/micropython.cmake)
    include(${LV_BINDINGS_DIR}/micropython.cmake)
endif()
