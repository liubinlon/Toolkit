add_subdirectory(px_vp20)
add_subdirectory(pxrUsdMayaGL)
add_subDirectory(vp2ComputeShaders)
add_subdirectory(vp2RenderDelegate)
add_subdirectory(vp2ShaderFragments)
if (CMAKE_WANT_MATERIALX_BUILD)
    add_subdirectory(MaterialXGenOgsXml)
endif()
