FROM node:slim as quasar

WORKDIR /app

RUN yarn global add @quasar/cli

FROM quasar as build

WORKDIR /app

COPY frontend/ .

RUN quasar build

FROM alpine

WORKDIR /dist

COPY --from=build /app/dist/spa/ .

CMD ["cp", "-R", ".", "/out"]
