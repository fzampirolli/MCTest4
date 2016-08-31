for file in *.jpg ; do convert "${file}" "${file/%jpg/eps}" ; done
