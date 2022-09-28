###############
# STAGE BUILD #
###############
FROM node:16-alpine AS build

WORKDIR /app

# copy dependency list
COPY ["package.json", "package-lock.json*", "./"]
# clean install dependencies, no devDependencies, no prepare script
RUN npm ci --production --ignore-scripts
# copy everything to the container
COPY . ./
# remove potential security issues
RUN npm audit fix
# build SvelteKit app
RUN npm run build

#############
# STAGE RUN #
#############
FROM nginx:1.19-alpine
# Remove default nginx website
RUN rm -rf /usr/share/nginx/html/*

# copy built static SvelteKit app to nginx
COPY --from=build /app/build /usr/share/nginx/html