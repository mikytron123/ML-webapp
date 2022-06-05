FROM mcr.microsoft.com/dotnet/sdk:6.0 AS build
WORKDIR /src
COPY Blazor.csproj .
RUN dotnet restore Blazor.csproj
COPY . .
RUN dotnet build Blazor.csproj -c Release -o /app/build

FROM build AS publish
RUN dotnet publish Blazor.csproj -c Release -o /app/publish

FROM nginx:alpine AS final
WORKDIR /usr/share/nginx/html
COPY --from=publish /app/publish/wwwroot .
COPY nginx.conf /etc/nginx/nginx.conf