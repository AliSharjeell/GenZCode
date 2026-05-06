# Use Node.js official lightweight image
FROM node:20-alpine

# Set working directory
WORKDIR /app

# Copy package descriptors
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy all source files
COPY . .

# Expose Next.js default port
EXPOSE 3000

# Run in development mode
CMD ["npm", "run", "dev"]
