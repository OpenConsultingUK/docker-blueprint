# Use a multi-stage build to reduce the size of the final image.
#   This example is optimized to reduce final image size rather than for simplicity.
# Using a -slim image also greatly reduces image size.
# It is possible to use -alpine images instead to further reduce image size, but this comes
# with several important caveats.
#   - Alpine images use MUSL rather than GLIBC (as used in the default Debian-based images).
#   - Most Python packages that require C code are tested against GLIBC, so there could be
#     subtle errors when using MUSL.
#   - These Python packages usually only provide binary wheels for GLIBC, so the packages
#     will need to be recompiled fully within the Docker images, increasing build times.
FROM python:3.10-slim

# Pin Poetry to a specific version to make Docker builds reproducible.
ENV POETRY_VERSION 1.7.1

# Set ENV variables that make Python more friendly to running inside a container.
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1

# By default, pip caches copies of downloaded packages from PyPI. These are not useful within
# a Docker image, so disable this to reduce the size of images.
ENV PIP_NO_CACHE_DIR 1

# Upgrade pip to the latest version
RUN pip install --upgrade pip

# Install any system dependencies required to build wheels, such as C compilers or system packages
# For example:
#RUN apt-get update && apt-get install -y \
#    gcc \
#    && rm -rf /var/lib/apt/lists/*

# Install Poetry into the global environment to isolate it from the venv. This prevents Poetry
# from uninstalling parts of itself.
RUN pip install "poetry==${POETRY_VERSION}"

# Pre-download/compile wheel dependencies into a virtual environment.
# Doing this in a multi-stage build allows omitting compile dependencies from the final image.
# This must be the same path that is used in the final image as the virtual environment has
# absolute symlinks in it.
ENV VIRTUAL_ENV /opt/venv
RUN python -m venv ${VIRTUAL_ENV}
ENV PATH "${VIRTUAL_ENV}/bin:${PATH}"

# Set the home directory for the user
ENV HOME /home/user

# Create the home directory for the new user.
RUN mkdir -p ${HOME}

# Create the user so the program doesn't run as root. This increases security of the container.
RUN groupadd -r user && \
    useradd -r -g user -d ${HOME} -s /sbin/nologin -c "Docker image user" user

# Setup application install directory.
ENV APP_HOME ${HOME}/app

# Create the application's home directory
RUN mkdir ${APP_HOME}

# If you use Docker Compose volumes, you might need to create the directories in the image,
# otherwise when Docker Compose creates them they are owned by the root user and are inaccessible
# by the non-root user. See https://github.com/docker/compose/issues/3270

# Set the working directory for the subsequent commands
WORKDIR ${APP_HOME}

# Copy the project configuration file
COPY pyproject.toml ./

# Don't install the package itself with Poetry because it will install it as an editable install.
# TODO: Improve this when non-editable `poetry install` is supported in Poetry.
#    https://github.com/python-poetry/poetry/issues/1382
RUN poetry install --only flask --no-root

# Create views folder and copy static, templates, and app.py into it
RUN mkdir -p views
COPY views/flask/static views/static
COPY views/flask/templates views/templates
COPY views/flask/app.py views/app.py

# Add the Poetry binaries to the user's PATH
RUN export PATH="/home/user/.local/bin:$PATH"

# Switch to the non-root user
USER user

# Set environment variables for FastAPI
ENV FASTHOST=0.0.0.0
ENV FASTPORT=9001
ENV HOST=0.0.0.0
ENV PORT=8000

# Expose the port the application will run on
EXPOSE 8000

# Define the default command to run when the container starts
CMD ["poetry", "run", "python", "views/app.py"]
