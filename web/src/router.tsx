import { createBrowserRouter } from "react-router-dom";

import { 
  ErrorPage,
  CreateAccountPage,
  HomePage
} from "./pages";
import { 
  createAccountPath, 
  homePath
} from "./lib/paths";


const router = createBrowserRouter([
  {
    path: homePath,
    element: <HomePage />,
    errorElement: <ErrorPage />,
  },
  {
    path: createAccountPath,
    element: <CreateAccountPage />,
    errorElement: <ErrorPage />,
  },
]);

export default router;