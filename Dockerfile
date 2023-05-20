FROM node:20-alpine

# Prepare non-root user
RUN addgroup -S appgroup && adduser -S appuser -G appgroup
WORKDIR /app
RUN chown -R appuser:appgroup /app
USER appuser

# Copy package.json to the working directory
COPY src/package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the project  
COPY ./src/. ./

EXPOSE 3000

# Start the server
CMD ["node", "server.js"]