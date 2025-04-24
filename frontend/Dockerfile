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

# Expose the development server port
EXPOSE 3000

# Start the development server
CMD ["npm", "run", "dev"]