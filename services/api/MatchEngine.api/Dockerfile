# Stage 1: Base Runtime Setup
FROM mcr.microsoft.com/dotnet/aspnet:10.0 AS base
WORKDIR /app
EXPOSE 5024
ENV ASPNETCORE_URLS=http://+:5024

# Stage 2: Nuget Package Restore (The Caching Trick)
FROM mcr.microsoft.com/dotnet/sdk:10.0 AS build
WORKDIR /src
COPY ["MatchEngine.Api.csproj", "./"]
RUN dotnet restore "./MatchEngine.Api.csproj"

# Stage 3: Source Compilation
COPY . .
RUN dotnet build "MatchEngine.Api.csproj" -c Release -o /app/build

# Stage 4: Publishing Binaries
FROM build AS publish
RUN dotnet publish "MatchEngine.Api.csproj" -c Release -o /app/publish /p:UseAppHost=false

# Stage 5: Final Assembly
FROM base AS final
WORKDIR /app
COPY --from=publish /app/publish .
ENTRYPOINT ["dotnet", "MatchEngine.Api.dll"]