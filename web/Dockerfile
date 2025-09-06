# Working Dockerfile for Next.js application
FROM node:18-alpine

WORKDIR /app

# Copy package files first for better caching
COPY package.json package-lock.json ./

# Install dependencies
RUN npm install --legacy-peer-deps

# Copy the rest of the application files
COPY . .
# Build the application
ENV NODE_ENV=production
RUN npm run build

# Expose port
EXPOSE 3000

# Start the application
CMD ["npm", "start"]