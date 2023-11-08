
# 1. make the target

# Discard the CMake option by this time
# cmake .

clear
make --quiet install

# exit_status=$?
# if [ $exit_status -eq 0 ]; then
#     echo "Make command completed successfully."
# else
#     echo "Make command encountered an error. Exit status: $exit_status"
# fi

# remove temporary files
rm -rf CMakeCache.txt
rm -rf cmake_install.cmake
rm -rf CMakeFiles
