
# make the targets

cmake .

clear
make all

# exit_status=$?
# if [ $exit_status -eq 0 ]; then
#     echo "Make command completed successfully."
# else
#     echo "Make command encountered an error. Exit status: $exit_status"
# fi

# remove temporary files
rm CMakeCache.txt
rm Makefile
rm cmake_install.cmake
rm -rf CMakeFiles