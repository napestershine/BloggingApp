# Working Dockerfile for Next.js application
FROM node:18-alpine

WORKDIR /app

# Copy all files first (will copy node_modules if present)
COPY . .

# Ensure we have package files
COPY package.json package-lock.json ./

# Install dependencies (this will work even if node_modules exists)
RUN npm install --legacy-peer-deps

# Build the application
ENV NODE_ENV=production
RUN npm run build

# Expose port
EXPOSE 3000

# Start the application
CMD ["npm", "start"]