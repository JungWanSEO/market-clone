import { initializeApp } from "firebase/app";
// import { getDatabase } from "firebase/database";
// import { getStorage } from "firebase/storage";
// import { getAuth } from "firebase/auth";

// TODO: Replace the following with your app's Firebase project configuration
// See: https://firebase.google.com/docs/web/learn-more#config-object
// Your web app's Firebase configuration
const firebaseConfig = {
  apiKey: process.env.VITE_APP_KEY,
  authDomain: process.env.VITE_AUTH_DOMAIN,
  databaseURL: process.env.VITE_DB_URL,
  projectId: process.env.VITE_PROJECT_ID,
  storageBucket: process.env.VITE_STORAGE_BUCKET,
  messagingSenderId: process.env.VITE_MESSAGE_ID,
  appId: process.env.VITE_APP_ID,
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);

// // Initialize Realtime Database and get a reference to the service
// const database = getDatabase(app);
// // Initialize Cloud Storage and get a reference to the service
// const storage = getStorage(app);

// const auth = getAuth(app);
