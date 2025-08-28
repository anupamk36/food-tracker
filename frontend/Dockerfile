FROM node:20

WORKDIR /app

# Copy package files
COPY package.json package-lock.json* ./

# Force clean install, ensure vite is included
RUN rm -rf node_modules package-lock.json && npm install --legacy-peer-deps vite

COPY . .

EXPOSE 5173

CMD ["npm", "run", "dev"]
