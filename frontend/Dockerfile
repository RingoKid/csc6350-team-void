FROM node:20-slim

WORKDIR /app

# Ensure node_modules directory is created
RUN mkdir -p /app/node_modules

# Copy package.json and package-lock.json
COPY void-fe/package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application files
COPY void-fe/. .

# Build for production
RUN npm run build

# Install serve package
RUN npm install -g serve

EXPOSE 3000

# Serve the built application
CMD ["serve", "-s", "dist", "-l", "3000"]