options(repos = 'http://cran.us.r-project.org')

# Set the local library path for the 'jovyan' user
.libPaths('/home/jovyan/.local/lib/R/library')

packages <- c("IRkernel", "ggplot2", "lattice", "reticulate", "mgcv")
install.packages(packages, lib = .libPaths()[1])

# Register the R kernel with Jupyter
IRkernel::installspec(user = TRUE)
