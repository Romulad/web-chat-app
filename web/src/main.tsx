import { StrictMode, Suspense } from 'react';
import { createRoot } from 'react-dom/client';

import { RouterProvider } from 'react-router-dom';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.min.css';

import './index.css';
import router from './router';

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <Suspense fallback={"Loading"}>
      <RouterProvider router={router}/>
      <ToastContainer 
      position="top-right"/>
    </Suspense>
  </StrictMode>,
)
