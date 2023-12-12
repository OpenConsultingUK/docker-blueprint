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
FROM nginx:stable-alpine

# Remove the default nginx configuration file
RUN rm /etc/nginx/conf.d/default.conf

# Copy custom nginx configuration file to the appropriate location
COPY views/nginx/default.conf /etc/nginx/conf.d/

# Copy SSL certificates to the nginx SSL directory
COPY views/nginx/certs/fullchain.pem /etc/ssl/certs/fullchain.pem
COPY views/nginx/certs/privkey.pem /etc/ssl/private/privkey.pem

# Set the working directory to the default nginx HTML directory
WORKDIR /var/www/html

# Expose port 80 to allow external access
EXPOSE 80
