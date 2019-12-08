#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools
import os


class VulkanConan(ConanFile):
    name = "vulkan"
    version = "1.1.126.0"
    description = "Vulkan is a new generation graphics and compute API that provides high-efficiency, cross-platform access to modern GPUs used in a wide variety of devices from PCs and consoles to mobile phones and embedded platforms."
    url = "https://github.com/flayan/conan-vulkan"
    homepage = "https://www.lunarg.com/vulkan-sdk/"

    # Indicates License type of the packaged library
    license = "MIT"

    # Packages the license for the conanfile.py
    exports = ["LICENSE.md"]

    # Options may need to change depending on the packaged library.
    settings = "os", "arch", "build_type"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = "shared=False", "fPIC=True"

    # Custom attributes for Bincrafters recipe conventions
    source_subfolder = "source_subfolder"

    def config_options(self):
        if self.settings.os == 'Windows':
            del self.options.fPIC

    def source(self):
        source_url = "https://vulkan.lunarg.com/sdk/download"
        if self.settings.os == 'Windows':
            tools.download("{0}/{1}/windows/VulkanSDK-{1}-Installer.exe".format(source_url, self.version), "VulkanSDK.exe")
            self.run("VulkanSDK.exe /S")
            os.rename("c:/VulkanSDK/{0}".format(self.version), self.source_subfolder)

    def get_lib_folder(self):
        if self.settings.os == 'Windows':
            if self.settings.arch == 'x86':
                return os.path.join(self.source_subfolder, "Lib32")
            else:
                return os.path.join(self.source_subfolder, "Lib")

    def get_bin_folder(self):
        if self.settings.os == 'Windows':
            if self.settings.arch == 'x86':
                return os.path.join(self.source_subfolder, "Bin32")
            else:
                return os.path.join(self.source_subfolder, "Bin")

    def package(self):
        self.copy(pattern="LICENSE.txt", dst="licenses", src=self.source_subfolder)

        include_folder = os.path.join(self.source_subfolder, "Include")
        
        self.copy(pattern="*", dst="include", src=include_folder)

        lib_folder = self.get_lib_folder()
        bin_folder = self.get_bin_folder()
        if self.options.shared:
            if self.settings.os == 'Windows':
                if self.settings.build_type == 'Release':
                    self.copy(pattern="*.dll", dst="bin", src=bin_folder, keep_path=False)
                    self.copy(pattern="*.json", dst="bin", src=bin_folder, keep_path=False)
                    self.copy(pattern="*", dst="lib", src=lib_folder, keep_path=False)
                else:
                    self.copy(pattern="*.dll", dst="bin", src=bin_folder, keep_path=False)
                    self.copy(pattern="*.json", dst="bin", src=bin_folder, keep_path=False)
                    self.copy(pattern="*.lib", dst="lib", src=lib_folder, keep_path=False)
                    self.copy(pattern="*.pdb", dst="lib", src=lib_folder, keep_path=False)
        else:
            if self.settings.os == 'Windows':
                if self.settings.build_type == 'Debug':
                    self.copy(pattern="*.pdb", dst="lib", src=lib_folder, keep_path=False)
                self.copy(pattern="*.lib", dst="lib", src=lib_folder, keep_path=False)
        self.copy(pattern="*.exe", dst="tools", src=bin_folder, keep_path=False)
        # self.copy(pattern="*.a", dst="lib", keep_path=False)
        # self.copy(pattern="*.so*", dst="lib", keep_path=False)
        # self.copy(pattern="*.dylib", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["vulkan-1"]
