# Usar la imagen base de Jupyter
FROM jupyter/base-notebook:python-3.8.6

# Cambiar al usuario root para realizar la instalación
USER root

# Actualizar e instalar dependencias de R
RUN apt-get update && \
    apt-get install -y r-base r-base-dev libcurl4-gnutls-dev libssl-dev libxml2-dev && \
    apt-get clean


# Crear y dar permisos a los directorios necesarios para el kernel de Jupyter
RUN mkdir -p /usr/local/share/jupyter/kernels && \
    chmod -R 777 /usr/local/share/jupyter && \
    mkdir -p /usr/local/lib/R/site-library && \
    chmod -R 777 /usr/local/lib/R/site-library

# Cambiar de nuevo al usuario jovyan para las instalaciones de R y Python
USER jovyan

# Instalar los paquetes de R necesarios
COPY install_r_packages.R /home/jovyan/
RUN Rscript /home/jovyan/install_r_packages.R

# Copiar y instalar los requisitos de Python
COPY notebooks/requirements_jupyter-notebook.txt /home/jovyan/work/
RUN pip install -r /home/jovyan/work/requirements_jupyter-notebook.txt
