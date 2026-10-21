Quick frontend + Node API setup

1) Install Node dependencies for the API and frontend

# in project root
cd api
npm install

# in frontend
cd ../frontend
npm install

2) Run services

# start Node API
cd ../api
npm run dev

# start React dev server
cd ../frontend
npm run dev

3) Use the React app at http://localhost:5173 to upload photos to the Node API (http://localhost:4000/api/upload).

Notes:
- The Node API is a lightweight prototype that saves uploads to `api/uploads/` and returns filename-based heuristic predictions.
- To wire image recognition to a real vision API, replace `recognizeStub` in `api/server.js` or use `diet_ai.recognize_image_stub` via an HTTP bridge.
- Flask CORS has been enabled to allow cross-origin requests during development.
