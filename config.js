// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyBsDEFSMwRucujCmeMmG7o3jpq2Noldgtk",
  authDomain: "stockinsight-78a23.firebaseapp.com",
  projectId: "stockinsight-78a23",
  storageBucket: "stockinsight-78a23.appspot.com",
  messagingSenderId: "177655953484",
  appId: "1:177655953484:web:723b559b94eb0afa6a5ce9",
  measurementId: "G-H0SM27DNME"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);