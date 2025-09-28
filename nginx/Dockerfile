FROM nginx:1.25

RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d



# Copy and set permissions for entrypoint
COPY entrypoint.sh /usr/src/nexus_movies_backend/
RUN chmod +x /usr/src/nexus_movies_backend/entrypoint.sh