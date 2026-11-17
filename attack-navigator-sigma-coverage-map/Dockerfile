# 공식 저장소의 Dockerfile 에서 빌드 단계를 node:22-slim 으로 줄이고 layers 복사를 뺀 것입니다.
FROM node:22-slim AS build
WORKDIR /src/nav-app
COPY ./nav-app/package.json ./nav-app/package-lock.json ./
RUN npm ci
COPY ./nav-app/ ./
RUN npm run build -- --configuration production

FROM nginx:alpine
COPY --from=build /src/nav-app/dist/browser/ /usr/share/nginx/html/
EXPOSE 80
