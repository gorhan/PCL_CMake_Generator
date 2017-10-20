from sys import argv

PCL_CMAKE_TEMPLATE='''
cmake_minimum_required(VERSION 2.6)
    
set(PROJECT "{0}")
    
# Start a project.
project(${{PROJECT}})

find_package(PCL 1.6 REQUIRED)
find_package(OpenCV REQUIRED)
    
# Search for source code.
file(GLOB folder_source {1}/*.cpp {1}/*.cc {1}/*.c)
file(GLOB folder_header {2}/*.h)
source_group("Source Files" FILES ${{folder_source}})
source_group("Header Files" FILES ${{folder_header}})

# Automatically add include directories if needed.
#foreach(header_file ${{folder_header}})
#  get_filename_component(p ${{header_file}} PATH)
#  include_directories(${{p}})
#endforeach(header_file ${{folder_header}})

# Include any directories needed
include_directories(${{PCL_INCLUDE_DIRS}} {2})
link_directories(${{PCL_LIBRARY_DIRS}})
add_definitions(${{PCL_DEFINITIONS}})

# Set up our main executable.
if (folder_source)
    add_executable(${{PROJECT}} ${{folder_source}} ${{folder_header}})
    target_link_libraries(${{PROJECT}} ${{GSL_LIBRARIES}} ${{PCL_LIBRARIES}} {3})
else (folder_source)
    message(FATAL_ERROR "No source code files found. Please add something")
endif (folder_source)
'''

def usage(argv):
    print "python {0} <PROJECT NAME> <TARGET_DIR> [LIBRARIES, ]".format( argv[0] )

if __name__ == "__main__":
    src_path = "src"
    include_path = "include"
    project_name = None
    target_dir = None
    libs = None
    cmake_filename = "CMakeLists.txt"

    if len(argv) >= 3:
        project_name = argv[1]
        target_dir = argv[2].rstrip('/')
        libs = argv[3:]
    
    else:
        usage()
        exit(-1)

    fp = open("/".join([target_dir, cmake_filename]), "w")
    fp.write(PCL_CMAKE_TEMPLATE.format(project_name, src_path, include_path, " ".join(libs)))
    fp.close()
